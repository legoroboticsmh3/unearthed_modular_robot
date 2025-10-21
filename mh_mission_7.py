from pybricks.tools import wait
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from urandom import randint
from umath import pi, sqrt

async def run_2(robot):
    robot.Right_attach.run_angle(100,-90*-1,then=Stop.HOLD)
    robot.Drive.settings(straight_speed=500)
    robot.Drive.settings(turn_rate=75)
    await robot.Drive.straight(795)
    await robot.Drive.turn(43)
    await robot.Drive.straight(-40)
    await robot.Drive.straight(45)
    await robot.Right_attach.run_angle(200,80*-1)
    robot.Drive.settings(straight_speed=200)
    await robot.Drive.straight(63)
    await robot.Right_attach.run_angle(180,-75*-1)
    await robot.Drive.turn(-44)
    robot.Drive.settings(straight_speed=500)
    robot.Drive.settings(turn_rate=160)
    await robot.Drive.straight(-813)
