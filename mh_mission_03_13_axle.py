from pybricks.tools import wait, multitask


async def run_11(robot):
    print("Starting Run: " + __name__)
    #robot.Drive.use_gyro(True)
    robot.Drive.settings(straight_speed=200)
    robot.Drive.settings(turn_rate=100)

    robot.Right_attach.dc(55) #setting up attachemnts
    robot.Left_attach.dc(100)
    robot.Left_attach.run_angle(400,250)

    await wait(400)
    #await robot.Left_attach.run_angle(500,-250)
    robot.Right_attach.stop()
    robot.Left_attach.stop()
    #await robot.Left_attach.run_angle(500,-40)
       
  
    
    #Drives to mission 03a
   # await robot.Drive.straight(50)
    robot.Drive.settings(straight_speed=600)
    await robot.Drive.straight(860)
    await robot.Drive.turn(90)
    await multitask(robot.Left_attach.run_angle(500,-350), wait(600), race=True)
    await robot.Drive.straight(95)
    await robot.Drive.turn(-5)
   

    #Drives and get ready position to lift the missions 03 
    #await robot.Left_attach.run_angle(100,20)
    #await wait(100)
   # await robot.Drive.straight(120)
    #await robot.Left_attach.run_angle(200, 220)  #condition for Gamma Robot
    
    await robot.Left_attach.run_angle(200, 380)   #condition for Sigma Robot
    #await multitask(robot.Left_attach.run_angle(180,220), wait(1000), race=True)
    await wait(1000)
    # await robot.Left_attach.run_angle(400, 80)
    #Drives to mission 13t
    await robot.Drive.straight(-40)
    robot.Drive.settings(straight_speed=300)
    #Adjust
    await robot.Drive.turn(30) # WAS 22 #turning to reach Mineshaft explorer
    await wait(100)
    await multitask(robot.Right_attach.run_angle(500,-580), wait(1000), race=True)
    await robot.Drive.straight(255) #Reaching and lifting statue rebuild

    #lifts up mission 13t
    await multitask(robot.Right_attach.run_angle(400,330), wait(800), race=True)
    
    #await multitask(robot.Right_attach.run_angle(400,130), wait(00), race=True)
    robot.Drive.settings(straight_speed=600)

    
    #drives back home
    await robot.Drive.straight(-250)
    await robot.Drive.turn(79.9)
    await robot.Drive.straight(670)

    # await robot.Drive.straight(95)
    # await robot.Left_attach.run_angle(600, 300)
    # await multitask(robot.Left_attach.run_angle(600, 500), wait(2000), race=True)
    # await robot.Left_attach.run_angle(600,350) # was (600-520) for speed
    # await wait(800)
    # await robot.Left_attach.run_angle(300,40) #was (800-500) for speed
    '''
    #await wait(100)
    #wait robot.Drive.straight(223)
    #await robot.Drive.turn(-14.5)
    #await wait(500)



#     #Lifts up mission 03 t
#     # await robot.Right_attach.run_angle(100,150)
#     #robot.Right_attach.dc(75)
#     #await wait(1500)
#     #await robot.Right_attach.run_angle(350,32)
#     #robot.Right_attach.dc(80)
#     await wait(700)


#     #Drives to mission 13t
#     await robot.Drive.straight(10)
#     robot.Drive.settings(straight_speed=300)
#     #Adjust
#     await robot.Drive.turn(23) # WAS 22
#     await wait(100)
#     await multitask(robot.Right_attach.run_angle(500,-580), wait(1000), race=True)
#     await robot.Drive.straight(202)

#     #lifts up mission 13t
#     await multitask(robot.Right_attach.run_angle(400,330), wait(800), race=True)
    
#     #await multitask(robot.Right_attach.run_angle(400,130), wait(00), race=True)
#     robot.Drive.settings(straight_speed=600)

    
#     #drives back home
#     await robot.Drive.straight(-250)
#     await robot.Drive.turn(79.9)
#     await robot.Drive.straight(670)'''