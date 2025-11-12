from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt


async def run_13(robot):
    print("Starting Run: " + __name__)

    # await robot.Drive.settings(turn_rate=70)
    await robot.Drive.straight(-30)
    await robot.Drive.turn(-67.5)
    await robot.Drive.straight(-940)
    await wait(500)
    await robot.Drive.straight(965)