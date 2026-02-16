# smart_capsule_commented_for_learning.py
# Fully commented, layman-friendly version of the Smart Capsule app.

# This file creates a small touchscreen-style application that:
# - Shows an idle/status screen (logo + temp/humidity)
# - Can open a live camera preview
# - Can "scan" the current camera view and match it against stored
#   reference images using a lightweight ORB feature matcher
# - Reads a DHT22 sensor (temperature + humidity), a vibration input,
#   shows an RGB LED status, and can run a Peltier cooler briefly when hot.

import os, time, cv2, numpy as np
import tkinter as tk

from PIL import Image, ImageTk, ImageDraw, ImageFont

import Adafruit_DHT as dht
from gpiozero import InputDevice, OutputDevice, RGBLED
from colorzero import Color

import threading

# Hardware: Peltier cooler driver on GPIO 21
peltier_pin = OutputDevice(21)

# Picamera2 is optional; the app runs without it but camera features won't work.
PICAMERA_AVAILABLE = True
try:
    from picamera2 import Picamera2
except Exception:
    PICAMERA_AVAILABLE = False


# Screen layout constants (designed for 800x480 displays)
W, H = 800, 480
BAR_H = 100                # height of the bottom button bar
LIVE_AREA = (W, H - BAR_H)
CAM_SIZE = (800, 480)
LOGO_PATH = "sac_logo.png"  # optional local logo file
REF_DIR = "refs"            # folder for reference images used by the scanner


# ---------------- Sensor helper ----------------
def read_dht():
    """Read the DHT22 and return (temperature_C, humidity_percent).

    Layman's explanation:
    - The DHT22 sensor gives temperature and humidity readings.
    - `read_retry` will try a few times because the sensor can sometimes fail
      on a single read.
    - We return the values rounded to one decimal place so they look nice on
      the display.
    """
    humidity_temp_sensor = 4  # GPIO pin where DHT data line is connected
    h, t = dht.read_retry(dht.DHT22, humidity_temp_sensor)
    # Print a short log for debugging
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))
    humidity = float("{0:0.1f}".format(h))
    temp = float("{0:0.1f}".format(t))
    return (temp, humidity)


# ---------------- Small drawing helpers ----------------
def _font(size):
    """Return a PIL font. Use a nice TTF if available, otherwise a default.

    Layman: this makes the on-screen text use a nicer font when possible.
    """
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()


def _safety_state(temp, rh):
    """Return a small label 'SAFE'/'YELLOW'/'RED' based on temp and humidity.

    Layman: shows whether the capsule environment is good for stored items.
    - SAFE = both temp and humidity are in the tight target window.
    - YELLOW = slightly outside the ideal range (or sensor failure).
    - RED = clearly outside safe limits.
    """
    # smart_capsule_commented_for_learning.py
    # Very simple comments for learners (middle-school level)

    import os, time, cv2, numpy as np
    import tkinter as tk
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    import Adafruit_DHT as dht
    from gpiozero import InputDevice, OutputDevice, RGBLED
    from colorzero import Color
    import threading

    # This controls a small cooler device (Peltier) attached to GPIO pin 21.
    peltier_pin = OutputDevice(21)

    # Camera library: if not on a Pi the import will fail and camera features
    # will be skipped.
    try:
        from picamera2 import Picamera2
        PICAMERA_AVAILABLE = True
    except Exception:
        PICAMERA_AVAILABLE = False

    # Screen and layout sizes (our app uses 800x480)
    W, H = 800, 480
    BAR_H = 100
    LIVE_AREA = (W, H - BAR_H)
    CAM_SIZE = (800, 480)
    LOGO_PATH = "sac_logo.png"
    REF_DIR = "refs"  # put images here to teach the app what to recognize


    def read_dht():
        """Get temperature and humidity from the DHT22 sensor.

        Simple: ask the sensor for values, round them to one decimal, and return
        them as (temperature, humidity).
        """
        pin = 4
        h, t = dht.read_retry(dht.DHT22, pin)
        # Format to one decimal place so the display looks neat.
        return (float("{0:0.1f}".format(t)), float("{0:0.1f}".format(h)))


    def _font(size):
        """Return a font for drawing text. If no nice font is available use a
        simple built-in one so the app still works everywhere."""
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except Exception:
            return ImageFont.load_default()


    def _safety_state(temp, rh):
        """Give a simple label: SAFE, YELLOW (be careful), or RED (bad).

        We use small number ranges so a person can quickly see if conditions are
        good for stored objects.
        """
        if temp is None or rh is None:
            return "YELLOW"
        if 18.0 <= temp <= 24.0 and 46.0 <= rh <= 52.0:
            return "SAFE"
        if 16.0 <= temp <= 26.0 and 40.0 <= rh <= 58.0:
            return "YELLOW"
        return "RED"


    def _draw_placeholder_logo(draw, box):
        """If there is no logo image, draw a simple box with 'SAC' text."""
        draw.rounded_rectangle(box, radius=20, fill=(25, 25, 25), outline=(70, 70, 70), width=2)
        draw.text((box[0] + 20, box[1] + 95), "SAC", fill=(120, 200, 255), font=_font(75))


    def make_status_image(temp, rh):
        """Build the picture shown when the camera is not active.

        This shows the logo, temperature, humidity, and the safety label.
        """
        w, h = LIVE_AREA
        img = Image.new("RGB", (w, h), (10, 10, 10))
        d = ImageDraw.Draw(img)

        # Top banner
        d.rectangle([0, 0, w, 60], fill=(0, 0, 0))
        d.text((12, 14), "Smart Artifact Capsule -- IDLE", fill=(255, 255, 255), font=_font(28))

        # Logo or placeholder
        logo_box = (30, 90, 290, 350)
        if os.path.exists(LOGO_PATH):
            try:
                logo = Image.open(LOGO_PATH).convert("RGBA").resize((260, 260), Image.LANCZOS)
                img.paste(logo, (logo_box[0], logo_box[1]), logo)
            except Exception:
                _draw_placeholder_logo(d, logo_box)
        else:
            _draw_placeholder_logo(d, logo_box)

        # Readings and label
        bx = 320
        d.text((bx, 110), "Capsule Status", fill=(255, 255, 0), font=_font(30))
        t_txt = "--" if temp is None else f"{temp:.1f} C"
        h_txt = "--" if rh is None else f"{rh:.0f} % RH"
        d.text((bx, 160), f"Temperature : {t_txt} (Target 18-24 C)", fill=(220, 220, 220), font=_font(22))
        d.text((bx, 198), f"Humidity    : {h_txt} (Target 46-52%)", fill=(220, 220, 220), font=_font(22))
        safety = _safety_state(temp, rh)
        d.text((bx + 12, 252), safety, fill=(0, 0, 0), font=_font(22))
        d.text((30, h - 40), "Tap LIVE to open camera. Tap SCAN to analyze.", fill=(180, 180, 180), font=_font(18))
        return img


    # --- Image matching setup (ORB) ---
    # ORB finds small visual 'features' in photos. We use it to compare what the
    # camera sees with pictures we keep in the refs/ folder.
    orb = cv2.ORB_create(nfeatures=1000)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


    def load_refs():
        """Load pictures from REF_DIR and find ORB features for each.

        Put photos of items you want the app to recognise into the refs/ folder.
        The file name (without extension) becomes the label shown after a scan.
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
                gallery.append({"label": os.path.splitext(fn)[0], "des": des})
        return gallery


    REFS = load_refs()


    def orb_best_match(frame_bgr):
        """Find which reference picture best matches the camera frame.

        Returns a (label, confidence) pair. Confidence is a simple number between
        0.0 and 1.0 that says how good the match is.
        """
        if not REFS:
            return ("Add images to refs/", 0.0)
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        kp, des = orb.detectAndCompute(gray, None)
        if des is None:
            return ("No features", 0.0)
        best_label, best_score = "No Match", 0.0
        for r in REFS:
            if r.get("des") is None:
                continue
            matches = bf.match(des, r["des"])
            if not matches:
                continue
            matches = sorted(matches, key=lambda x: x.distance)
            # we call a match 'good' when distance is small (here < 60)
            good = [m for m in matches if m.distance < 60]
            score = len(good) / max(len(matches), 1)
            if score > best_score:
                best_score, best_label = score, r["label"]
        return (best_label, round(float(best_score), 2))


    # --- The graphical app ---
    class App:
        """Simple app that shows status, live camera, and can scan images."""

        def __init__(self, root):
            # set up the window
            self.root = root
            root.title("Smart Artifact Capsule")
            root.attributes("-fullscreen", True)
            root.configure(bg="black")

            # state variables
            self.photo = None
            self.mode = "idle"  # 'idle', 'live', 'result', 'frozen'
            self.last_bgr = None
            self.picam2 = None
            self.cam_running = False
            self.cooling_on = False
            self.cooling_start_time = None

            # try to prepare the camera (may be missing on non-Pi machines)
            try:
                if PICAMERA_AVAILABLE:
                    self.picam2 = Picamera2()
                    cfg = self.picam2.create_preview_configuration(main={"size": CAM_SIZE, "format": "RGB888"})
                    self.picam2.configure(cfg)
                else:
                    self.picam2 = None
            except Exception as e:
                print("Camera init failed:", e)
                self.picam2 = None

            # place where video or status image appears
            self.video = tk.Label(root, bg="black")
            self.video.place(x=0, y=0, width=W, height=H - BAR_H)

            # small status text above buttons
            self.status = tk.Label(root, text="Ready . LIVE/SCAN", font=("Arial", 16), bg="black", fg="white")
            self.status.place(x=10, y=H - 130)

            # bottom buttons: LIVE, HIDE, SCAN, QUIT
            bar = tk.Frame(root, bg="#111")
            bar.place(x=0, y=H - BAR_H, width=W, height=BAR_H)
            style = dict(font=("Arial", 18, "bold"), bg="#2d6cdf", fg="white", bd=0, activebackground="#2552a3")
            bw = int(W / 4)
            tk.Button(bar, text="LIVE", command=self.on_live, **style).place(x=10, y=15, width=bw - 20, height=70)
            tk.Button(bar, text="HIDE", command=self.on_hide, **style).place(x=1 * bw + 10, y=15, width=bw - 20, height=70)
            tk.Button(bar, text="SCAN", command=self.on_scan, **style).place(x=2 * bw + 10, y=15, width=bw - 20, height=70)
            tk.Button(bar, text="QUIT", command=root.destroy, font=("Arial", 18, "bold"), bg="#b02a37", fg="white", bd=0, activebackground="#7c1e28").place(x=3 * bw + 10, y=15, width=bw - 20, height=70)

            # start automatic updates for the screen and sensors
            self.update_screen()
            self.update_sensors()

        # --- Camera helpers ---
        def start_camera(self):
            """Start the camera if we have one."""
            if self.picam2 is None or self.cam_running:
                return
            try:
                self.picam2.start()
                self.cam_running = True
                time.sleep(0.1)  # a small pause so the camera readies
            except Exception as e:
                print("start_camera error:", e)

        def stop_camera(self):
            """Stop the camera."""
            if self.picam2 and self.cam_running:
                try:
                    self.picam2.stop()
                except Exception as e:
                    print("stop_camera error:", e)
            self.cam_running = False

        def close_camera(self):
            """Close camera resources when app exits."""
            if self.picam2:
                try:
                    if self.cam_running:
                        self.picam2.stop()
                    self.picam2.close()
                except Exception as e:
                    print("close_camera error", e)
                self.picam2 = None

        def grab_frame(self):
            """Get one frame from the camera. Returns None if no camera."""
            if not (self.picam2 and self.cam_running):
                return None
            try:
                rgb = self.picam2.capture_array()
                return rgb
            except Exception as e:
                print("grab_frame error:", e)
                return None

        # --- Screen updates ---
        def update_screen(self):
            """Update what the user sees depending on mode (live/result/idle)."""
            if self.mode == "live":
                bgr = self.grab_frame()
                if bgr is None:
                    img = make_status_image(None, None)
                else:
                    self.last_bgr = bgr
                    disp = bgr.copy()
                    cv2.rectangle(disp, (0, 0), (W, 40), (0, 0, 0), -1)
                    cv2.putText(disp, "LIVE VIEW -- Tap SCAN to analyze . HIDE to return", (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                    img = Image.fromarray(cv2.cvtColor(disp, cv2.COLOR_BGR2RGB))
            elif self.mode == "result":
                img = self.result_image if self.result_image is not None else make_status_image(None, None)
            else:
                t, h = read_dht()
                img = make_status_image(t, h)
            img = img.resize((W, H - BAR_H))
            self.photo = ImageTk.PhotoImage(img)
            self.video.configure(image=self.photo)
            # run again after a short delay
            self.root.after(50 if self.mode == "live" else 300, self.update_screen)

        def update_sensors(self):
            """Check sensors and cooler timer every short time."""
            self.check_cooler_off()
            self.artifact_condition_check()
            self.root.after(250, self.update_sensors)

        # --- Buttons ---
        def on_live(self):
            # show the live camera view
            self.mode = "live"
            self.start_camera()

        def on_hide(self):
            # go back to the status picture and stop camera
            self.mode = "idle"
            self.stop_camera()

        def on_scan(self):
            """Take one picture, try to match it to refs/, and show the result."""
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
            # draw the label and confidence on the image
            disp = frame_bgr.copy()
            overlay = disp.copy()
            cv2.rectangle(overlay, (0, 0), (W, 40), (0, 0, 0), -1)
            disp = cv2.addWeighted(overlay, 0.35, disp, 0.65, 0)
            text = f"{label}  conf {conf:.2f}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 1.2
            thickness = 3
            (tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
            cx, cy = W // 2, (H - BAR_H) // 2
            org = (cx - tw // 2, cy + th // 2)
            cv2.putText(disp, text, org, font, scale, (0, 0, 0), thickness + 3, cv2.LINE_AA)
            cv2.putText(disp, text, org, font, scale, (255, 255, 0), thickness, cv2.LINE_AA)
            cv2.rectangle(disp, (0, 0), (W, 40), (0, 0, 0), -1)
            cv2.putText(disp, "SCAN RESULT -- Tap LIVE to resume camera . HIDE for status", (12, 28), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            self.result_image = Image.fromarray(cv2.cvtColor(disp, cv2.COLOR_BGR2RGB))
            self.mode = "result"
            self.stop_camera()

        def draw(self, bgr, banner=None, foot=None):
            """Show a given BGR image in the app window with optional text."""
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
            # stop updating the screen (show a frozen frame)
            self.mode = "frozen"
            self.status.config(text="Frozen frame")

        def artifact_condition_check(self):
            """Read vibration and DHT sensors and set the RGB LED color.

            Rules (simple):
              - If vibration detected -> red
              - If humidity high -> orange, low -> blue, good -> green
              - If temp high -> purple and start cooling; low -> yellow; good -> green
            """
            vibration_sensor = InputDevice(17)
            humidity_temp_sensor = 4
            h_upper = 70
            h_lower = 55
            t_upper = 30
            t_lower = 20
            red_pin = 10
            green_pin = 9
            blue_pin = 11
            rgb_led = RGBLED(red_pin, green_pin, blue_pin, active_high=False)

            if vibration_sensor.is_active:
                rgb_led.color = Color("red")
                print("Vibration detected!")

            h, t = dht.read_retry(dht.DHT22, humidity_temp_sensor)
            humidity = float("{0:0.1f}".format(h))
            temp = float("{0:0.1f}".format(t))

            if humidity > h_upper:
                rgb_led.color = Color("orange")
            elif humidity < h_lower:
                rgb_led.color = Color("blue")
            else:
                rgb_led.color = Color("green")

            if temp > t_upper:
                rgb_led.color = Color("purple")
                self.trigger_cooling()
            elif temp < t_lower:
                rgb_led.color = Color("yellow")
            else:
                rgb_led.color = Color("green")

        def trigger_cooling(self):
            """Turn the Peltier on for a short time to cool the capsule."""
            if self.cooling_on:
                return
            peltier_pin.on()
            self.cooling_on = True
            self.cooling_start_time = time.time()

        def check_cooler_off(self):
            """Turn the Peltier off after 20 seconds if it was turned on."""
            if self.cooling_on and self.cooling_start_time is not None:
                if time.time() - self.cooling_start_time >= 20.0:
                    peltier_pin.off()
                    self.cooling_on = False
                    self.cooling_start_time = None


    if __name__ == "__main__":
        print("starting main")
        root = tk.Tk()
        root.geometry(f"{W}x{H}+0+0")
        try:
            app = App(root)
            root.mainloop()
        finally:
            app.close_camera()
