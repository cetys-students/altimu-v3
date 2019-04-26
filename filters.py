class LowPassFilter:

    def __init__(self, measurement, bias):
        self.measurement = measurement
        self.bias = bias

    def update_measurement(self, new_measurement):
        self.measurement[0] = (self.measurement[0] * self.bias) + (new_measurement[0] * (1 - self.bias))
        self.measurement[1] = (self.measurement[1] * self.bias) + (new_measurement[1] * (1 - self.bias))
        self.measurement[2] = (self.measurement[2] * self.bias) + (new_measurement[2] * (1 - self.bias))

        return self.measurement


class HighPassFilter:

    def __init__(self, measurement, bias):
        self.measurement = measurement
        self.bias = bias

    def update_measurement(self, new_measurement):
        self.measurement[0] = self.measurement[0] + self.bias * (new_measurement[0] - self.measurement[0])
        self.measurement[1] = self.measurement[1] + self.bias * (new_measurement[1] - self.measurement[1])
        self.measurement[2] = self.measurement[2] + self.bias * (new_measurement[2] - self.measurement[2])

        return self.measurement
