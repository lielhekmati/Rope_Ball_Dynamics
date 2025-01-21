import math


class Rope:

    def __init__(self, anchor_point, length, k):
        self.length = length
        self.x = anchor_point[0]
        self.y = anchor_point[1]
        self.k = k

    def get_position(self):
        return self.x, self.y

    def set_position(self,x_anchor, y_anchor):
        self.x = x_anchor
        self.y = y_anchor

    def get_force(self, location):
        delta_x, delta_y = self.x - location[0], self.y - location[1]
        total_length = math.sqrt(delta_x**2 + delta_y**2)
        if total_length <= self.length:
            return 0, 0
        delta_l = total_length - self.length
        force = self.k * delta_l
        f_x = (delta_x / total_length) * force
        f_y = (delta_y / total_length) * force
        return f_x, f_y

