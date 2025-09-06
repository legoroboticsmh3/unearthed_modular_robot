from pybricks.tools import wait
from mh_controllers import StartPID

async def swerve(robot):
    chassisPID = StartPID(robot.config['turn']['pid'])
    robot.chassisPID = chassisPID

    #8 Segment Ackermann/Differential Gain Ammount Based on Wheel Angle
    #aGainMods = [0, .5, 1, .5, 0,-.5,-1,-.5]
    #dGainMods = [1, .5, 0,-.5,-1,-.5, 0, .5]

    #16 Segment Ackermann/Differential Gain Ammount Based on Wheel Angle
    aGainMods = [0, .25, .5, .75, 1, .75, .5, .25, 0, -.25,-.5,-.75,-1,-.75,-.5,-.25]
    dGainMods = [1, .75, .5, .25, 0,-.25,-.5,-.75, -1,-.75,-.5,-.25, 0, .25, .5, .75]

    ModIncrement = 360/len(aGainMods)
    while True:

        if not robot.runAttachment:
            wheelAngle = robot.wheelAngle
            speedDirection = robot.reverseWheels
            if robot.driveSpeed < 0:
                    speedDirection * -1
            speed = robot.driveSpeed * speedDirection
            chassisError = robot.gyro.heading()-robot.chassisAngle
            turnCorrection = chassisPID.update(chassisError)
            wheelCompass = wheelAngle % 360
            dGainMod = 0
            aGainMod = 0
            #print('wheelAngle:', robot.wheelAngle, 'chassisAngle:', robot.chassisAngle, 'gyroHeading:', robot.gyro.heading())

            if speed == 0 and chassisError == 0:
                #Use stop() instead of hold() to save power
                #Only use hold for line follow/attachment via SwerveStop()
                ## TESTING: reconfigured back to hold for better odometry
                robot.leftDrive.hold()
                robot.rightDrive.hold()
                robot.leftTurn.hold()
                robot.rightTurn.hold()
            else:
                for i in range(len(aGainMods)):
                    ModsAngle = ModIncrement * i
                    MinAngle = (ModsAngle - (ModIncrement/2)) % 360
                    MaxAngle = (ModsAngle + (ModIncrement/2)) % 360
                    if (MaxAngle > MinAngle and wheelCompass > MinAngle and wheelCompass <= MaxAngle) or (MaxAngle < MinAngle and (wheelCompass > MinAngle or wheelCompass <= MaxAngle)):
                        aGainMod = aGainMods[i]
                        dGainMod = dGainMods[i]
                        #print('Gain Modifier Matched! aGainMod:', aGainMod, '  dGainMod:', dGainMod, 'wheelCompass: ',wheelCompass)
                robot.leftDrive.run(speed-(turnCorrection*robot.config['turn']['dGain']*dGainMod))
                robot.rightDrive.run(speed+(turnCorrection*robot.config['turn']['dGain']*dGainMod))
                robot.leftTurn.track_target(wheelAngle-max(min(turnCorrection*robot.config['turn']['aGain']*aGainMod*speedDirection,90),-90)+robot.leftTurnOffset)
                robot.rightTurn.track_target(wheelAngle+max(min(turnCorrection*robot.config['turn']['aGain']*aGainMod*speedDirection,90),-90))
        await wait(25)