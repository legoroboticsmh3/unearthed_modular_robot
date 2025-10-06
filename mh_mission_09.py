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

Drive.straight(-771)
Drive.turn(-90)
Drive.straight(-480)
Drive.turn(-129)
Drive.straight(-290)
Drive.straight(290)
Drive.turn(-45)