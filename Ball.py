import math


def momentum_calc(v1, m1, v2, m2):
    u1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
    u2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
    return u1, u2


class Ball:

    def __init__(self, radius, location, mass, velocity):
        """
        Initializes a Ball instance.

        Args:
            radius (float): The radius of the ball.
            location (tuple): The initial (x, y) position of the ball.
            mass (float): The mass of the ball.
            velocity (tuple): The initial (vel_x, vel_y) velocity of the ball.
        """
        self.x = location[0]
        self.y = location[1]

        self.vel_x = velocity[0]
        self.vel_y = velocity[1]

        self.a_x = 0
        self.a_y = 0

        self.radius = radius
        self.mass = mass

    def get_position(self):
        """ Returns the position of the ball on x,y axes"""
        return self.x, self.y

    def get_velocity(self):
        """ Returns the ball's velocity components in x,y axes"""
        return self.vel_x, self.vel_y

    def get_radius(self):
        """ Return the radius of the ball"""
        return self.radius

    def get_mass(self):
        """ Return the mass of the ball"""
        return self.mass

    def set_velocity(self, vel_x, vel_y):
        """Gets velocity components in x,y axes
           Sets the ball's velocity components in x,y axes"""

        self.vel_x = vel_x
        self.vel_y = vel_y

    def set_position(self, x, y):
        """Gets location components in x,y axes
           Sets the ball's location components in x,y axes"""
        self.x = x
        self.y = y

    def update_position(self, f_x=0, f_y=0, t=1/100):
        """ Updates the ball's position based on given applied forces components in x,y axes and time step."""
        self.a_x = f_x / self.mass
        self.a_y = f_y / self.mass

        self.vel_x += self.a_x * t
        self.vel_y += self.a_y * t

        self.x += self.vel_x * t + 0.5 * self.a_x * t**2
        self.y += self.vel_y * t + 0.5 * self.a_y * t**2

    def collision(self, obj2):
        """ Handles collisions with obj2 that can be a wall or another ball."""
        if isinstance(obj2, str):
            # Handle ball-to-ball collisions
            if obj2 == 'x':
                self.set_velocity(self.vel_x, -self.vel_y)
            elif obj2 == 'y':
                self.set_velocity(-self.vel_x, self.vel_y)

        elif isinstance(obj2, Ball):
            # Handle ball-to-ball collisions
            v2_x, v2_y = obj2.get_velocity()
            mass2 = obj2.get_mass()
            ux_1, ux_2 = momentum_calc(self.vel_x, self.mass, v2_x, mass2)
            uy_1, uy_2 = momentum_calc(self.vel_y, self.mass, v2_y, mass2)

            self.set_velocity(ux_1, uy_1 * 0.95)
            obj2.set_velocity(ux_2, uy_2 * 0.95)

    def check_collision_with_walls(self, upper, lower, left, right):
        """ Checks and resolves collisions with the simulation boundaries."""
        x, y = self.get_position()
        r = self.get_radius()

        # Check for wall collisions and adjust positions
        if y - r < lower:
            self.collision('x')
            self.set_position(x, lower + r)
        elif y + r > upper:
            self.collision('x')
            self.set_position(x, upper - r)

        if x - r < left:
            self.collision('y')
            self.set_position(left + r, y)
        elif x + r > right:
            self.collision('y')
            self.set_position(right - r, y)

    def check_collision_between_balls(self, ball2):
        """ Checks and resolves collisions with another ball."""
        x1, y1 = self.get_position()
        x2, y2 = ball2.get_position()
        r1 = self.get_radius()
        r2 = ball2.get_radius()
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        #merged = self.is_merged(ball2)
        if distance <= r1 + r2:
            x, y = self.find_reposition_point(ball2)
            ball2.set_position(x, y)
            #if not merged:
            #    self.collision(ball2)
            self.collision(ball2)

    def find_reposition_point(self, ball2):
        """ Finds a new position for another ball to resolve overlap after a collision."""
        x1, y1 = self.get_position()
        x2, y2 = ball2.get_position()
        r1 = self.get_radius()
        r2 = ball2.get_radius()
        gradient = (y2 - y1) / (x2 - x1)
        if x1 < x2:
            x = x1 + (r1 + r2)/(1+gradient**2)**0.5
        else:
            x = x1 - (r1 + r2) / (1 + gradient ** 2) ** 0.5
        y = gradient * (x - x1) + y1
        return x, y

    def is_merged(self, ball):
        """ Determines if two balls have merged based on velocity and distance thresholds."""
        """This function is not used in the code but can be used in cases where the balls are vibrating in the simulation.
        you can find its usage in check_collision_between_balls function disabled with #
        """
        velocity_threshold = -1
        distance_threshold = 1
        v1_x, v1_y = self.get_velocity()
        v2_x, v2_y = ball.get_velocity()
        x1, y1 = self.get_position()
        x2, y2 = ball.get_position()
        r1 = self.get_radius()
        r2 = ball.get_radius()

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        relative_velocity = math.sqrt((v1_y - v2_y) ** 2 + (v1_x - v2_x) ** 2)

        if abs(r1 + r2 - distance) < distance_threshold and relative_velocity < velocity_threshold:
            print(1)
            return True

        return False
