from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt


async def run_1(robot):
    print("Starting Run: " + __name__)

    await robot.Drive.straight(-750)
    print("2nd line Run: " + __name__)
    await robot.Drive.turn(-90)
    await robot.Drive.straight(-510)
    await robot.Drive.turn(-143)
    await robot.Drive.straight(-130)
    print("Stopping Run: " + __name__)