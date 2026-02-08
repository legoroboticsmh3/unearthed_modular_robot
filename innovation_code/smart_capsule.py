# smart_capsule.py -- Touch UI + Live + Scan (ORB) for 800x480 screen

import os, time, cv2, numpy as np
import tkinter as tk
import tflite_runtime.interpreter as tflite

from PIL import Image, ImageTk, ImageDraw, ImageFont

import Adafruit_DHT as dht
import time
from gpiozero import InputDevice, OutputDevice, RGBLED
from colorzero import Color

import threading

def load_labels(path):
	labels = []
	with open(path, "r") as f:
		for line in f:
			line = line.strip()
			if not line:
				continue
			parts = line.split(" ", 1) # "0 Ceramic"
			labels.append(parts[1] if len(parts) == 2 else parts[0])
		return labels
	

class TFLitePredicter:
	def _init_(self, model_path, labels_path):
		self.labels = load_labels(labels_path)
		self.interpreter = tflite.Interpreter(model_path=model_path, num_threads=2)
		self.interpreter.allocate_tensors()
		self.inp = self.interpreter.get_input_details()[0]
		self.out = self.interpreter.get_output_details()[0]
		
		shape = self.inp["shape"] # [1, H, W, 3]
		self.h, self.w = int(shape[1]), int(shape[2])
		self.dtype = self.inp["dtype"] # float32 or uint8
    
	def predict(self, frame_brg):
		rgb = cv2,cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
		resized = cv2.resize(rgb, (self.w, self.h), interpolation=cv2.INTER_AREA)
	
		if self.dtype == np.float32:
			x = resized.astype(np.float32) / 255.0	
		else:
			x = resized.astype(np.uint8)

		x = np.expand+dims(x, axis=0)
		self.interpreter.set_tensor(self.inp["index"], x)
		self.interpreter.invoke()
		y = self.interpreter.get_tensor(self.out["index"])[0]


		idx = int(np.argmax(y))
		conf = float(y[idx])
		label = self.label[idx] if idx < len(self.labels) else f"class_{idx}"
		return label, conf


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
#CAM_SIZE = (680, 400)
CAM_SIZE = (800, 480)
LOGO_PATH = "sac_logo.png"


REF_DIR = "/home/pi/Robotics/FLLRobotics/refs"

def read_dht():
	#Read Temp and Humidity from DHT22
	humidity_temp_sensor = 4

	h,t = dht.read_retry(dht.DHT22, humidity_temp_sensor)
	#h,t = dht.read(dht.DHT22, humidity_temp_sensor)
	print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))

	#Formatting data into readable numbers
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
	
	#logo
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
		#mean_dist = np.mean([m.distance for m in matches])
		#score = 1.0 / (1.0 + mean_dist)  #higher better
		best = [m for m in matches if m.distance < 60]
		score = len(best) / max(len(matches), 1)
		
		if score > best_score:
			best_score, best_label = score, r["label"]
	#conf = min(max(best_score * 3.5, 0.0), 0.99)
	#return (best_label, float(conf))
	conf = round(float(best_score), 2)
	return (best_label, conf)
			
			
			
# --------- Camera ---------
"""
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": CAM_SIZE, "format":"RGB888"})
picam2.configure(config)
picam2.start()  # start once so Live appears instantly

"""

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

		#Initialize sensors once
		try:
			self.vibration_sensor = InputDevice(17)
			red_pin = 10
			green_pin = 9
			blue_pin = 11

			self.rgb_led = RGBLED(red_pin, green_pin, blue_pin, active_high=False)
			self.humidity_temp_sensor = 4
		except Exception as e:
			print(f"Sensor initialization error: {e}")
			self.rgb_led = None
			self.vibration_sensor = None

		# Cache sensor readings
		self.last_temp = None
		self.last_humidity = None
		self.last_sensor_read_time = 0
		self.sensor_read_interval = 2.0

		# create camera once and configure once
		try:
			self.picam2 = Picamera2()
			cfg = self.picam2.create_preview_configuration(main={"size": CAM_SIZE, "format":"RGB888"})
			self.picam2.configure(cfg)
		except Exception as e:
			print("Camera init failed:", e)
			self.picam2 = None
		
		# video area
		self.video = tk.Label(root, bg="black")
		self.video.place(x=0, y=0, width=W, height=H-BAR_H)
		
		
		# status text
		self.status = tk.Label(root, text="Ready . LIVE/SCAN",
						font=("Arial",16), bg="black", fg="white")
		self.status.place(x=10, y=H-130)
		
		
		# control bar
		
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
		
        #tflite ml setup
		self.ml = None
		try:
			self.ml = TFLitePredictor(model_path="", labels_path="ml/labels.txt")
			print("xxx: TFLite model loaded")
		except Exception as e:
			print("xxx: Failed to load TFLITE model:", e)
			self.ml = None
		
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
		#Call this only when existing app
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
			# Show frozen result image (already rendered with centered text)
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
		self.root.after(500, self.update_sensors)
		
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
		# Ensure we have a frame: if not in live, briefly start camera, grab one, stop
		frame_bgr = None
		if self.mode == "live":
			frame_bgr = self.last_bgr if self.last_bgr is not None else self.grab_frame()
		else:
			# grab a quick snapshot without going fully live
			self.start_camera()
			frame_bgr = self.grab_frame()
			self.stop_camera()
			
		if frame_bgr is None:
			#fallback to status
			self.mode = "idle"
			print("xxx: on scan no framee bgrr")
			return
			
			
		# TFLite prediction
		label, conf = orb_best_match(frame_bgr)
		print("xxx: on scan after orb best match label:%s, conf:%s", label, conf)
		#build frozen result frame with centered text
		disp = frame_bgr.copy()
		overlay = disp.copy()
		#darken top/bottom hands slightly to improve text legibility
		cv2.rectangle(overlay, (0,0), (W,40), (0,0,0), -1)
		alpha = 0.35
		disp = cv2.addWeighted(overlay, alpha, disp, 1-alpha, 0)
		
		#Centered multi-line text with outline
		text = f"{label} . conf {conf:.2f}"
		# print("text: ", text)
		# #compute text size
		font = cv2.FONT_HERSHEY_SIMPLEX
		scale = 1.2
		thickness = 3
		(tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
		cx, cy = W//2, (H-BAR_H)//2
		org = (cx - tw//2, cy + th//2)

		if conf < 0.60 and label not in ("ML not loaded", "Predict error"):
			lines = [f"Uncertain", f"Top: {label}", f"Conf: {conf*100:.0f}%"]
		else:
			lines = [f"{label}", f"Conf: {conf*100:.0f}%"]
	    
        #compute total hieght for centering
		line_gap = 18
		sizes = [cv2.getTextSize(line, font, scale, thickness)[0] for line in lines]
		total_h = sum(h for (w,h) in sizes) + line_gap * (len(lines) - 1)
		y = cy - total_h // 2
	
		for i, line in enumerate(lines):
			(tw, th) = sizes[i]
			x = cx - tw // 2
			y = y + th 
            #outline
			cv2.putText(disp, text, org, font, scale, (0,0,0), thickness+3, cv2.LINE_AA)
		    #fill
			cv2.putText(disp, text, org, font, scale, (255,255,0), thickness, cv2.LINE_AA)
			y = y + line_gap
	    
		
		print("xxx: on scan before printing banner")
		#top banner
		cv2.rectangle(disp, (0,0), (W,40), (0,0,0), -1)
		cv2.putText(disp, "SCAN RESULT -- Tap LIVE to resume camera . HIDE for status",
					(12,28), font, 0.8, (255,255,255), 2, cv2.LINE_AA)
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
		
	"""	
	def on_scan(self):
		if self.last_bgr is None:
			self.status.config(text="No frame yet --- tap LIVE first")
			return
		label, conf = orb_best_match(self.last_bgr)
		self.status.config(text=f"Prediction:{label}  ({conf:.2f})")
		self.draw(self.last_bgr, banner="SCAN RESULT", foot=f"{label} . conf{conf:.2f}")
	"""

	def artifact_condition_check(self):
			#Thresholds for humidity and temp
			h_upper = 70
			h_lower = 55
			t_upper = 26
			t_lower = 20

			current_time = time.time()
			if current_time - self.last_sensor_read_time >= self.sensor_read_interval:
				try:
					if self.vibration_sensor and self.vibration_sensor.is_active:
						if self.rgb_led:
							self.rgb_led.color = Color("white")
						print("Vibration detected!")
						self.last_sensor_read_time = current_time
						return

					#Read Temp and Humidity from DHT22
					h,t = dht.read(dht.DHT22, self.humidity_temp_sensor)

					if h is not None and t is not None:


						#h,t = dht.read(dht.DHT22, humidity_temp_sensor)
						print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))

						#Formatting data into readable numbers
						humidity = float("{0:0.1f}".format(h))
						temp = float("{0:0.1f}".format(t))

						self.last_temp = temp
						self.last_humidity = humidity
						self.last_sensor_read_time = current_time

					if self.rgb_led is not None:
						#Checks if humudity or temperature is too high or low
						if humidity > h_upper:
							self.rgb_led.color = Color("red")
							print("Humidity levels are too high")
						elif humidity < h_lower:
							self.rgb_led.color = Color("blue")
							print("Humidity levels are too low")
						else:
							self.rgb_led.color = Color("green")

						if temp > t_upper:
							self.rgb_led.color = Color("purple")
							print(f"Temperature levels are too high, temp: {temp}")
							self.trigger_cooling()
						elif temp < t_lower:
							self.rgb_led.color = Color("yellow")
							print("Temperature levels are too low")
						else:
							self.rgb_led.color = Color("green")
				except Exception as e:
					print(f"artifact_condition_check() - Sensor Reading error: {e}")
					self.last_sensor_read_time = current_time

	def trigger_cooling(self):
		#peltier_pin = OutputDevice(21)

		if self.cooling_on:
			print("Peltier is currently cooling")
			return
		
		peltier_pin.on()
		self.cooling_on = True

		self.cooling_start_time = time.time()
		print("peltier turned on")

	def check_cooler_off(self):
		if self.cooling_on and self.cooling_start_time is not None:
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









import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path="/home/pi/Robotics/FLLRobotics/model.tflite")
interpreter.allocate_tensors()

print("medels loaded successfully")
print(f"input: {interpreter.get_input_details()}")
print(f"output: {interpreter.get_output_details()}")