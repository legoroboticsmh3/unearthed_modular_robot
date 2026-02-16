from pybricks.tools import wait, multitask

#DO NOT USE THIS FILE, USE mh_mission_03_13.py INSTEAD

async def run_3(robot):
    print("Starting Run: " + __name__)
    #robot.Drive.use_gyro(True)
    robot.Drive.settings(straight_speed=500)
    robot.Drive.settings(turn_rate=100)

    robot.Right_attach.dc(120)
    robot.Left_attach.dc(85)
    await wait(600)
    robot.Right_attach.stop()
    robot.Left_attach.stop()
    
    #Drives to mission 03a
    await robot.Drive.straight(-1050) #orignally was 680
    await robot.Drive.turn(-90)
    await robot.Drive.straight(-110) # Going back to allow the angle adjustment.
    await wait(200)
    await robot.Drive.turn(-2) #turn to align orginal -2


    await robot.Left_attach.run_angle(300,-250) # this is for careful recovery
    await robot.Right_attach.run_angle(300,-290) # this is for the mine cart

    # Slow move into.
    robot.Drive.settings(straight_speed=100)
    await robot.Drive.straight(125)
    await multitask(robot.Left_attach.run_angle(300,-2),wait(100), race=True)
    await wait(500) 
    await robot.Drive.straight(50)  #feb 16 orig value 96 distance that it goes inside the frames
    await wait(100)
    await robot.Left_attach.run_angle(100,60) #lift angle after it grabs the artifact inside the frames roignally it was 300,50
    await wait(100)

    # With prints, it is working. So dont remove the print.
    print("V 1",robot.Right_attach.settings())
    print("left attach done")
    robot.Right_attach.run(720)
    print("V2 ",robot.Right_attach.settings())
    await wait(1000)
    robot.Right_attach.stop()

    await robot.Drive.straight(-145)
    await robot.Left_attach.run_angle(300,75)
    await wait(100)


    #Drives to mission 13t
    robot.Drive.settings(straight_speed=400)
    await robot.Drive.turn(39)#original value was 37
    await multitask(robot.Right_attach.run_angle(400,-380),wait(1000), race=True)
    await robot.Drive.straight(380)
    await multitask(robot.Right_attach.run_angle(600,380),wait(1000), race=True)
    '''
    #this is to deliver the artifact
    await robot.Drive.straight(-100)
    await robot.Drive.turn(15)
    await robot.Drive.straight(100)
    await multitask(robot.Left_attach.run_angle(600,-480),wait(1000), race=True)
   '''
    #drives back home
    await robot.Drive.straight(-250)
    #await multitask(robot.Left_attach.run_angle(600,200),wait(400), race=True) # Lift up the left arm
    await robot.Drive.turn(70)
    robot.Drive.settings(straight_speed=600)
    await robot.Drive.straight(800)