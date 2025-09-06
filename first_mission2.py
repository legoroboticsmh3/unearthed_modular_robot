from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

L_motor=Motor(Port.A,Direction.COUNTERCLOCKWISE)
R_motor=Motor(Port.E,Direction.CLOCKWISE)

Front_attach=Motor(Port.D)
Back_attach=Motor(Port.C)

L_ColorSensor=ColorSensor(Port.B)
#R_ColorSensor=ColorSensor(Port.F)

Drive=DriveBase(L_motor, R_motor, 87, 144)

color = L_ColorSensor.color(surface=True)
#color = R_ColorSensor.color(surface=True)

reflection=L_ColorSensor.reflection()
#reflection=R_ColorSensor.reflection()



color.BLACK = Color(h=240, s=7, v=15)
my_colors = (Color.BLACK)
L_ColorSensor.detectable_colors(my_colors)


def wait_for_color(my_colors):
    # While the color is not the desired color, we keep waiting.
    print(color, reflection)
    while sensor.color() != my_colors:
        wait(20)

# Now we use the function we just created above.
while True:
    # Here you can make your train/vehicle go forward.
    print("Waiting for red ...")
    wait_for_color(my_colors)

Drive.use_gyro(True)
Drive.straight(235)
Drive.turn(90)
Drive.straight(50)


R_ColorSensor.detectable_colors(my_colors)

while True:
    color = sensor.color()
 
    print(color)

    if color == Color.Black:
        print("It works!")

    wait(100)
Drive.straight(50)