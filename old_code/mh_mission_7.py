from pybricks.tools import wait
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from urandom import randint
from umath import pi, sqrt

#alignment is 9B same as Run 5

async def run_5(robot):
    await robot.Left_attach.run_angle(300,100)

    # robot.Left_attach.run_angle(100,-90,then=Stop.HOLD)
    # robot.Drive.settings(straight_speed=500)
    # robot.Drive.settings(turn_rate=75)
    # await robot.Drive.straight(770)  #reach Heavy Lifting
    # await robot.Drive.turn(35)
    # await robot.Drive.straight(-40)  
    # await robot.Drive.straight(10)    #reach heavy lifting
    # await robot.Left_attach.run_angle(300,100)
    # robot.Drive.settings(straight_speed=200)
    # await robot.Drive.straight(63) #couple with the ring of the mill

#  robot.Right_attach.run_angle(100,-90*-1,then=Stop.HOLD)
#  robot.Drive.settings(straight_speed=500)
#  robot.Drive.settings(turn_rate=75)
#  await robot.Drive.straight(700)  #reach Heavy Lifting
#  await robot.Drive.turn(40)
#  robot.Right_attach.run_angle(500,180)
    
    '''
    await robot.Right_attach.run_angle(180,-75*-1)
    await robot.Drive.straight(-80)
    await robot.Drive.turn(-44)
    robot.Drive.settings(straight_speed=500)
    robot.Drive.settings(turn_rate=160)
    
    await robot.Drive.straight(-813)
    

#####Below is the original code for mission 7 heavy lifting with the originl starting alignment of 7T"
    # robot.Right_attach.run_angle(100,-90*-1,then=Stop.HOLD)
    # robot.Drive.settings(straight_speed=800)
    # robot.Drive.settings(turn_rate=75)
    # await robot.Drive.straight(770)  #reach Heavy Lifting




    # await robot.Drive.turn(35)
    # await robot.Drive.straight(-40)  
    # await robot.Drive.straight(10)    #reach heavy lifting
    # await robot.Right_attach.run_angle(200,80*-1)
    # robot.Drive.settings(straight_speed=200)
    # await robot.Drive.straight(63) #couple with the ring of the mill
    # await robot.Right_attach.run_angle(180,-75*-1)
    # await robot.Drive.straight(-80)
    # await robot.Drive.turn(-44)
    # robot.Drive.settings(straight_speed=500)
    # robot.Drive.settings(turn_rate=160)
    
    # await robot.Drive.straight(-813)
    




