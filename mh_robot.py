from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Button, Color, Stop
from pybricks.tools import wait, StopWatch, Matrix
from mh_media import MY_ICONS
from mh_port_debug import PortDebug
from umath import pi

class Robot:
    # Import functions for Robot Class
    from mh_robot_misc import FixNone, WaitButton, GetTurnAngle, TurnSwerveWheel, TurnSwerveWheels, moveAttachment, cancelRun, CounterTurnWheel, CounterCalculate
    from mh_swerve_robot_drive import SwerveDrive, SwerveTurn, SwerveMove, SwerveStart, SwerveStop, setDirection, setDirectionCorrection, closest_rotation
    from mh_robot_remote import SwerveRemote, ConnectRemote
    from mh_robot_condition import StopConditionCheck, StopConditionSet

    def __init__(self, CONFIG):
        self.config = CONFIG
        ## Print which motor or sensor is on each port
        if(self.config['debug']):
            PortDebug()

        # Initialize Hub & Remap objects to self for ease of use
        if (self.config['hub'] == 'technic'):
            from pybricks.hubs import TechnicHub
            self.hub = TechnicHub()
            # Disable the stop button.
            self.hub.system.set_stop_button(None)
        else:
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


        # Assign Swerve Drive/Movement Motors
        self.leftDrive = Motor(self.config['drive']['left'][0],self.config['drive']['left'][1])
        self.rightDrive = Motor(self.config['drive']['right'][0],self.config['drive']['right'][1])

        # Drive/Movement Motor Speeds & Overrides
        self.driveSpeed = 0     # 0% Speed
        self.reverseWheels = 1  # 1 = forward, -1 = reverse
        #self.reverseLeftWheel = 1  # 1 = forward, -1 = reverse
        #print(self.leftDrive.control.limits())
        #print(self.rightDrive.control.limits())
        #self.leftDrive.control.limits(1200,2000,199) # Spike Prime Motor
        #self.rightDrive.control.limits(1200,2000,199) # Spike Prime Motor
        self.leftDrive.control.limits(1600,2300,280) # Powered Up Motors
        self.rightDrive.control.limits(1600,2300,280) # Powered Up Motors

        # Turn/Wheel Angle Motors
        self.leftTurnOffset = 0
        self.runAttachment = True # Set to True to disable swerve
        self.leftTurn = Motor(self.config['turn']['left'][0],self.config['turn']['left'][1], self.config['turn']['left'][2])
        self.rightTurn = Motor(self.config['turn']['right'][0],self.config['turn']['right'][1],self.config['turn']['right'][2])

        # [Wheel Calibration Output]
        # Before starting program, point wheels straight forward
        # Run Program Once, read the out put and enter number in
        # [turn][leftZero] and [turn][rightZero] config file.
        print("leftAbsAngle",self.leftTurn.angle() % 360)
        print("rightAbsAngle",self.rightTurn.angle() % 360)

        #Calculate wheel circumference as well as off center distance per 360 degree wheel module turn
        self.config['drive']['circumference'] = self.config['drive']['diameter']*self.config['drive']['gearRatio']*pi
        self.config['drive']['offCenter_circumference'] = self.config['drive']['offCenter'] * 2 * pi

        # Configure XBox Controller (If Enabled in Config)
        self.ConnectRemote()

        # Point turn motor to zero angle.  Allow user to rotate until wheel is pointing forward
        # FIXED: run_taget is currently spinning wheel ~360 degrees clockwise rather than finding the shortest path
        leftZero = self.config['turn']['leftZero'] if self.config['turn']['leftZero'] < 180 else self.config['turn']['leftZero'] - 360
        rightZero = self.config['turn']['rightZero'] if self.config['turn']['rightZero'] < 180 else self.config['turn']['rightZero'] - 360
        self.leftTurn.run_target(500, leftZero, then=Stop.HOLD, wait=True)
        self.rightTurn.run_target(500, rightZero, then=Stop.HOLD, wait=True)
        calibratePrompt = self.timer.time()
        if (self.config['hub'] == 'technic'):
            while not any(self.buttons.pressed()) and self.timer.time()- calibratePrompt < (20*1000):
                #self.leftTurn.run_angle(500, 120, then=Stop.HOLD, wait=True)
                self.TurnSwerveWheel('right', '120',1600)
                wait(1000)
            wait(1000)
            while not any(self.buttons.pressed()) and self.timer.time()- calibratePrompt < (20*1000):
                #self.rightTurn.run_angle(500, 120, then=Stop.HOLD, wait=True)
                self.TurnSwerveWheel('left', '120',1600)
                wait(1000)
            self.light.on(Color.ORANGE)
            wait(3000)
        else: #Spike Prime Wheel Angle Menu
            self.matrix.icon(Matrix(MY_ICONS['HAMMER']))
            while not any(self.buttons.pressed()) and self.timer.time()- calibratePrompt < (8*1000):
                wait(10)
            if any(self.buttons.pressed()):
                lastPressed = [] #Used for Button Release Detection
                while Button.CENTER not in lastPressed:
                    pressed = self.buttons.pressed()

                    #When Left Button is Released
                    if Button.LEFT in lastPressed and Button.LEFT not in pressed:
                        self.leftTurn.run_angle(500, 120, then=Stop.HOLD, wait=True)
                    #When Right Button is Released
                    if Button.RIGHT in lastPressed and Button.RIGHT not in pressed:
                        self.rightTurn.run_angle(500, 120, then=Stop.HOLD, wait=True)

                    lastPressed = pressed # Used for Button Release Detection
                    wait(50)

        wait(300)
        #Set Current Angle as Straight Forward
        self.wheelAngle = 0
        self.rightTurn.reset_angle(self.wheelAngle)
        self.leftTurn.reset_angle(self.wheelAngle)
        while not self.gyro.ready():
            wait(100)
        self.chassisAngle = self.gyro.heading()

        if (self.config['hub'] == 'technic'):
            # Enable the stop button again.
            self.hub.system.set_stop_button(Button.CENTER)

        # Configure Color Sensors
        if (self.config['line']['enable']):
            self.leftColor = ColorSensor(self.config['line']['left'])
            self.rightColor = ColorSensor(self.config['line']['right'])
            self.reflectSensor = self.leftColor
            self.lineSensor = self.rightColor
