from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt

async def run_remote(robot):
    print("Starting Run: " + __name__)
    await robot.SwerveStart(True)
    await robot.SwerveRemote()
