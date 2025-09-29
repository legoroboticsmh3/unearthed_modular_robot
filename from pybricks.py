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


Drive.straight(700)
Drive.turn(45)
Right_attach.run_angle(200, 150)
Drive.straight(20)
