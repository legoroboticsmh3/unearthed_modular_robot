from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

def run_2(robot):
    await robot.Drive.straight(770)
    await robot.Drive.turn(40)
    await robot.Drive.straight(-40)
    await robot.Right_attach.run_angle(250,55)
    await robot.Drive.straight(63)
    await robot.Right_attach.run_angle(200,-50)
    await robot.Drive.turn(-40)
    await robot.Drive.straight(-770)
