from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

R_Motor = Motor(Port.E,positive_direction=Direction.COUNTERCLOCKWISE, gears=[28, 20])
L_Motor = Motor(Port.F,positive_direction=Direction.CLOCKWISE, gears=[28, 20])
Left_attach=Motor(Port.A, gears=[28, 36])
Right_attach=Motor(Port.B, gears=[28, 36])
Drive= DriveBase(L_Motor,R_Motor,62.4,110)
Drive.use_gyro(True)

Drive.straight(770)
Drive.turn(40)
Drive.straight(-27)
Right_attach.run_angle(250,65)
Drive.straight(50)
Right_attach.run_angle(250,-80)
Drive.turn(-40)
Drive.settings(straight_speed=1300)
Drive.straight(-770)
