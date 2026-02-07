from pybricks.tools import wait, multitask
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from urandom import randint
from umath import pi, sqrt

#alignment is 9B same as Run 5

async def run_5(robot):
    robot.Drive.settings(straight_speed=600)

    await multitask(robot.Right_attach.run_angle(100,90), wait(500), race=True)
    robot.Drive.settings(turn_rate=75)
    await robot.Drive.straight(15)
    await robot.Drive.turn(-11) #turn to avoid hitting silo
    # await robot.Drive.straight(740)  #reach Heavy Lifting
    # await robot.Drive.turn(51) #face heavy lifting
    # #await robot.Drive.straight(-40)  
    # await robot.Drive.straight(60)    #reach heavy lifting
    # await robot.Right_attach.run_angle(150,-180) #placing attachment down to pick up the heavy lifting
    # await wait(900)
    # robot.Drive.settings(straight_speed=200)
    # await robot.Drive.straight(50) #couple with the ring of the mill
    # await wait(300)
    # #await robot.Right_attach.run_angle(200,150) #pick up the weight
    # robot.Right_attach.dc(100)
    # await wait(2000)
    # robot.Drive.settings(straight_speed=600)
    # await robot.Drive.straight(-80) #come out of the area
    # await robot.Drive.turn(-50)#turn towards blue base
    # robot.Drive.settings(turn_rate=160)
    # await robot.Drive.straight(-800) #going to blue base
    

    
    




