from pybricks.parameters import Port, Direction
from pybricks.pupdevices import Motor, ColorSensor, ForceSensor, UltrasonicSensor
from pybricks.tools import wait

def dump_all(robot): 
    print("Starting full robot data dump...\n")

    # --- robot INTERNALS ---
    battery_voltage = robot.battery.voltage()        # in mV
    battery_current = robot.battery.current()        # in mA
    temperature = robot.battery.temperature()        # in °C
    bt_status = robot.bluetooth.status()             # on/off/connected
    button = robot.button.pressed()                  # returns a tuple of pressed buttons

    # --- IMU DATA ---
    accel = robot.imu.acceleration()                 # (x, y, z) mm/s²
    ang_vel = robot.imu.angular_velocity()           # (x, y, z) °/s
    orientation = robot.imu.orientation()            # (yaw, pitch, roll)
    heading = robot.imu.heading()                    # yaw only

    # --- CONNECTED DEVICES ---
    devices = {}
    for port in [Port.A, Port.B, Port.C, Port.D]:
        device = robot.device(port)
        devices[str(port)] = str(device)

    # --- OUTPUT EVERYTHING ---
    print("========== robot STATUS ==========")
    print("Battery voltage (mV):", battery_voltage)
    print("Battery current (mA):", battery_current)
    print("Battery temperature (°C):", temperature)
    print("Bluetooth status:", bt_status)
    print("Buttons pressed:", button)
    print()
    print("---- IMU ----")
    print("Acceleration (mm/s²):", accel)
    print("Angular velocity (°/s):", ang_vel)
    print("Orientation (yaw, pitch, roll):", orientation)
    print("Heading (°):", heading)
    print()
    print("---- Connected Devices ----")
    for port, device in devices.items():
        print(f"{port}: {device}")
    print("================================\n")

