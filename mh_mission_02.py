from pybricks.tools import wait


#Shows mission 5
async def run_5(robot):#n
    print("Starting Run: " + __name__)#D

    #Drives to mission 2 area
    # await robot.Right_attach.run_angle(100,10)
    await robot.Drive.straight(660)
    await robot.Drive.turn(-43.49)

    # Keep the attaahcment in the middle poistion
    await robot.Right_attach.run_angle(500,-80)

    #Drives to push and pick up topsoils
    await robot.Drive.straight(170)

    # #right arm lowers down to grab topsoil and push the topsoil
    robot.Right_attach.dc(-55)
    await wait(451)
    await robot.Drive.straight(32)
    
    #Drives straight to push topsoil
    robot.Right_attach.dc(-10)
    await robot.Drive.straight(88)

    #Picks up topsoil
    await robot.Right_attach.run_angle(500,120) 
    
    await robot.Drive.straight(-210)
    await robot.Drive.turn(43.49)
    await robot.Drive.straight(-180)
    await robot.Drive.turn(88)
    #drives back to base

