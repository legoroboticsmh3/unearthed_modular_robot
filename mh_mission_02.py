from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
L_motor=Motor(Port.F,Direction.CLOCKWISE, gears=[28,20])
R_motor=Motor(Port.E,Direction.COUNTERCLOCKWISE, gears=[28,20])
#Left_attach=Motor(Port.C)
#Right_attach=Motor(Port.D)
Drive=DriveBase(L_motor, R_motor, 62.4, 110)
Drive.use_gyro(True)
Drive.straight(675)
Drive.turn(-45)
Drive.straight(230)
R_attach=Motor(Port.B)
R_attach.run_angle(500,90)
#wait(850)
Drive.straight(-200)
Drive.turn(45)
Drive.straight(-670)

Drive.straight(180)
Drive.turn(90)
Drive.straight(500)
Drive.straight(-500)