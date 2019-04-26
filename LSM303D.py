from enum import IntEnum


class Registers(IntEnum):
    STATUS_M = 0x07
    OUT_X_L_M = 0x08
    OUT_X_H_M = 0x09
    OUT_Y_L_M = 0x0A
    OUT_Y_H_M = 0X0B
    OUT_Z_L_M = 0x0C
    OUT_Z_H_M = 0x0D
    WHO_AM_I = 0x0F
    CTRL0 = 0x1F
    CTRL1 = 0x20
    CTRL2 = 0x21
    CTRL3 = 0x22
    CTRL4 = 0x23
    CTRL5 = 0x24
    CTRL6 = 0x25
    CTRL7 = 0x26
    STATUS_A = 0x27
    OUT_X_L_A = 0x28
    OUT_X_H_A = 0x29
    OUT_Y_L_A = 0x2A
    OUT_Y_H_A = 0x2B
    OUT_Z_L_A = 0x2C
    OUT_Z_H_A = 0x2D


class AccelScale(IntEnum):
    G_2 = 0
    G_4 = 1
    G_6 = 2
    G_8 = 3
    G_16 = 4

    @property
    def scaling_factor(self):
        """
        The scaling factor based on the sensor full scale.

        :return: The scaling factor expressed in mg/digit.
        """
        if self == AccelScale.G_2:
            return 0.061
        elif self == AccelScale.G_4:
            return 0.122
        elif self == AccelScale.G_6:
            return 0.183
        elif self == AccelScale.G_8:
            return 0.244
        elif self == AccelScale.G_16:
            return 0.732
        else:
            return 0.0


class MagScale(IntEnum):
    Gauss_2 = 0
    Gauss_4 = 1
    Gauss_8 = 2
    Gauss_12 = 3

    @property
    def scaling_factor(self):
        """
        The scaling factor based on the sensor full scale.

        :return: The scaling factor expressed in mgauss/digit.
        """
        if self == MagScale.Gauss_2:
            return 0.080
        elif self == MagScale.Gauss_4:
            return 0.160
        elif self == MagScale.Gauss_8:
            return 0.320
        elif self == MagScale.Gauss_12:
            return 0.479
        else:
            return 0.0


class LSM303D:

    # The physical I2C address of the MEMS
    address = 0x1D
    # The accelerometer axis output registers
    accel_axis_output_registers = [
        Registers.OUT_X_L_A,
        Registers.OUT_X_H_A,
        Registers.OUT_Y_L_A,
        Registers.OUT_Y_H_A,
        Registers.OUT_Z_L_A,
        Registers.OUT_Z_H_A,
    ]
    # The magnetometer axis output register
    mag_axis_output_registers = [
        Registers.OUT_X_L_M,
        Registers.OUT_X_H_M,
        Registers.OUT_Y_L_M,
        Registers.OUT_Y_H_M,
        Registers.OUT_Z_L_M,
        Registers.OUT_Z_H_M,
    ]

    def __init__(self, accel_scale, mag_scale):
        self.accel_scale = accel_scale
        self.mag_scale = mag_scale
