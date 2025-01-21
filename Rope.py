import math


class Rope:
    """
    Represents a rope in the simulation that connects an anchor point to a ball.

    Attributes:
        x (float): The x-coordinate of the anchor point.
        y (float): The y-coordinate of the anchor point.
        length (float): The length of the rope.
        k (float): The spring constant of the rope.
    """
    def __init__(self, anchor_point, length, k):
        """
        Initializes a Rope instance.

        Args:
            anchor_point (tuple): The (x, y) coordinates of the anchor point.
            length (float): The length of the rope.
            k (float): The spring constant of the rope.
        """
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
        """ Calculates the force exerted by the rope on an object at a given location."""
        delta_x, delta_y = self.x - location[0], self.y - location[1]
        total_length = math.sqrt(delta_x**2 + delta_y**2)
        if total_length <= self.length:
            return 0, 0
        delta_l = total_length - self.length
        force = self.k * delta_l  # Hooke's law force

        # Normalize the force direction to the rope's direction
        f_x = (delta_x / total_length) * force
        f_y = (delta_y / total_length) * force
        return f_x, f_y

