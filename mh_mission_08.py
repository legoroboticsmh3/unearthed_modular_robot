from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt


async def run_8(robot):
    print("Starting Run: " + __name__)
    
    robot.Drive.settings(turn_rate=160)

    await robot.Drive.straight(200)
    await robot.Drive.turn(45)
    await robot.Drive.straight(85)
    await robot.Drive.turn(-45)
    await robot.Drive.straight(170)
    
    
    
    #await robot.Drive.straight(430) #original distance for starting point at 7Beam
    print(robot.gyro.heading())
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,85) #hammer  up
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,85) #hammer up
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,120) #hammer up
    #await robot.Right_attach.run_angle(500,-100) #hammer down 4th time
    #await robot.Right_attach.run_angle(500,85) #hammer up
    await robot.Drive.straight(-120)
    await robot.Drive.turn(-15)
    await robot.Drive.straight(210)
    await robot.Drive.turn(-105)
    await robot.Right_attach.run_angle(200,-100)
    await robot.Drive.straight(40)
    await robot.Right_attach.run_angle(500,100)
    await robot.Drive.straight(-60)
    await robot.Drive.turn(-90)
    await robot.Drive.straight(270)



