from pybricks.tools import wait

async def run_8(robot):
    print("Starting Run: " + __name__)
 
    await robot.Drive.straight(430)
    await robot.Right_attach.run_angle(500,-100) #hammer down 1st time
    await robot.Right_attach.run_angle(500,100) #hammer  up
    #await robot.Right_attach.dc(-100) #hammer down 2nd time
    await robot.Right_attach.run_angle(500,-100)
    await robot.Right_attach.run_angle(500,100) #hammer up
    await robot.Right_attach.run_angle(500,-100) #hammer down 3rd time
    await robot.Right_attach.run_angle(500,100) #hammer up
    await robot.Right_attach.run_angle(500,-100) #hammer down 4th time
    await robot.Right_attach.run_angle(500,100) #hammer up
    
    #continue to mission 5 and 6
    await robot.Drive.straight(-110)
    await robot.Drive.turn(-90)
    await robot.Drive.straight(55)
    await robot.Drive.turn(90)
    await robot.Drive.straight(335) #reach the Boulder station
    wait(100)
    await robot.Drive.turn(40)  #flip the lever
    await robot.Drive.straight(60)
    robot.Drive.settings(turn_rate=150)   #to get the boulders down 
    await robot.Drive.turn(-39)        #to get the boulders down Mission number 6
    robot.Drive.settings(turn_rate=160)
    await robot.Drive.straight(55)
    await robot.Drive.turn(-95)     #mission number 5
    await robot.Drive.straight(-260) #push the boulders back
    await robot.Drive.turn(-8)
    await robot.Drive.straight(310)  
    await robot.Drive.turn(110)
    await robot.Drive.straight(80) #reach the who lives here area
    robot.Drive.settings(turn_rate=60)
    await robot.Drive.turn(-39) 


   # robot.Drive.straight(590)
   #  await robot.Drive.straight(200)
   #  await robot.Drive.turn(12)
   #  await robot.Drive.straight(500)
   #  await robot.Drive.turn(35)
   #  robot.Drive.settings(straight_speed=500)
   #  await robot.Drive.straight(-370)
   #  await robot.Drive.straight(230)
   #  await robot.Drive.turn(-60)
   #  await robot.Drive.straight(890)
   #  await robot.Drive.turn(-75)
   #  await robot.Drive.straight(640)
   