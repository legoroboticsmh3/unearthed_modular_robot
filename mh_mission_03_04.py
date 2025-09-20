from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch


hub = PrimeHub()
R_motor=Motor(Port.E,Direction.COUNTERCLOCKWISE, gears=[28,20])
L_motor=Motor(Port.F,Direction.CLOCKWISE, gears=[28,20])
Left_attach=Motor(Port.A)
Right_attach=Motor(Port.B)
Drive=DriveBase(L_motor, R_motor, 62.4, 110)

Drive.use_gyro(True)
Drive.straight(-1000)
Drive.turn(-90)
Right_attach.run_angle(500, 90)
Drive.straight(250)
Right_attach.run_angle(500, 90)
Drive.settings(straight_speed=10)
Drive.straight(-250)