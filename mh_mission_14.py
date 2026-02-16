from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt


async def run_7(robot):
    print("Starting Run: " + __name__)
    robot.Drive.settings(straight_speed=600)

    await robot.Drive.straight(-400-100)
    await robot.Drive.straight(500)