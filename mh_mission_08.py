from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt


async def run_8(robot):
    print("Starting Run: " + __name__)

    robot.Drive.settings(turn_rate=160)

    await robot.Drive.straight(430)
    
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,85) #hammer  up
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,85) #hammer up
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,120) #hammer up
    await robot.Right_attach.run_angle(500,-100) #hammer down 4th time
    await robot.Right_attach.run_angle(500,85) #hammer up
    await robot.Drive.straight(-430) #drive back
