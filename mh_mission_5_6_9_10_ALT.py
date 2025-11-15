from pybricks.tools import wait

async def run_3(robot):
  print("Starting Run: " + __name__)
  robot.Drive.settings(straight_speed=700)
  await robot.Drive.straight(660) 
  await robot.Drive.turn(45)
  await robot.Drive.straight(70) #reach the Boulder station
  robot.Drive.settings(turn_rate=150)   #to get the boulders down 
  await robot.Drive.turn(-39)        #flip the red lever
    
  robot.Drive.settings(turn_rate=160)
  await robot.Drive.turn(-20) #align to reach who lives there
  await robot.Drive.straight(-15) #moving straight for who lives there and try to push the lever
  
  await robot.Right_attach.run_angle(500,-70)
  await robot.Right_attach.run_angle(500,70)
  #await wait(500)
  await robot.Drive.straight(20)
  await robot.Drive.turn(-35)
  await robot.Drive.straight(100)
  await robot.Drive.turn(55)
  await robot.Drive.straight(-150)
  #await robot.Drive.turn(10)  #(Tire Dirty Value)
  await robot.Drive.turn(13)  
  robot.Drive.settings(straight_speed=300)
  await robot.Drive.straight(144)    #reach the who lives there station
  robot.Drive.settings(turn_rate=100)
  await robot.Drive.turn(-40)            #flip the who lives there red lever
  robot.Drive.settings(turn_rate=160)
  await robot.Drive.straight(-110)
  robot.Drive.settings(straight_speed=700)
  await robot.Drive.turn(-40)  #previous value of 40 when i changed the who lives there angle to 13
  await robot.Drive.straight(600) 

  await robot.Drive.turn(-142)
  await robot.Drive.straight(46)
  await robot.Right_attach.run_angle(500,-70) # hammer the Tip Scales
  await robot.Drive.turn(-20)
  await robot.Drive.straight(-40)

  await robot.Right_attach.run_angle(500,80)
  await robot.Right_attach.run_angle(500,-90) #bring the hammer down to Whats on Sale
  
  robot.Drive.settings(straight_speed=300)
  await robot.Drive.straight(220) #whats on scale
  await robot.Drive.straight(-40)
  robot.Drive.settings(straight_speed=700)
  await robot.Right_attach.run_angle(500,70)
  await robot.Drive.straight(-70)

  #return to base
  await robot.Drive.turn(-40)  #original was 37 this is the value we need to change so the robot does not go close to the who lives there area
  await robot.Drive.straight(270)
  await robot.Drive.turn(54)
  await robot.Drive.straight(700)



