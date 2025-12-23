from pybricks.tools import wait, multitask


async def run_3(robot):
    print("Starting Run: " + __name__)
    #robot.Drive.use_gyro(True)
    robot.Drive.settings(straight_speed=500)
    robot.Drive.settings(turn_rate=100)

    robot.Right_attach.dc(55)
    robot.Left_attach.dc(85)
    await wait(600)
    robot.Right_attach.stop()
    robot.Left_attach.stop()
    
    #Drives to mission 03a
    await robot.Drive.straight(680)
    await robot.Drive.turn(46)
    #####await wait(500)

    #Drives and get ready position to lift the missions 03 
    #await robot.Left_attach.run_angle(100,20)
    #await wait(100)
    await robot.Right_attach.run_angle(100,-120)
    #await wait(100)
    await robot.Drive.straight(223)
    #await robot.Drive.turn(-14.5)
    #await wait(500)

    

    #Lifts up mission 03 t
    await robot.Right_attach.run_angle(75,78)
    await wait(1500)
    await robot.Right_attach.run_angle(350,35)
    await wait(500)


    #Drives to mission 13t
    robot.Drive.settings(straight_speed=100)
    #Adjustst
    await robot.Drive.straight(-40)
    await robot.Drive.turn(67)
    await wait(100)
    await robot.Right_attach.run_angle(100,-132)
    await wait(200)
    await robot.Drive.straight(176)


    #lifts up mission 13t
    robot.Right_attach.run_angle(400,130)
    await wait(1500)
    #await multitask(robot.Right_attach.run_angle(400,130), wait(00), race=True)
    robot.Drive.settings(straight_speed=400)

    
    #drives back homet
    await robot.Drive.straight(-350)
    await robot.Drive.turn(70)
    await robot.Drive.straight(660)


