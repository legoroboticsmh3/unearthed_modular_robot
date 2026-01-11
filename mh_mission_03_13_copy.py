from pybricks.tools import wait, multitask


async def run_3(robot):
    print("Starting Run: " + __name__)
    #robot.Drive.use_gyro(True)
    robot.Drive.settings(straight_speed=200)
    robot.Drive.settings(turn_rate=100)

    robot.Right_attach.dc(55) 
    # robot.Left_attach.dc(85)
    #await wait(600)
    #await robot.Left_attach.run_angle(500,-250)
    robot.Right_attach.stop()
    # robot.Left_attach.stop()
    #await robot.Left_attach.run_angle(500,-40)
       
  
    
    #Drives to mission 03a
    await robot.Drive.straight(50)
    robot.Drive.settings(straight_speed=500)
    await robot.Drive.straight(755)
    await robot.Drive.turn(90)
    await multitask(robot.Left_attach.run_angle(500,280), wait(800), race=True)
    #####await wait(500)

    #Drives and get ready position to lift the missions 03 
    #await robot.Left_attach.run_angle(100,20)
    #await wait(100)
    await robot.Drive.straight(130)
    await robot.Left_attach.run_angle(600-520,-180)
    await wait(800)
    await robot.Left_attach.run_angle(800-500,-50)
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
    robot.Drive.settings(straight_speed=100)
    #Adjust
    await robot.Drive.turn(20)
    await wait(100)
    await multitask(robot.Right_attach.run_angle(500,-280), wait(800), race=True)
    await robot.Drive.straight(178)

    #lifts up mission 13t
    robot.Right_attach.run_angle(400,232)
    await wait(3000)
    
    #await multitask(robot.Right_attach.run_angle(400,130), wait(00), race=True)
    robot.Drive.settings(straight_speed=400)

    
    #drives back home
    await robot.Drive.straight(-250)
    await robot.Drive.turn(79.9)
    await robot.Drive.straight(670)
   # Run three finished at line 67
