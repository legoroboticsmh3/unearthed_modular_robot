from pybricks.tools import wait,multitask


#Shows mission 2
async def run_2(robot):#n
    print("Starting Run: " + __name__)

    robot.Drive.settings(straight_speed=400)
    robot.Right_attach.dc(55)
    robot.Left_attach.dc(85)
    await wait(600)
    robot.Right_attach.stop()
    robot.Left_attach.stop()


    await robot.Drive.straight(680) #drving straight to mission 2 
    await robot.Drive.turn(-38) #turning to line up with misssion 2 


    await robot.Right_attach.run_angle(500,-180) 
    await wait(200) #waiting for the attachment to move

    
    robot.Drive.settings(straight_speed=200) #setting the speed of driving straight 
    #await robot.Drive.turn(-5)  #
    #await robot.Drive.straight(5)
    #await robot.Drive.turn(-0.5)  #
    #await robot.Drive.straight(73)       #
    await robot.Drive.straight(170)
    await wait(200)
    #await robot.Drive.turn(-5.5)
    #await robot.Drive.straight(17)
    #await robot.Drive.turn(.5)
    #await robot.Drive.turn(-20)


    robot.Right_attach.dc(-40) #right arm lowers down to grab topsoil and push the topsoil
    await wait(451) #
    
    # await robot.Drive.straight(100)
    await multitask(robot.Drive.straight(100),wait(700), race=True)
    robot.Drive.stop()


    #Picks up topsoil
    await robot.Right_attach.run_angle(500,10) 
    await robot.Drive.straight(-15)
    await robot.Right_attach.run_angle(500,150) 
    
    await robot.Drive.turn(-10) 
    await robot.Drive.straight(-240) 
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

    robot.Left_attach.dc(-100)
    await wait(200)
    await robot.Left_attach.run_angle(500,80)
    robot.Left_attach.dc(-100)
    await wait(200)
    robot.Left_attach.dc(40)
    await wait(1000)
    await robot.Drive.straight(-80)
    await robot.Drive.turn(-70)
    #robot.Drive.settings(straight_speed=1000)
    await robot.Drive.straight(450)    
    

