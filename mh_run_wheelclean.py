from pybricks.tools import wait
from pybricks.parameters import Button, Color
from urandom import randint
from umath import pi, sqrt

#Working
#Blue Side - Collection blue, Plankton Sample
async def wheelclean(robot):
    print("Starting Run: " + __name__)
    await robot.SwerveStart(True)
    while True:
        await robot.SwerveMove(speed=35, amount=10, unit='cm')