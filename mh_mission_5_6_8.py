from pybricks.tools import wait

async def run_8(robot):
    print("Starting Run: " + __name__)
 
    await robot.Drive.straight(430)
    #await robot.Right_attach.run_angle(500,-100) #hammer down 1st time
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,85) #hammer  up
    #await robot.Right_attach.dc(-100) #hammer down 2nd time
    # await robot.Right_attach.run_angle(500,-100)
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,85) #hammer up
    #await robot.Right_attach.run_angle(500,-100) #hammer down 3rd time
    robot.Right_attach.dc(-60)
    await wait(500)
    await robot.Right_attach.run_angle(500,120) #hammer up
   #  await robot.Right_attach.run_angle(500,-100) #hammer down 4th time
   #  await robot.Right_attach.run_angle(500,85) #hammer up

   #  #continue to mission 5 and 6
    await robot.Drive.straight(-105)
    await robot.Drive.turn(-90)
    await robot.Drive.straight(55)
    await robot.Drive.turn(90)
    await robot.Drive.straight(335) 
    wait(100)
    await robot.Drive.turn(45)
    await robot.Drive.straight(50) #reach the Boulder station
    robot.Drive.settings(turn_rate=150)   #to get the boulders down 
    await robot.Drive.turn(-39)        #flip the red lever
    robot.Drive.settings(turn_rate=160)
    #await robot.Drive.straight(55)
    await robot.Drive.turn(-115)     #turn an angle to align and push the boulders back
    await robot.Drive.straight(-263) #push the boulders back
    await robot.Drive.turn(-8)
    await robot.Drive.straight(310)  
    await robot.Drive.turn(120)
    await robot.Drive.straight(125) #reach the who lives here area
    robot.Drive.settings(turn_rate=30)
    await robot.Drive.turn(-39) #flip the red lever
    robot.Drive.settings(turn_rate=160) #reset the turn rate


   # # robot.Drive.straight(590)
   # #  await robot.Drive.straight(200)
   # #  await robot.Drive.turn(12)
   # #  await robot.Drive.straight(500)
   # #  await robot.Drive.turn(35)
   # #  robot.Drive.settings(straight_speed=500)
   # #  await robot.Drive.straight(-370)
   # #  await robot.Drive.straight(230)
   # #  await robot.Drive.turn(-60)
   # #  await robot.Drive.straight(890)
   # #  await robot.Drive.turn(-75)
   # #  await robot.Drive.straight(640)
   