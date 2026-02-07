from pybricks.tools import wait, multitask

#THIS IS CURRENT CODE FOR RUNS 3 AND 13

async def run_3(robot):
    print("Starting Run: " + __name__)
    robot.Drive.settings(straight_speed=200)
    robot.Drive.settings(turn_rate=100)

    robot.Right_attach.dc(55) #setting up attachemnts
    robot.Right_attach.stop()
  
    #Drives to mission 03a
    robot.Drive.settings(straight_speed=600)
    await robot.Drive.straight(805)
    await robot.Drive.turn(85)
    await multitask(robot.Left_attach.run_angle(500,350), wait(1500), race=True)
   

    #Drives and get ready position to lift the missions 03 
    await robot.Drive.straight(190)
    await robot.Left_attach.run_angle(170,-220) # was (600-520) for speed
    await wait(400)
    await robot.Left_attach.run_angle(300,-40) #was (800-500) for speed
    await wait(400)


    #Drives to mission 13t
    await robot.Drive.straight(-30)
    robot.Drive.settings(straight_speed=300)
    
    #Adjust
    await robot.Drive.turn(28) # WAS 22
    await robot.Left_attach.run_angle(300,100)
    await multitask(robot.Right_attach.run_angle(500,-480), wait(1000), race=True)
    await robot.Drive.straight(180)

    #lifts up mission 13t
    await multitask(robot.Right_attach.run_angle(500,450), wait(1000), race=True)
    
    #await multitask(robot.Right_attach.run_angle(400,130), wait(00), race=True)
    robot.Drive.settings(straight_speed=600)

    
    #drives back home
    await robot.Drive.straight(-250)
    await robot.Drive.turn(79.9)
    await robot.Drive.straight(680)