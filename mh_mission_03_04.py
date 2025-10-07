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

# THE RED NEXT TO THE LINE NUMBER MEANS IT HAS TO BE CHANGED IF NOT THERE EVERYTHING IS FINE TO REMOVE IT PRESS IT.
Drive.use_gyro(True)
Left_attach.run_angle(200, -15)
#tuoched the wall and turned to face the model
Drive.straight(-980)
Drive.turn(-91)
#put down the attachment to grab the model
Right_attach.run_angle(150,100)
Left_attach.run_angle(240,117.6)
Drive.settings(straight_speed=50)
Drive.straight(122)
Left_attach.run_angle(200,-12)
wait(500)
Right_attach.run_angle(100,-130)
Drive.straight(-145)
Drive.settings(straight_speed=500)
Drive.turn(90)
#grabbed the model 
wait(500)
#goes to the mission 13
Drive.turn(-48)
Left_attach.run_angle(500, 80)
Drive.settings(straight_speed=100)
Drive.straight(364.5)
Drive.settings(straight_speed=1000)
Left_attach.dc(-9000)
wait(600) 
#missions completed