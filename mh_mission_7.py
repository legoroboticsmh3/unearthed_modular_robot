from pybricks.tools import wait
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from urandom import randint
from umath import pi, sqrt

async def run_2(robot):
    robot.Right_attach.run_angle(100,-90*-1,then=Stop.HOLD)
    robot.Drive.settings(straight_speed=500)
    robot.Drive.settings(turn_rate=75)
    await robot.Drive.straight(770)  #reach Heavy Lifting
    await robot.Drive.turn(35)
    await robot.Drive.straight(-40)  
    await robot.Drive.straight(10)    #reach heavy lifting
    await robot.Right_attach.run_angle(200,80*-1)
    robot.Drive.settings(straight_speed=200)
    await robot.Drive.straight(63) #couple with the ring of the mill
    await robot.Right_attach.run_angle(180,-75*-1)
    await robot.Drive.straight(-80)
    await robot.Drive.turn(-44)
    robot.Drive.settings(straight_speed=500)
    robot.Drive.settings(turn_rate=160)
    #await robot.Drive.straight(-813)   #(Use this distance to come to the home base)

    #Adding code below to see if I can solve mission 10 and reach 

    await robot.Drive.straight(-630)
    robot.Drive.settings(turn_rate=75)
    await robot.Drive.turn(-40)
    await robot.Drive.straight(420)
    await robot.Right_attach.run_angle(100,80*-1)
    await robot.Right_attach.run_angle(200,-100*-1)
    await robot.Drive_straight(-200)








