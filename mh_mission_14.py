from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt


async def run_9(robot):
    print("Starting Run: " + __name__)
    robot.Drive.settings(straight_speed=600)

    await robot.Drive.straight(300)
    await robot.Drive.turn(50)
    await robot.Drive.straight(220)
    await robot.Drive.straight(-450)