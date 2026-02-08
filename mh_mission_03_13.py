from pybricks.tools import wait, multitask

#THIS IS CURRENT CODE FOR RUNS 3 AND 13

async def run_3(robot):
    print("Starting Run: " + __name__)
    robot.Drive.settings(straight_speed=200)
    robot.Drive.settings(turn_rate=100)

    robot.Right_attach.dc(55) #setting up attachemnts
    robot.Left_attach.dc(-55) #setting up attachemnts
    await wait(400)
    robot.Right_attach.hold()
    robot.Left_attach.hold()
  
    #Drives to mission 03a
    robot.Drive.settings(straight_speed=600)
    await robot.Drive.straight(805)
    await robot.Drive.turn(85)
    await multitask(robot.Left_attach.run_angle(500,350), wait(800), race=True)
   

    #Drives and get ready position to lift the missions 03 
    await robot.Drive.straight(190)
    await robot.Left_attach.run_angle(500,-330) # was (600-520) for speed
    await wait(400)


    #Drives to mission 13t
    robot.Drive.settings(straight_speed=600)
    await robot.Left_attach.run_angle(300,100)
    
    #Adjust
    await robot.Drive.turn(32) # WAS 22
    await multitask(robot.Right_attach.run_angle(500,-480), wait(1000), race=True)
    await robot.Drive.straight(155)

    #lifts up mission 13t
    await multitask(robot.Right_attach.run_angle(500,450), wait(1000), race=True)
    
  
    #drives back home
    robot.Drive.settings(straight_speed=600)
    await robot.Drive.straight(-260)
    await robot.Drive.turn(79.9)
    await robot.Drive.straight(680)