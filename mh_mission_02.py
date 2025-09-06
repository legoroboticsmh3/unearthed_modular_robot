from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
L_motor=Motor(Port.F,Direction.CLOCKWISE)
R_motor=Motor(Port.E,Direction.COUNTERCLOCKWISE)
#Left_attach=Motor(Port.C)
#Right_attach=Motor(Port.D)
Drive=DriveBase(L_motor, R_motor, 35, 150)
Drive.straight(275)
Drive.turn(-15)
Drive.straight(90)
R_attach=Motor(Port.B)
R_attach.run_angle(500,90)
wait(850)
Drive.straight(-90)
Drive.turn(15)
Drive.straight(-280)
    