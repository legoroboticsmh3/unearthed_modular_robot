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

Drive.settings(turn_rate=160)
# Attach_Right=Motor(Port.D)
# Attach_Left=Motor(Port.C)
Drive.straight(680)  
Drive.turn(49)
Drive.straight(35)
Drive.settings(turn_rate=75)   #to get the boulders down 
Drive.turn(-39)        #to get the boulders down Mission number 6
Drive.settings(turn_rate=160)
Drive.straight(50)
Drive.turn(-98)     #mission number 5
Drive.straight(-260)   #push the boulders back
# Drive.straight(590)
Drive.straight(200)
Drive.turn(8)
Drive.straight(410)
Drive.turn(35)
Drive.settings(straight_speed=800)
Drive.straight(-250)
wait(1000)
Drive.straight(200)



#Drive.settings(straight_speed=200)

#Drive.straight(-220)
#Drive.turn(10)
#Drive.straight(-20)
#wait(2000)
#Drive.stop()

#Drive.turn(-15)
#Drive.straight(100, then=Stop.Hold)
#Drive.straight(-10)
#wait(1000)
#Drive.straight(50)
#Drive.turn(15)


