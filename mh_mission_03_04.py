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
Left_attach.run_angle(200, -15)
Drive.straight(-980)
Drive.turn(-91)
Left_attach.run_angle(240,112.6)
Drive.settings(straight_speed=50)
Drive.straight(122)
Left_attach.run_angle(200, -12)
wait(500)
Drive.straight(-147)
Drive.settings(straight_speed=200)
Drive.turn(90)
Drive.straight(1300)
wait(100)
#left_attach.run_angle(500, -90) 
wait(600)
Left_attach.run_angle(500, 100 )
