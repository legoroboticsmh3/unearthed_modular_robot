from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt


async def run_3(robot):
    print("Starting Run: " + __name__)

    robot.Drive.settings(turn_rate=160)
    # Attach_Right=Motor(Port.D)
    # Attach_Left=Motor(Port.C)
    #Drive.straight(680)  #this is the distance for the original wihout the mission 9 back attachment
    robot.Drive.settings(straight_speed=500)
    await robot.Drive.straight(196)  
    await robot.Drive.turn(90)

    await robot.Drive.straight(510)
    await robot.Drive.turn(49)
    await robot.Drive.straight(49)
    robot.Drive.settings(turn_rate=75)   #to get the boulders down 
    await robot.Drive.turn(-39)        #to get the boulders down Mission number 6
    robot.Drive.settings(turn_rate=160)
    await robot.Drive.straight(55)
    await robot.Drive.turn(-95)     #mission number 5
    await robot.Drive.straight(-260) 
    await robot.Drive.straight(180)  #push the boulders back
    # robot.Drive.straight(590)
    await robot.Drive.straight(200)
    await robot.Drive.turn(12)
    await robot.Drive.straight(500)
    await robot.Drive.turn(35)
    robot.Drive.settings(straight_speed=500)
    await robot.Drive.straight(-370)
    await robot.Drive.straight(230)
    await robot.Drive.turn(-60)
    await robot.Drive.straight(890)
    await robot.Drive.turn(-75)
    await robot.Drive.straight(640)
    #1000, 640