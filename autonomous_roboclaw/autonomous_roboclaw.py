import TOFSeonsors as TOFSensors
import SRF10_rangefinder as SRF10

import Engine
import Servos
import time
import os
import atexit

SERVO_MIN = 600  # Min pulse length out of 4096
SERVO_MAX = 1200  # Max pulse length out of 4096

def stop_at_exit(engine):
    engine.stop_all_wheels()

def main():
    sensors = TOFSensors.TOFSensor()
    engine = Engine.Engine()
    servos = Servos.Servos()
    atexit.register(stop_at_exit, engine)
    engine.move_all_wheels_forward(20)
    servos.both_servos_down()
    servos.front_servo_forward()
    time.sleep(2)
    engine.move_all_wheels_backward(20)
    servos.both_servos_forward()
    time.sleep(2)
    engine.stop_all_wheels()
    servos.both_servos_down()

    rf = SRF10.SRF10()
    print ("Length of rxb: " + str(len(rf.rxb)))
    print ("Bus address : " + str(rf.bus_addr))
    while (1):
        print("Sensor left distance in mm: " + str(sensors.tof_left.get_distance()))
        print("Sensor right distance in mm: " + str(sensors.tof_right.get_distance()))
        print("USS read_range : " + str(rf.measure_and_read()))
        time.sleep(0.2)

    stop1 = 0
    stop2 = 0
    '''
    timing = tof.get_timing()
    if (timing < 20000):
        timing = 20000
    print("Timing %d ms" % (timing / 1000))

    while (1):
        pwm.set_pwm(0, 0, SERVO_MIN)
        time.sleep(0.5)
        distance = tof.get_distance()
        print("1: %d mm, %d cm" % (distance, (distance / 10)))
        if (distance > 200):
            engine.stop_all_wheels()
            stop1 = 1
            print("Stopp_1!")
        else:
            # c.move(30)
            stop1 = 0
            print("Frei_1!")
        # time.sleep(0.5)
        pwm.set_pwm(0, 0, SERVO_MAX)
        time.sleep(0.5)
        distance = tof.get_distance()
        print("2: %d mm, %d cm" % (distance, (distance / 10)))
        if (distance < 200):
            engine.stop_all_wheels()
            stop2 = 1
            print("Stopp_2!")
        else:
            # c.move(30)
            stop2 = 0
            print("Frei_2!")
        if (stop1 == 0 and stop2 == 0):
            engine.move_all_wheels_forward(20)
'''


if __name__ == '__main__':
    main()
