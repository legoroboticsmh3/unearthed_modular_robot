from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

L_motor=Motor(Port.A,Direction.COUNTERCLOCKWISE)
R_motor=Motor(Port.E,Direction.CLOCKWISE)
Drive=DriveBase(L_motor, R_motor, 87, 144)


L_ColorSensor=ColorSensor(Port.B)

color = L_ColorSensor.color(surface=True)
reflection=L_ColorSensor.reflection()


# Initialize the sensor.
sensor = ColorSensor(Port.B)

while True:
    # Read the color and reflection
    color = sensor.color()
    reflection = sensor.reflection()

    # Print the measured color and reflection.
    print(color, reflection)

    # Move the sensor around and see how
    # well you can detect colors.

    # Wait so we can read the value.
    wait(100)

