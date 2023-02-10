import time
import board
from board import SCL, SDA
import busio
import pulseio
from adafruit_seesaw.seesaw import Seesaw

i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)

# Initial test of moisture levels, comment out later
#while True:
    # read moisture level through capacitive touch pad
#    touch = ss.moisture_read()

    # read temperature from the temperature sensor
#    temp = ss.get_temp()

#    print("temp: " + str(temp) + "  moisture: " + str(touch))
#    time.sleep(1)

# Monitor soil moisture, and water a plant as it needs it.
TOO_DRY = 880

# When did the pump last fire?
last_pumped = 0

# How long to wait between pumps for the soil to equalize (secs)
soil_wait_time = 30

# Initialize the water pump,
# a small  motor used via PWM on a SN754410 H-bridge chip.

pump = pulseio.PWMOut(board.A2, duty_cycle=0)

# Main Loop.
while True:
        touch = ss.moisture_read()
        if touch < TOO_DRY:
            print(f'TOO DRY! {touch}')

            if time.time() - last_pumped > soil_wait_time:
                print("Watering ...")
                pump.duty_cycle = 65535
                time.sleep(3)
                pump.duty_cycle = 0
                last_pumped = time.time()
        else:
            print(touch)

        time.sleep(2)
