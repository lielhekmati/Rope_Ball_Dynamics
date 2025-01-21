class Ball:
    def __init__(self, radius, location, mass):

        self.x = location[0]
        self.y = location[1]

        self.vel_x = 7
        self.vel_y = 0

        self.a_x = 0
        self.a_y = 0

        self.radius = radius
        self.mass = mass

    def get_position(self):
        return self.x, self.y

    def get_velocity(self):
        return self.vel_x, self.vel_y

    def get_radius(self):
        return self.radius

    def get_mass(self):
        return self.mass

    def set_velocity(self, vel_x, vel_y):
        self.vel_x = vel_x
        self.vel_y = vel_y

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def update_position(self, f_x=0, f_y=0, t=1/100):

        self.a_x = f_x / self.mass
        self.a_y = f_y / self.mass

        self.vel_x += self.a_x * t
        self.vel_y += self.a_y * t

        self.x += self.vel_x * t + 0.5 * self.a_x * t**2
        self.y += self.vel_y * t + 0.5 * self.a_y * t**2



