from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Button, Color, Stop
from pybricks.tools import wait, StopWatch, Matrix
from pybricks.robotics import DriveBase
#from mh_media import MY_ICONS
from utils.mh_port_debug import PortDebug
from umath import pi

class Robot:
    # Import functions for Robot Class
  

    def __init__(self, CONFIG):
        self.config = CONFIG
        ## Print which motor or sensor is on each port
        if(self.config['debug']):
            PortDebug()

   
        
        from pybricks.hubs import PrimeHub
        self.hub = PrimeHub()


        self.hub.system.set_stop_button(Button.BLUETOOTH)
        self.matrix = self.display = self.hub.display
        self.speaker = self.hub.speaker
        self.speaker.volume(40)
        self.gyro = self.imu = self.hub.imu
        self.light = self.hub.light
        self.buttons = self.hub.buttons
        self.timer = StopWatch()

        # Assign Movement Motors
        self.L_Motor = Motor(self.config['drive']['left'][0],positive_direction=self.config['drive']['left'][1],gears=self.config['drive']['left'][2])
        self.R_Motor = Motor(self.config['drive']['right'][0],positive_direction=self.config['drive']['right'][1],gears=self.config['drive']['right'][2])
        self.Drive= DriveBase(self.L_Motor,self.R_Motor,self.config['drive']['diameter'],self.config['drive']['width'])
        self.Drive.use_gyro(True)
        #while not self.gyro.ready():
        #    wait(100)

        self.chassisAngle = self.gyro.heading()
        self.Left_attach=Motor(self.config['attach']['left'][0], gears=self.config['attach']['left'][1])
        self.Right_attach=Motor(self.config['attach']['right'][0], gears=self.config['attach']['right'][1])


        # Configure Color Sensors
        if (self.config['line']['enable']):
            self.leftColor = ColorSensor(self.config['line']['left'])
            self.rightColor = ColorSensor(self.config['line']['right'])
            self.reflectSensor = self.leftColor
            self.lineSensor = self.rightColor

    async def cancelRun(self):
        #When Center button pessed, Stop Run by exiting race
        while not Button.CENTER in self.buttons.pressed():
            await wait(50)
        
        self.Drive.stop()
        self.Right_attach.stop()
        self.Left_attach.stop()
