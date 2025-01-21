import math


class Rope:

    def __init__(self, location, l, k):
        self.length = l
        self.x = location[0]
        self.y = location[1]
        self.k = k

    def get_position(self):
        return self.x, self.y

    def get_force(self, location):
        delta_x, delta_y = self.x - location[0], self.y - location[1]
        total_length = math.sqrt(delta_x**2 + delta_y**2)
        delta_l = total_length - self.length
        if total_length <= self.length:
            return 0, 0
        force = self.k * delta_l
        f_x = (delta_x / total_length) * force
        f_y = (delta_y / total_length) * force
        return f_x, f_y

