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

Drive.turn(17)
Drive.straight(-700)
Drive.turn(73)
Drive.straight(-70) 
Drive.straight(70)
Drive.turn(-73) 
Drive.straight(680)