from enum import IntEnum


class Registers(IntEnum):
    WHO_AM_I = 0x0F
    CTRL1 = 0x20
    CTRL2 = 0x21
    CTRL3 = 0x22
    CTRL4 = 0x23
    CTRL5 = 0x24
    STATUS_M = 0x27
    OUT_X_L = 0x28
    OUT_X_H = 0x29
    OUT_Y_L = 0x2A
    OUT_Y_H = 0X2B
    OUT_Z_L = 0x2C
    OUT_Z_H = 0x2D


class GyroScale(IntEnum):
    DPS_245 = 0
    DPS_500 = 1
    DPS_2000 = 2

    @property
    def scaling_factor(self):
        """
        The scaling factor based on the sensor full scale.

        :return: The scaling factor expressed in mdps/digit.
        """
        if self == GyroScale.DPS_245:
            return 8.75
        elif self == GyroScale.DPS_500:
            return 17.5
        elif self == GyroScale.DPS_2000:
            return 70.0
        else:
            return 0.0


class L3GD20H:

    # The physical I2C address of the MEMS
    address = 0x6B
    # The accelerometer axis output registers
    axis_output_registers = [
        Registers.OUT_X_L,
        Registers.OUT_X_H,
        Registers.OUT_Y_L,
        Registers.OUT_Y_H,
        Registers.OUT_Z_L,
        Registers.OUT_Z_H,
    ]

    def __init__(self, gyro_scale):
        self.gyro_scale = gyro_scale
