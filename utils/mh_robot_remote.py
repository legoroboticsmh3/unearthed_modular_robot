from pybricks.tools import wait, Matrix
from pybricks.parameters import Button, Color
from pybricks.iodevices import XboxController
from ..mh_media import MY_ICONS
from umath import *

def ConnectRemote(self):
    if(self.config['xboxcontroller']['enable']):
        self.light.animate([Color.RED, Color.BLUE], 1000)
        print("Waiting For XBox Controller...")
        if (self.config['hub'] != 'technic'):
            self.matrix.icon(Matrix(MY_ICONS['XBOX']))
        try:
            # Search for a remote for 10 seconds.
            self.remote = XboxController()
            self.light.on(Color.RED)
            print("Connected!")
        except OSError:
            print("Could not find the remote.")
            self.light.on(Color.YELLOW)


async def SwerveRemote(robot):
    def closest_rotation(currentAngle, targetAngle):
        # Normalize the angles to be within 0 - 360
        def normalize_angle(angle):
            return angle % 360

        currentAngle = normalize_angle(currentAngle)
        if robot.reverseWheels == -1:
            targetAngle = normalize_angle(targetAngle+180)
        else:
            targetAngle = normalize_angle(targetAngle)

        # Calculate the difference between normalized angles
        difference = targetAngle - currentAngle
       
        # Normalize the difference to be within -180 - 180
        if difference > 180:
            difference -= 360
        elif difference < -180:
            difference += 360

        return difference

    def setDirection(targetAngle):
        newAngleDelta = closest_rotation(robot.wheelAngle, targetAngle)

        # Normalize the difference to be within -90 - 90 and reverse wheel direction if needed
        if newAngleDelta > 90:
            newAngleDelta -= 180
            robot.reverseWheels *= -1
        if newAngleDelta < -90:
            newAngleDelta += 180
            robot.reverseWheels *= -1

        robot.wheelAngle = robot.wheelAngle + newAngleDelta

    # Left Joystick : wheel direction relative to (chassis or field)
    # Right Joystick : rotate chassis clockwise or counterclockwise
    # A Button:  toggle between default chassis orientation and field orientation
    # B Button:  Reset field north orientation
    # X Button:  toggle from Chassis/Field Swerve Mode to Diffy/Ackerman fixed Angle Mode
    if(robot.config['xboxcontroller']['enable']):
        SWERVE_MODE = True
        FIELD_MODE = 0
        JOY_DEADZONE = robot.config['xboxcontroller']['deadzone']
        while True:
            if Button.X in robot.remote.buttons.pressed():
                while Button.X in robot.remote.buttons.pressed():
                    await wait(100)
                SWERVE_MODE = not SWERVE_MODE # Toggle between 1 and 0
            if Button.A in robot.remote.buttons.pressed():
                while Button.A in robot.remote.buttons.pressed():
                    await wait(100)
                FIELD_MODE = 1 - FIELD_MODE # Toggle between 1 and 0
            if Button.B in robot.remote.buttons.pressed():
                robot.chassisAngle = 0
                robot.gyro.reset_heading(0)
            if (robot.config['hub'] != 'technic'):
                if not SWERVE_MODE:
                    robot.matrix.char("D")
                elif FIELD_MODE:
                    robot.matrix.char("F")
                else:
                    robot.matrix.char("S")

            x, y = robot.remote.joystick_left()
            speed = sqrt((x*x)+(y*y));
            raw_angle = degrees(atan2(y, x))*-1
            angle = (raw_angle+90)%360

            turn, speed2 = robot.remote.joystick_right()
            dpad = robot.remote.dpad()
            if SWERVE_MODE:
                if abs(x) <= JOY_DEADZONE and abs(y) <= JOY_DEADZONE:
                    robot.driveSpeed = 0
                else:
                    #This Code can replace the if else condition however will constantly check heading.
                    #setDirection(angle-(robot.gyro.heading()*FIELD_MODE))

                    # [Field Oriented Swerve Mode]
                    if FIELD_MODE:
                        setDirection(angle-robot.gyro.heading())
                    # [Chassis Oriented Swerve Mode]
                    else:
                        setDirection(angle)
                    robot.driveSpeed = speed*14
                if abs(turn) > JOY_DEADZONE:
                    robot.chassisAngle += turn *.2  # Adjust to .1 or .3 depending on speed of robot turns.
            # [Fixed Angle Diffy/Ackermann Mode]
            else:
                if abs(x) <= JOY_DEADZONE and abs(y) <= JOY_DEADZONE:
                    robot.driveSpeed = 0
                else:
                    setDirection(angle)
                    robot.driveSpeed = speed*14
                if abs(turn) > JOY_DEADZONE:
                    if speed2 > JOY_DEADZONE * -1:
                        robot.chassisAngle += turn *.2
                    else:
                        robot.chassisAngle += turn *-.2
                # Car type steering. When in reverse, turning right will rotate chassis counter clockwise
                if abs(speed2) > JOY_DEADZONE:
                    robot.driveSpeed = sqrt((turn*turn)+(speed2*speed2)) * 14 * (-1 if speed2 < 0 else 1)
                #Use directional pad to set fixed angle and steer with right joystick
                if dpad != 0:
                    print('dpad',dpad, 'angle', (dpad - 1) * 45)
                    setDirection((dpad - 1) * 45)
            await wait(100)
