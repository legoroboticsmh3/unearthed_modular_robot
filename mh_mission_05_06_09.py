from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

R_Motor = Motor(Port.E,positive_direction=Direction.COUNTERCLOCKWISE, gears=[28, 20])
L_Motor = Motor(Port.F,positive_direction=Direction.CLOCKWISE, gears=[28, 20])
Drive= DriveBase(L_Motor,R_Motor,62.4,110)
Drive.use_gyro(True)
Drive.settings(turn_rate=160)
# Attach_Right=Motor(Port.D)
# Attach_Left=Motor(Port.C)
Drive.straight(680)
Drive.turn(49)
Drive.straight(35)
Drive.settings(turn_rate=75)
Drive.turn(-39)
Drive.settings(turn_rate=160)
Drive.straight(50)
Drive.turn(-96)
Drive.straight(-260)
# Drive.straight(590)
Drive.straight(200)
Drive.turn(8)
Drive.straight(390)
Drive.turn(38)
Drive.straight(-200)