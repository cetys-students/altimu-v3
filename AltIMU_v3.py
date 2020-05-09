from I2C import I2C
from LSM303D import LSM303D, AccelScale, MagScale
from LSM303D import Registers as LSM303DRegisters
from L3GD20H import L3GD20H, GyroScale
from L3GD20H import Registers as L3GD20HRegisters


class AltIMUv3(I2C):

    def __init__(self,
                 accel_scale=AccelScale.G_2,
                 mag_scale=MagScale.Gauss_4,
                 gyro_scale=GyroScale.DPS_2000,
                 bus_id=1):
        """ 
        Set up I2C connection and initialize some flags and values.
        """

        super(AltIMUv3, self).__init__(bus_id)
        self.accel_mems = LSM303D(accel_scale, mag_scale)
        self.gyro_mems = L3GD20H(gyro_scale)

    def __del__(self):
        """ 
        Clean up.
        """
        try:
            # Power down MEMS
            self.write_register(self.accel_mems.address, LSM303DRegisters.CTRL1, 0x00)
            self.write_register(self.accel_mems.address, LSM303DRegisters.CTRL7, 0x03)

            super(AltIMUv3, self).__del__()
        except:
            pass

    def enable(self):

        # Accelerometer ODR selection and enable (800 Hz)
        self.write_register(self.accel_mems.address, LSM303DRegisters.CTRL1, 0x97)

        # Accelerometer FS selection
        ctrl_2_value = self.accel_mems.accel_scale << 3
        self.write_register(self.accel_mems.address, LSM303DRegisters.CTRL2, ctrl_2_value)

        # Magnetometer enable
        self.write_register(self.accel_mems.address, LSM303DRegisters.CTRL7, 0x00)

        # Magnetometer ODR selection (50Hz)
        self.write_register(self.accel_mems.address, LSM303DRegisters.CTRL5, 0x70)

        # Magnetometer FS selection
        ctrl_6_value = self.accel_mems.mag_scale << 5
        self.write_register(self.accel_mems.address, LSM303DRegisters.CTRL6, ctrl_6_value)

        # Gyro ODR Selection (800 Hz)
        self.write_register(self.gyro_mems.address, L3GD20HRegisters.CTRL1, 0xCF)

        # Gyro FS selection (2000 dps)
        self.write_register(self.gyro_mems.address, L3GD20HRegisters.CTRL4, 0x30)

    def get_accelerometer_raw(self):
        """
        Return a 3D vector of raw accelerometer data.
        """

        return self.read_sensor(self.accel_mems.address,
                                self.accel_mems.accel_axis_output_registers)

    def get_accelerometer_cal(self):
        """
        Return a 3D vector of calibrated accelerometer data.
        """
        raw = self.get_accelerometer_raw()
        scaling = self.accel_mems.accel_scale.scaling_factor / 1000

        cal_x = raw[0] * scaling
        cal_y = raw[1] * scaling
        cal_z = raw[2] * scaling

        return [cal_x, cal_y, cal_z]

    def get_gyro_raw(self):
        """
        Return a 3D vector of raw gyro data.
        """

        return self.read_sensor(self.gyro_mems.address,
                                self.gyro_mems.axis_output_registers)

    def get_gyro_cal(self, bias=[0,0,0]):
        """
        Return a 3D vector of calibrated accelerometer data.
        """
        raw = self.get_gyro_raw()
        scaling = self.gyro_mems.gyro_scale.scaling_factor / 1000

        cal_x = (raw[0] * scaling) - bias[0]
        cal_y = (raw[1] * scaling) - bias[1]
        cal_z = (raw[2] * scaling) - bias[2]

        return [cal_x, cal_y, cal_z]