from pybricks.tools import wait

async def run_6(robot):
  print("Starting Run: " + __name__)

  robot.Drive.settings(turn_rate=160)
  await robot.Drive.straight(420)
  
  #Completing Silo
  print(robot.gyro.heading())
  robot.Right_attach.dc(-60)
  await wait(500)
  await robot.Right_attach.run_angle(500,85) #hammer  up
  robot.Right_attach.dc(-60)
  await wait(500)
  await robot.Right_attach.run_angle(500,85) #hammer up
  robot.Right_attach.dc(-60)
  await wait(500)
  await robot.Right_attach.run_angle(500,120) #hammer up
  #await robot.Right_attach.run_angle(500,-100) #hammer down 4th time
  #await robot.Right_attach.run_angle(500,85) #hammer up
  robot.Drive.settings(straight_speed=300)



  #Going to the Forge
  await robot.Drive.turn(-45)
  await robot.Drive.straight(50)
  await robot.Drive.turn(45)
  await robot.Drive.straight(220) #reach the Boulder station
  #await robot.Drive.turn(-15)
  await robot.Drive.straight(15)
  await robot.Right_attach.run_angle(500,-85) #Complete the Forge
  await robot.Drive.turn(-15)
  await robot.Right_attach.run_angle(500,85)
  await robot.Drive.turn(-35)
  await robot.Drive.straight(140)
  await wait(500)
  await robot.Right_attach.run_angle(500,-50)
  robot.Drive.settings(turn_rate=100)
  await robot.Drive.turn(42)
  robot.Drive.settings(turn_rate=160)
  await wait(500)
  await robot.Right_attach.run_angle(500,-15)
  await robot.Right_attach.run_angle(500,60)
  await robot.Drive.turn(-10)
  await robot.Drive.straight(-320)
  await robot.Drive.turn(-95)
  await robot.Right_attach.run_angle(500,-65)
  await robot.Drive.straight(80)