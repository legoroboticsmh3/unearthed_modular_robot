# smart_capsule.py -- Touch UI + Live + Scan (ORB) for 800x480 screen

import os, time, cv2, numpy as np
import tkinter as tk

from PIL import Image, ImageTk, ImageDraw, ImageFont

import Adafruit_DHT as dht
import time
from gpiozero import InputDevice, OutputDevice, RGBLED
from colorzero import Color

import threading

#Define peltier pin
peltier_pin = OutputDevice(21)

#--------- Picamera2 (lazy start)-----
PICAMERA_AVAILABLE = True
try:
	from picamera2 import Picamera2
except Exception:
	PICAMERA_AVAILABLE = False
	
	
	
# --------- UI Layout ---------
W,H = 800,480
BAR_H = 100
LIVE_AREA = (W, H - BAR_H)
CAM_SIZE = (800, 480)
LOGO_PATH = "sac_logo.png"


REF_DIR = "refs"

def read_dht():
	
	humidity_temp_sensor = 4

	h,t = dht.read_retry(dht.DHT22, humidity_temp_sensor)
	print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))

	
	humidity = float("{0:0.1f}".format(h))
	temp = float("{0:0.1f}".format(t))
	return(temp, humidity)

def _font(size):
	try:
		return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
	except Exception:
		return ImageFont.load_default()

def _safety_state(temp, rh):
	if temp is None or rh is None:
		return "YELLOW"
	safe_t = 18.0 <= temp <= 24.0
	safe_h = 46.0 <= rh  <= 52.0
	if safe_t and safe_h:
		return "SAFE"
	if (16.0 <= temp <= 26.0) and (40.0 <= rh <= 58.0):
		return "YELLOW"
	return "RED"
	
def _draw_placeholder_logo(draw, box):
	x0, y0, x1, y1 = box
	draw.rounded_rectangle(box, radius=20,  fill=(25, 25, 25),  outline=(70, 70, 70), width=2)
	draw.text((x0+20,  y0+95),  " SAC", fill=(120,200,255),  font=_font(75))
	
def make_status_image(temp, rh):
	w, h = LIVE_AREA
	img = Image.new("RGB", (w, h), (10,10,10))
	d = ImageDraw.Draw(img)
	
	d.rectangle([0,0,w,60], fill=(0,0,0))
	d.text((12,14), "Smart Artifact Capsule -- IDLE", fill=(255,255,255), font=_font(28))
	
	
	logo_box = (30, 90, 290, 350)
	if os.path.exists(LOGO_PATH):
		try:
			logo = Image.open(LOGO_PATH).convert("RGBA").resize((260,260), Image.LANCZOS)
			img.paste(logo,  (logo_box[0], logo_box[1]), logo)
		except Exception:
			_draw_placeholder_logo(d, logo_box)
	else:
		_draw_placeholder_logo(d, logo_box)
	
	#status
	bx = 320
	d.text((bx,110), "Capsule Status", fill=(255,255,0), font=_font(30))
	t_txt = "--" if temp is None else f"{temp:.1f} *C"
	h_txt = "--" if rh  is None else f"{rh:.0f} % RH"
	d.text((bx,160), f"Tempertature : {t_txt} (Target 18-24 *C)", fikll=(220,220,220), font=_font(22))
	d.text((bx,198), f"Humidity  : {h_txt} (Target 46-52%)", fill=(220,220,220), font=_font(22))
	safety = _safety_state(temp, rh)
	col = {"SAFE":(40,180,60),"YELLOW":(220,180,30),"RED":(200,50,50)}[safety]
	d.text((bx+12,252), safety, fill=(0,0,0), font=_font(22))
	d.text((30, h-40), "Tap LIVE for camera . Tap SCAN to alalyze current view . Tap HIDE to return",
			fill=(180,180,180), font=_font(18))
	return img


# ------- ORB gallery --------

orb = cv2.ORB_create(nfeatures=1000)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

print("all imports donee")

def load_refs():
	gallery = []
	os.makedirs(REF_DIR, exist_ok=True)
	for fn in sorted(os.listdir(REF_DIR)):
		if fn.lower().endswith((".jpg",".jpeg",".png")):
			path = os.path.join(REF_DIR, fn)
			img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
			if img is None:
				continue
			kp, des = orb.detectAndCompute(img,None)
			gallery.append({"label": os.path.splitext(fn)[0], "img": img, "kp": kp, "des": des})
			
	return gallery
			
REFS = load_refs()
					
def orb_best_match(frame_bgr):
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
		best = [m for m in matches if m.distance < 60]
		score = len(best) / max(len(matches), 1)
		
		if score > best_score:
			best_score, best_label = score, r["label"]
	conf = round(float(best_score), 2)
	return (best_label, conf)
			
			

# -------- Tkinter App -------

class App:
	def __init__(self, root):
		self.root = root
		root.title("Smart Artifact Capsule")
		root.attributes("-fullscreen", True)
		root.configure(bg="black")
		
		# state
		self.photo = None
		self.mode = "idle"    # idle / live
		self.last_bgr = None
		self.picam2 = None
		self.cam_running = False
		self.cooling_on = False
		self.cooling_start_time = None
		
		
		try:
			self.picam2 = Picamera2()
			cfg = self.picam2.create_preview_configuration(main={"size": CAM_SIZE, "format":"RGB888"})
			self.picam2.configure(cfg)
		except Exception as e:
			print("Camera init failed:", e)
			self.picam2 = None
		
		
		self.video = tk.Label(root, bg="black")
		self.video.place(x=0, y=0, width=W, height=H-BAR_H)
		
		
		
		self.status = tk.Label(root, text="Ready . LIVE/SCAN",
						font=("Arial",16), bg="black", fg="white")
		self.status.place(x=10, y=H-130)
		
		
		
		
		bar = tk.Frame(root, bg="#111")
		bar.place(x=0, y=H-BAR_H, width=W, height=BAR_H)
		style = dict(font=("Arial",18,"bold"), bg="#2d6cdf", fg="white", bd=0, activebackground="#2552a3")

	
		bw = int(W/4)
		
		tk.Button(bar, text="LIVE",  command=self.on_live,  **style).place(x=10,   y=15, width=bw-20, height=70)
		tk.Button(bar, text="HIDE",  command=self.on_hide,  **style).place(x=1*bw+10,  y=15, width=bw-20, height=70) 
		tk.Button(bar, text="SCAN", command=self.on_scan,  **style).place(x=2*bw+10, y=15, width=bw-20, height=70)
		tk.Button(bar, text="QUIT", command=root.destroy, font=("Arial",18,"bold"),
				bg="#b02a37", fg="white", bd=0, activebackground="#7c1e28").place(x=3*bw+10, y=15, width = bw-20, height=70)
			
			
		self.update_screen()
		self.update_sensors()
		
#------ camera control
		
	def start_camera(self):
		if self.picam2 is None or self.cam_running:
			return
		try:
			self.picam2.start()
			self.cam_running = True
			time.sleep(0.1) # tiny warm up
			print("picam working")
		except Exception as e:
			print("start_camera error:", e)

		
	def stop_camera(self):
		if self.picam2 and self.cam_running:
			try: 
				self.picam2.stop()
			except Exception as e:
				print("stop_camera arror:", e)
		self.cam_running = False
	
	def close_camera(self):
		
		if self.picam2:
			try:
				if self.cam_running:
					self.picam2.stop()
				self.picam2.close()
			except Exception as e:
				print("close_camera error", e)
			self.picam2 = None	
		
	def grab_frame(self):
		if not (self.picam2 and self.cam_running):
			return None
		try:
			rgb = self.picam2.capture_array()     #RGB
			bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
			return rgb
		except Exception as e:
			print("grab_frame error:", e)
			return None
		
		
	# ----- UI Loop ------
	def update_screen(self):
		if self.mode == "live":
			bgr = self.grab_frame()
			if bgr is None:
				img = make_status_image(None, None)
			else:
				self.last_bgr = bgr
				disp = bgr.copy()
				cv2.rectangle(disp, (0,0), (W,40), (0,0,0), -1)
				cv2.putText(disp, "LIVE VIEW -- Tap SCAN to analyze . HIDE to return",
							(12,28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255),2, cv2.LINE_AA)
				img = Image.fromarray(cv2.cvtColor(disp, cv2.COLOR_BGR2RGB))
		elif self.mode == "result":
			img = self.result_image if self.result_image is not None else make_status_image(None, None)
		else:
			#idle
			t,h = read_dht()
			img = make_status_image(t,h)
				
		img = img.resize((W, H-BAR_H))
		self.photo = ImageTk.PhotoImage(img)
		self.video.configure(image=self.photo)
		self.root.after(50 if self.mode=="live" else 300, self.update_screen)

	def update_sensors(self):
		self.check_cooler_off()
		self.artifact_condition_check()
		self.root.after(250, self.update_sensors)
		
	# -------- buttons --------
	def on_live(self):
		self.mode = "live"
		self.start_camera()
		
	def on_hide(self):
		self.mode = "idle"
		self.stop_camera()
		#self.result_image = None
		
	def on_scan(self):
		"""
		Freeze the current view, run the prediction, and display the frozen frame with the prediction text **centered** on screen (no live feed).
		"""
		
		frame_bgr = None
		if self.mode == "live":
			frame_bgr = self.last_bgr if self.last_bgr is not None else self.grab_frame()
		else:
			
			self.start_camera()
			frame_bgr = self.grab_frame()
			self.stop_camera()
			
		if frame_bgr is None:
			#fallback to status
			self.mode = "idle"
			print("xxx: on scan no framee bgrr")
			return
			
			
		
		label, conf = orb_best_match(frame_bgr)
		print("xxx: on scan after orb best match label:%s, conf:%s", label, conf)
		
		disp = frame_bgr.copy()
		overlay = disp.copy()
		
		cv2.rectangle(overlay, (0,0), (W,40), (0,0,0), -1)
		alpha = 0.35
		disp = cv2.addWeighted(overlay, alpha, disp, 1-alpha, 0)
		
		
		text = f"{label} . conf {conf:.2f}"
		print("text: ", text)
		
		font = cv2.FONT_HERSHEY_SIMPLEX
		scale = 1.2
		thickness = 3
		(tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
		cx, cy = W//2, (H-BAR_H)//2
		org = (cx - tw//2, cy + th//2)
		
		cv2.putText(disp, text, org, font, scale, (0,0,0), thickness+3, cv2.LINE_AA)
		
		cv2.putText(disp, text, org, font, scale, (255,255,0), thickness, cv2.LINE_AA)
		
		print("xxx: on scan before printing banner")
		
		cv2.rectangle(disp, (0,0), (W,40), (0,0,0), -1)
		cv2.putText(disp, "SCAN RESULT -- Tap LIVE to resume camera . HIDE for status",
					(12,28), font, 0.8, (255,255,255), 2, cv2.LINEfrom_AA)
		print("xxx: on scan after putting on banner")			
					
		self.result_image = Image.fromarray(cv2.cvtColor(disp, cv2.COLOR_BGR2RGB))
		self.mode = "result"
		# ensure camera is off in result mode
		self.stop_camera()
		
	def draw(self, bgr, banner=None, foot=None):
		disp = bgr.copy()
		
		if banner:
			
			cv2.rectangle(disp, (0,0), (W,40), (0,0,0), -1)
			
			cv2.putText(disp, banner, (12,28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255),2, cv2.LINE_AA)
		if foot:
			cv2.rectangle(disp, (0,H-140), (W,H-100), (0,0,0), -1)
			cv2.putText(disp, foot, (12,H-110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0),2, cv2.LINE_AA)
		rgb = cv2.cvtColor(disp, cv2.COLOR_BGR2RGB)
		#img = Image.fromarray(rgb).resize((W, H-100))
		img = Image.fromarray(rgb).resize((W, H-BAR_H))
		self.photo = ImageTk.PhotoImage(img)
		self.video.configure(image=self.photo)
		
	def on_live(self):
		self.mode = "live"
		self.start_camera()
		#self.status.config(text="Live view")
		
		
	def on_freeze(self):
		self.mode = "frozen"
		self.status.config(text="Frozen frame")
		

	def artifact_condition_check(self):
			
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

			
			h,t = dht.read_retry(dht.DHT22, humidity_temp_sensor)
			print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))

			
			humidity = float("{0:0.1f}".format(h))
			temp = float("{0:0.1f}".format(t))

			
			if humidity > h_upper:
				rgb_led.color = Color("orange")
				print("Humidity levels are too high")
			elif humidity < h_lower:
				rgb_led.color = Color("blue")
				print("Humidity levels are too low")
			else:
				rgb_led.color = Color("green")

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
		if self.cooling_on:
			print("Peltier is currently cooling")
			return
		
		peltier_pin.on()
		self.cooling_on = True

		self.cooling_start_time = time.time()
		print("peltier turned on")

	def check_cooler_off(self):
		if self.cooling_on and self.cooling_start_time != None:
			if time.time() - self.cooling_start_time >= 20.0:
				peltier_pin.off()
				self.cooling_on = False
				self.cooling_start_time = None
				print("Peltier turned off")
		
		

	
if __name__ == "__main__":
	print("starting main")
	root = tk.Tk()
	root.geometry(f"{W}x{H}+0+0")
	
	try:
		app = App(root)
		root.mainloop()
		
	finally:
		app.close_camera()
