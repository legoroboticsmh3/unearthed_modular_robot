from pybricks.tools import wait


async def run_6(robot):
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
    await robot.Drive.turn(41)
    #####await wait(500)

    #Drives and get ready position to lift the missions 03 
    #await robot.Left_attach.run_angle(100,20)
    #await wait(100)
    await robot.Right_attach.run_angle(100,-120)
    #await wait(100)
    await robot.Drive.straight(245)
    #await robot.Drive.turn(-14.5)
    #await wait(500)

    

    #Lifts up mission 03
    await robot.Right_attach.run_angle(67,100)
    await robot.Right_attach.run_angle(350,33)
    await wait(500)


    #Drives to mission 13
    robot.Drive.settings(straight_speed=100)
    #Adjusts
    await robot.Drive.straight(-40)
    await robot.Drive.turn(65)
    #await wait(100)
    await robot.Right_attach.run_angle(100,-132)
    await wait(200)
    await robot.Drive.straight(185)


    #lifts up mission 13
    await robot.Right_attach.run_angle(400,133)
    robot.Drive.settings(straight_speed=400)

    
    #drives back home
    await robot.Drive.straight(-350)
    await robot.Drive.turn(77)
    await robot.Drive.straight(660)


async def run_9(robot):
    print("Starting Run: " + __name__)
    robot.Drive.settings(straight_speed=500)
    
    #Drives to Mision 13
    await robot.Drive.straight(67)
    await robot.Drive.turn(60)
    await robot.Drive.straight(680)
    await robot.Drive.turn(-93)
    await wait(100)
    await robot.Drive.straight(40)
    await wait(100)
    robot.Right_attach.dc(-120)
    await wait(100)
    await robot.Right_attach.run_angle(500,100)
    await wait(100)
    await robot.Drive.turn(90)
