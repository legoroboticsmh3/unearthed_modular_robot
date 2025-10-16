from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch


hub = PrimeHub()
R_motor=Motor(Port.E,Direction.COUNTERCLOCKWISE, gears=[28,20])
L_motor=Motor(Port.F,Direction.CLOCKWISE, gears=[28,20])
Left_attach=Motor(Port.A, gears=[28, 36])
Right_attach=Motor(Port.B, gears=[28, 36])
Drive=DriveBase(L_motor, R_motor, 62.4, 110)

Drive.use_gyro(True)
Left_attach.run_angle(200, 45)
Left_attach.run_angle(200, -31.5)
Drive.straight(-980)
Drive.turn(-91)
Right_attach.run_angle(150,100)
Left_attach.run_angle(240,117.6)
Drive.settings(straight_speed=50)
Drive.straight(122)
Left_attach.run_angle(200,-14)
wait(500)
Right_attach.run_angle(100,-100)
Drive.straight(-145)
Drive.settings(straight_speed=500)
Drive.turn(90)
wait(500)
Drive.turn(-45)
Left_attach.run_angle(500,40)
Drive.settings(straight_speed=120)
Drive.straight(377.5)
Drive.settings(straight_speed=41)
Left_attach.dc(-64)
wait(600) 
Drive.settings(straight_speed=250)
Drive.straight(-364.5)
Drive.turn(45)
Drive.straight(974)
