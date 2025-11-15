from pybricks.tools import wait,multitask


#Shows mission 5
async def run_5(robot):#n
    print("Starting Run: " + __name__)

    robot.Drive.settings(straight_speed=400)
    robot.Right_attach.dc(55)
    robot.Left_attach.dc(85)
    await wait(600)
    robot.Right_attach.stop()
    robot.Left_attach.stop()

    #Drives to mission 2 area
    await robot.Drive.straight(650)
    await robot.Drive.turn(-40)

    # Keep the attaahcment in the middle poistion
    await robot.Right_attach.run_angle(500,-80)

    #Drives to push and pick up topsoils
    robot.Drive.settings(straight_speed=200)
    await robot.Drive.straight(100)
    await robot.Drive.turn(-7.5)
    await robot.Drive.straight(55)

    # #right arm lowers down to grab topsoil and push the topsoil
    robot.Right_attach.dc(-28)
    await wait(451)
    
    # await robot.Drive.straight(100)
    await multitask(robot.Drive.straight(100),wait(700), race=True)
    robot.Drive.stop()


    #Picks up topsoil
    await robot.Right_attach.run_angle(500,120) 
    
    await robot.Drive.turn(-10)
    await robot.Drive.straight(-230)
    await robot.Drive.turn(-46)
    await robot.Drive.straight(50)
    await robot.Drive.turn(20)
    await wait(200)
    #await robot.Drive.drive_power(30)
    robot.L_Motor.dc(65)
    robot.R_Motor.dc(50)
    await wait(600)
    robot.R_Motor.stop()
    robot.L_Motor.dc(80)
    await wait(300)
    robot.L_Motor.stop()

    robot.Left_attach.dc(-100)
    await wait(200)
    await robot.Left_attach.run_angle(500,80)
    robot.Left_attach.dc(-100)
    await wait(200)
    robot.Left_attach.dc(70)
    await wait(1000)
    await robot.Drive.straight(-80)
    await robot.Drive.turn(-70)
    robot.Drive.settings(straight_speed=1000)
    await robot.Drive.straight(450)    
    

