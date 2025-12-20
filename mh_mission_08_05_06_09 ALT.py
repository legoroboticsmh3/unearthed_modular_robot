from pybricks.tools import wait, multitask


#Completing missions 5 and 6 in one motion



async def run_6(robot):
  print("Starting Run: " + __name__)

  await multitask(robot.Right_attach.run_angle(500, 50), wait(700), race=True)
  await multitask(robot.Left_attach.run_angle(500, 50), wait(700), race=True)

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
  await robot.Drive.turn(-3)
  await robot.Drive.straight(16)
  await robot.Right_attach.run_angle(500,-85) #Complete the Forge
  await robot.Right_attach.run_angle(500,50)
  await robot.Right_attach.run_angle(500,-30)
  await robot.Drive.straight(50)
  await robot.Drive.turn(-15)
  await robot.Right_attach.run_angle(500,85)
  await robot.Drive.turn(-35)
  await robot.Drive.straight(140)
  await robot.Right_attach.run_angle(500,-57)
  await wait(1000)
  robot.Drive.settings(turn_rate=100)
  await robot.Drive.turn(45)
  robot.Drive.settings(turn_rate=160)
  await wait(1000)
  await robot.Right_attach.run_angle(500,-20)
  await wait(500)
  await robot.Right_attach.run_angle(500,60)
  await robot.Drive.turn(-12)
  await robot.Drive.straight(-280)
  await robot.Drive.turn(-90)
  await robot.Drive.straight(20)
  await robot.Right_attach.run_angle(500,-80)
  await wait(500)
  await robot.Drive.straight(80)
  await robot.Right_attach.run_angle(500,75)
  await robot.Drive.turn(67)
  await wait(500)
  #await robot.Drive.straight(10)
  await robot.Left_attach.run_angle(500,-150)
  await wait(1000)
  await robot.Drive.straight(-150)
  await robot.Drive.straight(30)
  await robot.Left_attach.run_angle(500,50)
  await robot.Drive.straight(50)
  await robot.Left_attach.run_angle(500,67)
  await robot.Drive.straight(-400)

