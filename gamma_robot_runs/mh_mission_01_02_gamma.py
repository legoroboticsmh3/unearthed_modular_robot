from pybricks.tools import wait,multitask


#Shows mission 2
async def run_2(robot):
    print("Starting Run: " + __name__)

    robot.Drive.settings(straight_speed=400)
    robot.Right_attach.dc(55)
    robot.Left_attach.dc(85)
    await wait(600)
    robot.Right_attach.stop()
    robot.Left_attach.stop()


    await robot.Drive.straight(745) #drving straight to mission 2 #was 700
    await robot.Drive.turn(-45) #turning to line up with misssion 2 


    await robot.Right_attach.run_angle(500,-180) 
    await wait(200) #waiting for the attachment to move

    
    robot.Drive.settings(straight_speed=200) #setting the speed of driving straight 
    await robot.Drive.straight(110) #driving into topsoil
    await wait(200)

    robot.Right_attach.dc(-40) #right arm lowers down to grab topsoil and push the topsoil
    await wait(451) 
    
    await multitask(robot.Drive.straight(140),wait(700), race=True) #driving forward while pushing topsoil
    robot.Drive.stop()


    #Picks up topsoil
    #await robot.Drive.turn(-7)# turning to not get stuck on surface brushing while backing up
    await robot.Right_attach.run_angle(100,50)
    await robot.Drive.straight(-50) #driving backwards to get to surface brushing
    await robot.Right_attach.run_angle(100,200) #picking up topsoil
    #await robot.Drive.turn(7)
    
    await robot.Drive.turn(-12) 
    await robot.Drive.straight(-200) 
    await robot.Drive.turn(-46)
    await robot.Drive.straight(40)
    await robot.Drive.turn(10)
    await wait(200)
    #await robot.Drive.drive_power(30)
    robot.L_Motor.dc(65)
    robot.R_Motor.dc(50)
    await wait(600)
    robot.R_Motor.stop()
    robot.L_Motor.dc(80)
    await wait(300)
    robot.L_Motor.stop()

    #mission_02 to tap twice for surface brushing
    robot.Left_attach.dc(-100)
    await wait(200)
    await robot.Left_attach.run_angle(500,200)
    robot.Left_attach.dc(-100)
    await wait(200)
    # await robot.Left_attach.run_angle(500,200)
    await multitask(robot.Left_attach.run_angle(500,200), wait(1000), race=True)
    robot.Left_attach.stop()
    #robot.Left_attach.dc(-100)
    #await wait(200)
    await robot.Drive.straight(-80)
    await robot.Drive.turn(-70)
    robot.Drive.settings(straight_speed=600)
    await robot.Drive.straight(450)    