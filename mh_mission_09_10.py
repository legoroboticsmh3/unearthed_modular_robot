from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch



async def run_5(robot):
    print("Starting Run: " + __name__)

    robot.Drive.settings(turn_rate=160)
    robot.Drive.settings(straight_speed=500)
    # Mission 10 Code
    await robot.Drive.straight(-210)
    await robot.Drive.turn(-90)
    await robot.Drive.straight(-620)
    await robot.Drive.turn(90)
    robot.Drive.settings(straight_speed=300)
    await robot.Drive.straight(-100)
    robot.Drive.settings(straight_speed=500)
    await wait(1000)
    await robot.Drive.straight(90)
    await robot.Drive.turn(-73) 
    await robot.Drive.straight(750)

    '''
    await robot.Drive.turn(17)
    await robot.Drive.straight(-700)
    await robot.Drive.turn(73)
    await robot.Drive.straight(-70) 
    await robot.Drive.straight(70)
    await robot.Drive.turn(-73) 
    await robot.Drive.straight(680)
    '''

    # TODO: Mission 9 code goes here