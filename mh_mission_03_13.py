from pybricks.tools import wait, multitask

#THIS IS CURRENT CODE FOR RUNS 3 AND 13

async def run_3(robot):
    print("Starting Run: " + __name__)
    #robot.Drive.use_gyro(True)
    robot.Drive.settings(straight_speed=200)
    robot.Drive.settings(turn_rate=100)

    robot.Right_attach.dc(55) #setting up attachemnts
    # robot.Left_attach.dc(85)
    #await wait(600)
    #await robot.Left_attach.run_angle(500,-250)
    robot.Right_attach.stop()
    # robot.Left_attach.stop()
    #await robot.Left_attach.run_angle(500,-40)
       
  
    
    #Drives to mission 03a
    await robot.Drive.straight(50)
    robot.Drive.settings(straight_speed=600)
    await robot.Drive.straight(755)
    await robot.Drive.turn(89)
    await multitask(robot.Left_attach.run_angle(500,280), wait(1500), race=True)
   

    #Drives and get ready position to lift the missions 03 
    #await robot.Left_attach.run_angle(100,20)
    #await wait(100)
    await robot.Drive.straight(130)
    await robot.Left_attach.run_angle(170,-220) # was (600-520) for speed
    await wait(800)
    await robot.Left_attach.run_angle(300,-40) #was (800-500) for speed
    #await wait(100)
    #wait robot.Drive.straight(223)
    #await robot.Drive.turn(-14.5)
    #await wait(500)



    #Lifts up mission 03 t
    # await robot.Right_attach.run_angle(100,150)
    #robot.Right_attach.dc(75)
    #await wait(1500)
    #await robot.Right_attach.run_angle(350,32)
    #robot.Right_attach.dc(80)
    await wait(700)


    #Drives to mission 13t
    await robot.Drive.straight(10)
    robot.Drive.settings(straight_speed=300)
    #Adjust
    await robot.Drive.turn(22)
    await wait(100)
    await multitask(robot.Right_attach.run_angle(500,-580), wait(1000), race=True)
    await robot.Drive.straight(182)

    #lifts up mission 13t
    await multitask(robot.Right_attach.run_angle(400,232), wait(800), race=True)
    
    #await multitask(robot.Right_attach.run_angle(400,130), wait(00), race=True)
    robot.Drive.settings(straight_speed=600)

    
    #drives back home
    await robot.Drive.straight(-250)
    await robot.Drive.turn(79.9)
    await robot.Drive.straight(670)