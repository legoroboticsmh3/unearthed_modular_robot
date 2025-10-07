from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch


#these are all the default setings for the robot
hub = PrimeHub()
R_motor=Motor(Port.E,Direction.COUNTERCLOCKWISE, gears=[28,20])
L_motor=Motor(Port.F,Direction.CLOCKWISE, gears=[28,20])
Left_attach=Motor(Port.A, gears=[28, 36])
Right_attach=Motor(Port.B,)
Drive=DriveBase(L_motor, R_motor, 62.4, 110)

#going to the mission model mission 3

Drive.use_gyro(True)
Drive.straight(550)
Right_attach.run_angle(200, 130)
Drive.straight(-200)
Right_attach.run_angle(200, -130)
Drive.turn(-90)
Drive.straight(180)
Drive.turn(90)
Right_attach.run_angle(200, 130)
Drive.straight(300)
Drive.straight(-350)