import math
from AltIMU_v3 import AltIMUv3
from time import sleep
from graph_manager import GraphManager

print('Initializing...')

# Setup Altimu
altimu = AltIMUv3()
altimu.enable()

# Graph Manager
graph_manager = GraphManager('Filter Test', 'Time')

# Initialize angles
alpha = 0
beta = 0
gamma = 0

# Miscellaneous Properties
sampling_period = 0.01
bias = 0.98

# Calibration procedure
bias_gyro_x = 0
bias_gyro_y = 0
bias_gyro_z = 0
calibration_data_samples = 500
print('Calibrating...')
for i in range(calibration_data_samples):
    gyro = altimu.get_gyro_cal()
    bias_gyro_x += gyro[0]
    bias_gyro_y += gyro[1]
    bias_gyro_z += gyro[2]
    sleep(sampling_period)
bias_gyro_x /= calibration_data_samples
bias_gyro_y /= calibration_data_samples
bias_gyro_z /= calibration_data_samples

# Filtering procedure (Note, this would be real time data)
gyro_angle_x_set = []
gyro_angle_y_set = []
accel_angle_x_set = []
accel_angle_y_set = []
comp_angle_x_set = []
comp_angle_y_set = []
print('Sampling...')
for i in range(1000):

    # Calibrated Readings
    accel = altimu.get_accelerometer_cal()
    gyro = altimu.get_gyro_cal([bias_gyro_x, bias_gyro_y, bias_gyro_z])

    # Gyro Angles
    gyro_angle_x = gyro[0] * sampling_period
    gyro_angle_y = gyro[1] * sampling_period
    gyro_angle_z = gyro[2] * sampling_period

    # Accel Angles
    accel_angle_x = math.atan2(accel[0], math.sqrt((accel[1] * accel[1]) + (accel[2] * accel[2])))
    accel_angle_y = math.atan2(accel[1], math.sqrt((accel[0] * accel[0]) + (accel[2] * accel[2])))

    # Complementary Filter
    alpha = alpha + gyro_angle_z
    beta = bias * (beta + gyro_angle_x) + (1.0 - bias) * accel_angle_x
    gamma = bias * (beta + gyro_angle_y) + (1.0 - bias) * accel_angle_y

    # Plotting Data Sets
    gyro_angle_x_set.append(gyro_angle_x)
    gyro_angle_y_set.append(gyro_angle_y)
    accel_angle_x_set.append(accel_angle_x)
    accel_angle_y_set.append(accel_angle_y)
    comp_angle_x_set.append(beta)
    comp_angle_y_set.append(gamma)

    sleep(sampling_period)

print('Generating plots...')
graph_manager.add_data_set(name='gyro x', y_values=gyro_angle_x_set, color='blue', dash='solid')
graph_manager.add_data_set(name='gyro y', y_values=gyro_angle_y_set, color='navy', dash='solid')
graph_manager.add_data_set(name='accel x', y_values=accel_angle_x_set, color='green', dash='solid')
graph_manager.add_data_set(name='accel y', y_values=accel_angle_y_set, color='lime', dash='solid')
graph_manager.add_data_set(name='comp x', y_values=comp_angle_x_set, color='red', dash='solid')
graph_manager.add_data_set(name='comp y', y_values=comp_angle_y_set, color='maroon', dash='solid')
graph_manager.show()

print('Done...')