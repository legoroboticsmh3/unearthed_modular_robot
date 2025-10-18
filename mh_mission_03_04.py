from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt

async def run_5(robot):
    print("Starting Run: " + __name__)
    robot.Drive.settings(straight_speed=500)
    await robot.Left_attach.run_angle(200, 45)
    await robot.Left_attach.run_angle(200, -45)
    await robot.Drive.straight(-970)
    await robot.Drive.turn(-91)
    await robot.Right_attach.run_angle(150,-100)
    await robot.Left_attach.run_angle(240,117.6)
    robot.Drive.settings(straight_speed=50)
    await robot.Drive.straight(122)
    await robot.Left_attach.run_angle(200,-14)
    await wait(500)
    await robot.Right_attach.run_angle(100,100)
    await robot.Drive.straight(-145)
    robot.Drive.settings(straight_speed=500)
    await robot.Drive.turn(90)
    await wait(500)
    await robot.Drive.turn(-45)
    await robot.Left_attach.run_angle(500,40)
    robot.Drive.settings(straight_speed=120)
    await robot.Drive.straight(390.5)
    robot.Drive.settings(straight_speed=41)
    robot.Left_attach.dc(-95)
    await wait(600) 
    robot.Drive.settings(straight_speed=250)
    await robot.Drive.straight(-364.5)
    await robot.Drive.turn(45)
    await robot.Drive.straight(974)
