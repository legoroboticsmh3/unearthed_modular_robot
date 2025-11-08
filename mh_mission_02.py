from pybricks.tools import wait


#Shows mission 5
async def run_5(robot):#n
    print("Starting Run: " + __name__)#D

    robot.Right_attach.dc(55)
    robot.Left_attach.dc(85)
    await wait(600)

    #Drives to mission 2 area
    # await robot.Right_attach.run_angle(100,10)
    await robot.Drive.straight(660)
    await robot.Drive.turn(-43.5)

    # Keep the attaahcment in the middle poistion
    await robot.Right_attach.run_angle(500,-80)

    #Drives to push and pick up topsoils
    await robot.Drive.straight(165)

    # #right arm lowers down to grab topsoil and push the topsoil
    robot.Right_attach.dc(-55)
    await wait(451)
    await robot.Drive.straight(32)
    
    #Drives straight to push topsoil
    robot.Right_attach.dc(-10)
    await robot.Drive.straight(88)

    #Picks up topsoil
    await robot.Right_attach.run_angle(500,120) 
    
    await robot.Drive.turn(-10)
    await robot.Drive.straight(-290)
    await robot.Drive.turn(-36.5)
    #await robot.Drive.straight(-180)
    #await robot.Drive.turn(88)
    #drives back to base

