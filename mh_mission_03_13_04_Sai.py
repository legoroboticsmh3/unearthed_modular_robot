from pybricks.tools import wait, multitask

#DEFINETLEY USE THIS FILE

async def run_3(robot):
    print("Starting Run: " + __name__)
    #robot.Drive.use_gyro(True)
    robot.Drive.settings(straight_speed=600)
    robot.Drive.settings(turn_rate=100)

    robot.Right_attach.dc(120)
    robot.Left_attach.dc(85)
    await wait(600)
    robot.Right_attach.stop()
    robot.Left_attach.stop()
    
    #Drives to mission 03a
    await robot.Drive.straight(-950) #orignally was 680
    await robot.Drive.turn(-90)
    await robot.Drive.straight(-90) # Going back to allow the angle adjustment. Sigma value was -90 
    await wait(200)
    await robot.Drive.turn(-2) #turn to align orginal -2


    await robot.Left_attach.run_angle(300,-250) # this is for careful recovery (Sigma was -250)
    await robot.Right_attach.run_angle(300,-290) # this is for the mine cart

    # Slow move into.
    robot.Drive.settings(straight_speed=50)
    await wait(200)
    await robot.Drive.straight(105) #Moves into the artifact area to grab artifact
    await multitask(robot.Left_attach.run_angle(300,-2),wait(100), race=True) #Lowering arm to align perfectly to artifact
    #await wait(500) 
    await robot.Drive.straight(75)  #feb 16 orig value 96 distance that it goes inside the frames
    #await wait(100)
    await robot.Left_attach.run_angle(100,60) #lift arm after it grabs the artifact inside the frames Sigma value is (100,60)
    await wait(100)

    # With prints, it is working. So dont remove the print.
    print("V 1",robot.Right_attach.settings())
    print("left attach done")
    robot.Right_attach.run(300) #Sending minecart to to other side : was(720)
    print("V2 ",robot.Right_attach.settings())
    await wait(2000)
    robot.Right_attach.stop()

    await robot.Drive.straight(-145) #backing out of artifact area
    await robot.Left_attach.run_angle(300,75) #comes outside and lifts artifact higher to secure it
    #await wait(100)


    #Drives to mission 13t
    robot.Drive.settings(straight_speed=600) #was 400
    await robot.Drive.turn(39.7)#turns toward dinosaur
    await multitask(robot.Right_attach.run_angle(400,-380),wait(1000), race=True) #lowering to prepare for lifting the dinosaur
    await robot.Drive.straight(380) #going toward dinosaur and putting arm under the artifact to lift it up
    await multitask(robot.Right_attach.run_angle(600,380),wait(1000), race=True) #lifting the dinosaur up
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