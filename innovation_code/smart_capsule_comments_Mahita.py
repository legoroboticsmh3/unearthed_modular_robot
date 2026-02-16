# Smart Capsule app
# Touch UI with live camera view and image scanning (ORB matcher).

import os, time, cv2, numpy as np
import tkinter as tk

from PIL import Image, ImageTk, ImageDraw, ImageFont

import Adafruit_DHT as dht
from gpiozero import InputDevice, OutputDevice, RGBLED
from colorzero import Color

import threading

# Peltier cooler control (GPIO 21)
peltier_pin = OutputDevice(21)

# Try to import Picamera2. If unavailable we still run but camera features
# will be disabled.
PICAMERA_AVAILABLE = True
try:
    from picamera2 import Picamera2
except Exception:
    PICAMERA_AVAILABLE = False


# ---------- Screen layout constants ----------
W, H = 800, 480
BAR_H = 100              # bottom control bar height
LIVE_AREA = (W, H - BAR_H)
CAM_SIZE = (800, 480)
LOGO_PATH = "sac_logo.png"
REF_DIR = "refs"        # folder for reference images used by the scanner


def read_dht():
    """Read the DHT22 sensor and return (temp_C, humidity_pct).

    Plain explanation:
    - The DHT22 is a simple temperature + humidity sensor wired to a GPIO pin.
    - This function asks the sensor for a reading using `read_retry`, which
      will try a few times if the first attempt fails (this sensor sometimes
      returns intermittent errors).
    - The returned values are (humidity, temperature) according to the
      Adafruit_DHT API; we reformat them here as (temperature, humidity)
      rounded to one decimal place because the UI only needs a simple
      human-readable number.

    Returns:
      (temp_C, humidity_pct) — both floats with one decimal place.
    """
    humidity_temp_sensor = 4
    h, t = dht.read_retry(dht.DHT22, humidity_temp_sensor)
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))
    humidity = float("{0:0.1f}".format(h))
    temp = float("{0:0.1f}".format(t))
    return (temp, humidity)


def _font(size):
    """Return a Pillow font object for drawing text.

    Plain explanation:
    - On Linux systems a nice TTF font is usually available at the path used
      below. If that font is not present (for example, on the hub or on a
      minimal image) we gracefully fall back to Pillow's built-in bitmap
      font so the UI still shows readable text.
    - The `size` parameter controls text size for the drawn images.
    """
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()


def _safety_state(temp, rh):
    """Decide a simple safety label from temperature and humidity.

    Plain explanation and reasoning:
    - We give the capsule a human-friendly status label so a viewer can tell
      at a glance whether the environment is good for the artifact.
    - 'SAFE' means both temperature and humidity are within tight target
      ranges chosen for sensitive items. These are conservative defaults and
      can be changed to match the artifact's needs.
    - 'YELLOW' is a caution state used when values are slightly outside the
      ideal but not yet critical.
    - 'RED' signals the measured values are outside the acceptable window and
      may need human attention.

    Notes:
    - If either value is None (sensor failure), we show 'YELLOW' to indicate
      caution rather than silently assuming everything is OK.
    - The numeric thresholds below are simple and intentionally readable; if
      you need more precise rules (time-weighted averages, hysteresis, or
      logging), add that logic here.
    """
    if temp is None or rh is None:
        return "YELLOW"
    safe_t = 18.0 <= temp <= 24.0
    safe_h = 46.0 <= rh <= 52.0
    if safe_t and safe_h:
        return "SAFE"
    if (16.0 <= temp <= 26.0) and (40.0 <= rh <= 58.0):
        return "YELLOW"
    return "RED"


def _draw_placeholder_logo(draw, box):
    """Draw a simple box and 'SAC' text when no logo file is present."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=20, fill=(25, 25, 25), outline=(70, 70, 70), width=2)
    draw.text((x0 + 20, y0 + 95), " SAC", fill=(120, 200, 255), font=_font(75))


def make_status_image(temp, rh):
    """Build a simple status picture showing logo, temp, humidity, and tips.

    This is shown when the camera is not active.
    """
    w, h = LIVE_AREA
    img = Image.new("RGB", (w, h), (10, 10, 10))
    d = ImageDraw.Draw(img)

    # top banner
    d.rectangle([0, 0, w, 60], fill=(0, 0, 0))
    d.text((12, 14), "Smart Artifact Capsule -- IDLE", fill=(255, 255, 255), font=_font(28))

    # logo or placeholder
    logo_box = (30, 90, 290, 350)
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA").resize((260, 260), Image.LANCZOS)
            img.paste(logo, (logo_box[0], logo_box[1]), logo)
        except Exception:
            _draw_placeholder_logo(d, logo_box)
    else:
        _draw_placeholder_logo(d, logo_box)

    # show readings and safety state
    bx = 320
    d.text((bx, 110), "Capsule Status", fill=(255, 255, 0), font=_font(30))
    t_txt = "--" if temp is None else f"{temp:.1f} *C"
    h_txt = "--" if rh is None else f"{rh:.0f} % RH"
    d.text((bx, 160), f"Temperature : {t_txt} (Target 18-24 *C)", fill=(220, 220, 220), font=_font(22))
    d.text((bx, 198), f"Humidity  : {h_txt} (Target 46-52%)", fill=(220, 220, 220), font=_font(22))
    safety = _safety_state(temp, rh)
    d.text((bx + 12, 252), safety, fill=(0, 0, 0), font=_font(22))
    d.text((30, h - 40), "Tap LIVE to open camera. Tap SCAN to analyze. Tap HIDE to return.",
           fill=(180, 180, 180), font=_font(18))
    return img


# ---------- ORB (image matching) setup ----------
# ORB finds small distinctive features; BFMatcher compares them.
orb = cv2.ORB_create(nfeatures=1000)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

print("all imports done")


def load_refs():
    """Load reference images from the `refs` folder and compute ORB features.

    Plain explanation:
    - The scanner compares live frames to a small gallery of known images.
    - For speed we preprocess each reference image once: load it in
      grayscale, find ORB keypoints and descriptors, and store them in a
      simple dictionary list.
    - The returned `gallery` is a list of dicts where `label` is the file
      name (used as the human-readable result) and `des` is the descriptor
      array used during matching.
    - If the `refs` folder does not exist it is created so the program can
      be shipped with an empty refs directory and users can add images later.
    """
    gallery = []
    os.makedirs(REF_DIR, exist_ok=True)
    for fn in sorted(os.listdir(REF_DIR)):
        if fn.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(REF_DIR, fn)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            kp, des = orb.detectAndCompute(img, None)
            gallery.append({"label": os.path.splitext(fn)[0], "img": img, "kp": kp, "des": des})

    return gallery


REFS = load_refs()


def orb_best_match(frame_bgr):
    """Compare a camera frame to the loaded references.

    Simple explanation of the algorithm:
    1. Convert the incoming camera frame to grayscale and extract ORB
       descriptors (the same kind we computed for the references).
    2. For each reference image in `REFS` use a brute-force matcher to pair
       descriptors. The matcher returns matches with a `distance` value; lower
       is better.
    3. Count how many matches are 'good' (we use `distance < 60` as a rule of
       thumb). The confidence is the number of good matches divided by the
       total matches for that reference. This gives a simple fraction in
       [0, 1] representing how well the two images agree.

    Notes and limitations:
    - This is a lightweight heuristic: it is fast and easy to understand but
      not perfect. Objects that are very different in lighting, scale, or
      orientation may fail to match even if they are the same object.
    - You can improve results by adding more reference images taken from
      different angles and lighting conditions, or by tuning the distance
      threshold and `nfeatures` used when creating the ORB detector.

    Returns:
      (label, confidence) — `label` is a short text from the reference file
      name and `confidence` is a float rounded to two decimals.
    """
    if not REFS:
        return ("Add images to refs/", 0.0)
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    kp, des = orb.detectAndCompute(gray, None)
    if des is None:
        return ("No features", 0.0)
    best_label, best_score = "No Match", 0.0
    for r in REFS:
        if r["des"] is None:
            continue
        matches = bf.match(des, r["des"])
        if not matches:
            continue
        matches = sorted(matches, key=lambda x: x.distance)
        # treat matches with small distance as 'good'
        good = [m for m in matches if m.distance < 60]
        score = len(good) / max(len(matches), 1)

        if score > best_score:
            best_score, best_label = score, r["label"]
    conf = round(float(best_score), 2)
    return (best_label, conf)


# ---------- Tkinter GUI application ----------


class App:
    """Main application object.

    Plain explanation of responsibilities:
    - Create and manage the full-screen Tk window and the simple control
      buttons across the bottom.
    - Manage the camera lifecycle (start/stop) and provide a small live view.
    - Provide a 'scan' action that captures one frame, runs ORB matching,
      and displays a static result image.
    - Periodically read sensors (DHT22, vibration) and set the RGB LED and
      cooler state. This is done on a short repeating timer so the UI stays
      responsive.
    """

    def __init__(self, root):
        self.root = root
        root.title("Smart Artifact Capsule")
        root.attributes("-fullscreen", True)
        root.configure(bg="black")

        # state
        self.photo = None
        self.mode = "idle"  # 'idle', 'live', 'result', or 'frozen'
        self.last_bgr = None
        self.picam2 = None
        self.cam_running = False
        self.cooling_on = False
        self.cooling_start_time = None

        # try to start camera; if it fails we keep going without camera
        try:
            self.picam2 = Picamera2()
            cfg = self.picam2.create_preview_configuration(main={"size": CAM_SIZE, "format": "RGB888"})
            self.picam2.configure(cfg)
        except Exception as e:
            print("Camera init failed:", e)
            self.picam2 = None

        # area where video or status image is shown
        self.video = tk.Label(root, bg="black")
        self.video.place(x=0, y=0, width=W, height=H - BAR_H)

        # small status label
        self.status = tk.Label(root, text="Ready . LIVE/SCAN", font=("Arial", 16), bg="black", fg="white")
        self.status.place(x=10, y=H - 130)

        # bottom control bar with buttons
        bar = tk.Frame(root, bg="#111")
        bar.place(x=0, y=H - BAR_H, width=W, height=BAR_H)
        style = dict(font=("Arial", 18, "bold"), bg="#2d6cdf", fg="white", bd=0, activebackground="#2552a3")

        bw = int(W / 4)
        tk.Button(bar, text="LIVE", command=self.on_live, **style).place(x=10, y=15, width=bw - 20, height=70)
        tk.Button(bar, text="HIDE", command=self.on_hide, **style).place(x=1 * bw + 10, y=15, width=bw - 20, height=70)
        tk.Button(bar, text="SCAN", command=self.on_scan, **style).place(x=2 * bw + 10, y=15, width=bw - 20, height=70)
        tk.Button(bar, text="QUIT", command=root.destroy, font=("Arial", 18, "bold"),
                  bg="#b02a37", fg="white", bd=0, activebackground="#7c1e28").place(x=3 * bw + 10, y=15,
                                                                                         width=bw - 20, height=70)

        # start repeating updates
        self.update_screen()
        self.update_sensors()

    # ---------- Camera helpers ----------
    def start_camera(self):
        """Start the Picamera2 camera if configured.

        Plain explanation:
        - If `Picamera2` was not imported successfully during startup, the
          camera-related methods are no-ops and the app continues showing the
          status image instead.
        - We set `self.cam_running = True` only after the camera has started and
          add a small sleep so the sensor has a fraction of a second to
          produce a first frame.
        """
        if self.picam2 is None or self.cam_running:
            return
        try:
            self.picam2.start()
            self.cam_running = True
            time.sleep(0.1)
            print("picam working")
        except Exception as e:
            print("start_camera error:", e)

    def stop_camera(self):
        """Stop the camera if it is running."""
        if self.picam2 and self.cam_running:
            try:
                self.picam2.stop()
            except Exception as e:
                print("stop_camera error:", e)
        self.cam_running = False

    def close_camera(self):
        """Release camera resources when the app exits."""
        if self.picam2:
            try:
                if self.cam_running:
                    self.picam2.stop()
                self.picam2.close()
            except Exception as e:
                print("close_camera error", e)
            self.picam2 = None

    def grab_frame(self):
        """Capture and return a single RGB frame from the camera.

        Plain explanation:
        - Returns a NumPy array in RGB order suitable for conversion to a
          Pillow image. If the camera is not available or an error occurs,
          `None` is returned. The callers handle `None` by falling back to the
          status picture so the UI remains usable even without a camera.
        """
        if not (self.picam2 and self.cam_running):
            return None
        try:
            rgb = self.picam2.capture_array()
            return rgb
        except Exception as e:
            print("grab_frame error:", e)
            return None

    # ---------- UI update loop ----------
    def update_screen(self):
        """Refresh the main display area depending on the current mode.

        Modes and behavior:
        - 'live': show a continuous camera feed (if available). If the camera
          is not ready, show the status image instead.
        - 'result': show a single static image that was produced by a scan.
        - otherwise (idle): read the temperature/humidity and show the
          status image built by `make_status_image`.

        The function schedules itself with `root.after` so it runs repeatedly
        without blocking the Tk event loop. The refresh rate is faster while
        in live mode to create a smoother video preview.
        """
        if self.mode == "live":
            bgr = self.grab_frame()
            if bgr is None:
                img = make_status_image(None, None)
            else:
                self.last_bgr = bgr
                disp = bgr.copy()
                cv2.rectangle(disp, (0, 0), (W, 40), (0, 0, 0), -1)
                cv2.putText(disp, "LIVE VIEW -- Tap SCAN to analyze . HIDE to return",
                            (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                img = Image.fromarray(cv2.cvtColor(disp, cv2.COLOR_BGR2RGB))
        elif self.mode == "result":
            img = self.result_image if self.result_image is not None else make_status_image(None, None)
        else:
            t, h = read_dht()
            img = make_status_image(t, h)

        img = img.resize((W, H - BAR_H))
        self.photo = ImageTk.PhotoImage(img)
        self.video.configure(image=self.photo)
        self.root.after(50 if self.mode == "live" else 300, self.update_screen)

    def update_sensors(self):
        """Periodic sensor checks: cooler timeout and sensor-driven actions."""
        self.check_cooler_off()
        self.artifact_condition_check()
        self.root.after(250, self.update_sensors)

    # ---------- Button handlers ----------
    def on_live(self):
        # go to live camera view
        self.mode = "live"
        self.start_camera()

    def on_hide(self):
        # go back to idle/status and stop camera
        self.mode = "idle"
        self.stop_camera()

    def on_scan(self):
        """Capture one frame and run the ORB-based image matcher.

        Plain explanation of flow:
        1. If we are already showing the live view use the last captured
           frame (fast and non-disruptive). Otherwise, briefly start the
           camera, capture a frame, and stop it—this keeps scanning usable
           when the camera is normally off.
        2. Pass the frame to `orb_best_match` to find the best reference and a
           confidence score.
        3. Draw the result text onto the captured image and switch to the
           'result' mode. The camera is stopped so the result remains static
           for easy reading.
        """
        frame_bgr = None
        if self.mode == "live":
            frame_bgr = self.last_bgr if self.last_bgr is not None else self.grab_frame()
        else:
            self.start_camera()
            frame_bgr = self.grab_frame()
            self.stop_camera()

        if frame_bgr is None:
            self.mode = "idle"
            print("on_scan: no frame")
            return

        label, conf = orb_best_match(frame_bgr)
        print("on_scan: label=%s, conf=%s" % (label, conf))

        disp = frame_bgr.copy()
        overlay = disp.copy()
        cv2.rectangle(overlay, (0, 0), (W, 40), (0, 0, 0), -1)
        alpha = 0.35
        disp = cv2.addWeighted(overlay, alpha, disp, 1 - alpha, 0)

        # center the match text
        text = f"{label} . conf {conf:.2f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1.2
        thickness = 3
        (tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
        cx, cy = W // 2, (H - BAR_H) // 2
        org = (cx - tw // 2, cy + th // 2)
        cv2.putText(disp, text, org, font, scale, (0, 0, 0), thickness + 3, cv2.LINE_AA)
        cv2.putText(disp, text, org, font, scale, (255, 255, 0), thickness, cv2.LINE_AA)

        cv2.rectangle(disp, (0, 0), (W, 40), (0, 0, 0), -1)
        cv2.putText(disp, "SCAN RESULT -- Tap LIVE to resume camera . HIDE for status",
                    (12, 28), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        self.result_image = Image.fromarray(cv2.cvtColor(disp, cv2.COLOR_BGR2RGB))
        self.mode = "result"
        self.stop_camera()

    def draw(self, bgr, banner=None, foot=None):
        """Show a BGR image in the UI, with optional banner/foot text."""
        disp = bgr.copy()
        if banner:
            cv2.rectangle(disp, (0, 0), (W, 40), (0, 0, 0), -1)
            cv2.putText(disp, banner, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if foot:
            cv2.rectangle(disp, (0, H - 140), (W, H - 100), (0, 0, 0), -1)
            cv2.putText(disp, foot, (12, H - 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2, cv2.LINE_AA)
        rgb = cv2.cvtColor(disp, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb).resize((W, H - BAR_H))
        self.photo = ImageTk.PhotoImage(img)
        self.video.configure(image=self.photo)

    def on_freeze(self):
        # show a frozen image (not updated)
        self.mode = "frozen"
        self.status.config(text="Frozen frame")

    def artifact_condition_check(self):
        """Check environmental and motion sensors and update LED/cooling.

        Plain explanation of what this does and why:
        - The function reads three inputs: a vibration sensor, and the
          temperature/humidity from the DHT22.
        - It uses a small set of thresholds to pick a color for the RGB LED
          so a person standing near the capsule can see the state quickly.
        - If temperature is above the high threshold we call
          `trigger_cooling()` to switch on the Peltier element briefly.

        Design notes:
        - Vibration detection is handled first because it signals physical
          disturbance and should be obvious (red) immediately.
        - The humidity and temperature checks are intentionally simple: for
          production you might prefer time-averaged values or hysteresis to
          avoid rapid color flicker on borderline conditions.
        """
        vibration_sensor = InputDevice(17)
        humidity_temp_sensor = 4

        # thresholds for warnings
        h_upper = 70
        h_lower = 55
        t_upper = 30
        t_lower = 20

        # RGB LED hardware pins
        red_pin = 10
        green_pin = 9
        blue_pin = 11
        rgb_led = RGBLED(red_pin, green_pin, blue_pin, active_high=False)

        # vibration takes priority
        if vibration_sensor.is_active:
            rgb_led.color = Color("red")
            print("Vibration detected!")

        # read DHT22 sensor
        h, t = dht.read_retry(dht.DHT22, humidity_temp_sensor)
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))
        humidity = float("{0:0.1f}".format(h))
        temp = float("{0:0.1f}".format(t))

        # humidity color
        if humidity > h_upper:
            rgb_led.color = Color("orange")
            print("Humidity levels are too high")
        elif humidity < h_lower:
            rgb_led.color = Color("blue")
            print("Humidity levels are too low")
        else:
            rgb_led.color = Color("green")

        # temperature color and possible cooler trigger
        if temp > t_upper:
            rgb_led.color = Color("purple")
            print(f"Temperature levels are too high, temp: {temp}")
            self.trigger_cooling()
        elif temp < t_lower:
            rgb_led.color = Color("yellow")
            print("Temperature levels are too low")
        else:
            rgb_led.color = Color("green")

    def trigger_cooling(self):
        """Start the Peltier cooler for a short, controlled burst.

        Plain explanation:
        - To avoid running the Peltier continuously (which could waste power
          or stress the hardware) we only run it for a short interval and
          record the start time. `check_cooler_off()` will later turn it off
          after the configured timeout.
        - If the cooler is already on this function does nothing.
        """
        if self.cooling_on:
            print("Peltier is currently cooling")
            return

        peltier_pin.on()
        self.cooling_on = True
        self.cooling_start_time = time.time()
        print("peltier turned on")

    def check_cooler_off(self):
        """Turn off the Peltier when its allowed run time has elapsed.

        Plain explanation:
        - This is a safety and power-saving measure. We check how long the
          cooler has been on and, once the elapsed time reaches 20 seconds,
          switch it off and clear the tracking fields so it can be triggered
          again later if needed.
        - The 20-second value is a simple default; tune it to suit your
          hardware and thermal response.
        """
        if self.cooling_on and self.cooling_start_time is not None:
            if time.time() - self.cooling_start_time >= 20.0:
                peltier_pin.off()
                self.cooling_on = False
                self.cooling_start_time = None
                print("Peltier turned off")


if __name__ == "__main__":
    # start the GUI app when run directly
    print("starting main")
    root = tk.Tk()
    root.geometry(f"{W}x{H}+0+0")

    try:
        app = App(root)
        root.mainloop()
    finally:
        # ensure camera is closed on exit
        app.close_camera()
