from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt

async def run_9(robot):
    print("Starting Run: " + __name__)
    robot.Drive.settings(straight_speed=500)
    robot.Left_attach.dc(10)
    await wait(300)
    robot.Left_attach.stop()

    #F
    await robot.Drive.straight(970)
    robot.Drive.settings(turn_rate=75)

    await robot.Drive.turn(90)
    await robot.Drive.turn(-.5)
    await wait(200)
    await robot.Left_attach.run_angle(240,69)
    await wait(300)
    robot.Drive.settings(straight_speed=70)
    await robot.Drive.straight(150)
    wait(500)
    await robot.Left_attach.run_angle(240,5)
    await wait(200)
    await robot.Left_attach.run_angle(240,-8) #lifting up artifact
    await wait(200)
    await robot.Drive.straight(-150)
    wait(200)
    robot.Drive.settings(straight_speed=500)
    robot.Drive.settings(turn_rate=100)
    await robot.Drive.turn(90)
    await robot.Left_attach.run_angle(100,-67.5)
    await robot.Drive.straight(900)