#!/usr/bin/env python3

import pigpio
import struct


class Bh1750fvi:

    class Mode:
        HRESOLUTION_MODE = 0
        HRESOLUTION_MODE2 = 1
        LRESOLUTION_MODE = 2

    def __init__(self, pi: pigpio.pi, i2c_handle: int):
        self.__pigpio = pi
        self.__h = i2c_handle

    def power_down(self):
        self.__pigpio.i2c_write_device(self.__h, [self.__Opecode.POWER_DOWN])

    def power_on(self):
        self.__pigpio.i2c_write_device(self.__h, [self.__Opecode.POWER_ON])

    def reset(self):
        self.__pigpio.i2c_write_device(self.__h, [self.__Opecode.RESET])

    def continuously_measurement(self, mode: Mode):
        if mode == self.Mode.HRESOLUTION_MODE:
            opecode = self.__Opecode.CONTINUOUSLY_HRESOLUTION_MODE
        elif mode == self.Mode.HRESOLUTION_MODE2:
            opecode = self.__Opecode.CONTINUOUSLY_HRESOLUTION_MODE2
        elif mode == self.Mode.LRESOLUTION_MODE:
            opecode = self.__Opecode.CONTINUOUSLY_LRESOLUTION_MODE
        else:
            raise RuntimeError

        self.__pigpio.i2c_write_device(self.__h, [opecode])

    def read_lux(self) -> float:
        _, data = self.__pigpio.i2c_read_device(self.__h, 2)
        return struct.unpack(">H", data)[0]

    class __Opecode:
        POWER_DOWN = 0b0000_0000
        POWER_ON = 0b0000_0001
        RESET = 0b0000_0111
        CONTINUOUSLY_HRESOLUTION_MODE = 0b0001_0000
        CONTINUOUSLY_HRESOLUTION_MODE2 = 0b0001_0001
        CONTINUOUSLY_LRESOLUTION_MODE = 0b0001_0011
        ONE_TIME_HRESOLUTION_MODE = 0b0010_0000
        ONE_TIME_HRESOLUTION_MODE2 = 0b0010_0001
        ONE_TIME_LRESOLUTION_MODE = 0b0010_0011
        CHANGE_MEASUREMENT_TIME_HIGH = 0b0100_0000
        CHANGE_MEASUREMENT_TIME_LOW = 0b0110_0000


if __name__ == "__main__":
    import time

    pi = pigpio.pi()
    sensor = Bh1750fvi(pi, pi.i2c_open(1, 0x23))

    sensor.power_on()
    sensor.continuously_measurement(sensor.Mode.HRESOLUTION_MODE)

    for i in range(10):
        time.sleep(1)
        print(sensor.read_lux())

    pi.stop()
