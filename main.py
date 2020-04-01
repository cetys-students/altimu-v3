from AltIMU_v3 import AltIMUv3
from filters import LowPassFilter, HighPassFilter
from time import sleep
from graph_manager import GraphManager

# Setup Altimu
altimu = AltIMUv3()
altimu.enable()

# Graph Manager
graph_manager = GraphManager('Gyro Test', 'Time')

# Initialize a low pass filter with a default value and a bias of 80%
low_pass_filter = LowPassFilter([0.0, 0.0, 1.0], 0.8)

# Initialize a high pass filter with a default value and a bias of 80%
high_pass_filter = HighPassFilter([0.0, 0.0, 0.0], 0.8)

samples_x = []
samples_y = []
samples_z = []
for i in range(0, 1000):

    # Calibrated Accelerometer
    accel = altimu.get_accelerometer_cal()

    # Estimated gravity
    estimated_gravity = low_pass_filter.update_measurement(accel)

    # Estimated linear acceleration
    linear_x = accel[0] - estimated_gravity[0]
    linear_y = accel[1] - estimated_gravity[1]
    linear_z = accel[2] - estimated_gravity[2]

    # Calibrated Gyro
    gyro = altimu.get_gyro_cal()

    # Undrifted Gyro
    # undrifted_gyro = high_pass_filter.update_measurement(gyro)

    # print(f"Accel\tx: {accel[0]: .6f}\ty: {accel[1]: .6f}\tz: {accel[2]: .6f} [g]")
    # print(f"Gravity\tx: {estimated_gravity[0]: .6f}\ty: {estimated_gravity[1]: .6f}\tz: {estimated_gravity[2]: .6f} [g]")
    # print(f"LinearA\tx: {linear_x: .6f}\ty: {linear_y: .6f}\tz: {linear_z: .6f} [g]")
    print(f"gyro\tx: {gyro[0]: .6f}\ty: {gyro[1]: .6f}\tz: {gyro[2]: .6f} [dps]")

    samples_x.append(gyro[0])
    samples_y.append(gyro[1])
    samples_z.append(gyro[2])
    sleep(0.01)

graph_manager.add_data_set(name='lax (g)', y_values=samples_x, color='red', dash='solid')
graph_manager.add_data_set(name='lay (g)', y_values=samples_y, color='green', dash='solid')
graph_manager.add_data_set(name='laz (g)', y_values=samples_z, color='blue', dash='solid')
graph_manager.show()
