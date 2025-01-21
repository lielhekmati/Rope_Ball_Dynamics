import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Simulation:
    def __init__(self, balls, ropes, bounds, frame_count, frame_interval):

        self.balls = balls
        self.ropes = ropes
        self.bounds = bounds
        self.frame_count = frame_count
        self.frame_interval = frame_interval

        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(bounds[2], bounds[3])
        self.ax.set_ylim(bounds[1], bounds[0])
        self.ax.set_aspect('equal')

        # Visualization
        self.ball_visualizations = []
        self.rope_visualizations = []

        self.setup_balls_visualization()
        self.setup_ropes_visualization()
        self.setup_visuals()

    def setup_balls_visualization(self):
        color_list = ['red', 'blue', 'green']
        for i, ball in enumerate(self.balls):
            visualization = plt.Circle(ball.get_position(), ball.get_radius(), color=color_list[i])
            self.ball_visualizations.append(visualization)

    def setup_ropes_visualization(self):
        for i, rope in enumerate(self.ropes):
            visualization = self.ax.plot([rope.x, rope.y], [self.balls[i].x, self.balls[i].y], color='black')[0]
            self.rope_visualizations.append(visualization)

    def setup_visuals(self):
        for ball_visualization in self.ball_visualizations:
            self.ax.add_patch(ball_visualization)
        for rope_visualization in self.rope_visualizations:
            self.ax.add_line(rope_visualization)

    def update(self, frame):

        for i in range(len(self.balls)):
            f_x_rope, f_y_rope = self.ropes[i].get_force(self.balls[i].get_position())
            mass = self.balls[i].get_mass()
            sigma_f_x = f_x_rope
            sigma_f_y = f_y_rope - mass * 9.8
            self.balls[i].update_position(sigma_f_x, sigma_f_y)

        for ball in self.balls:
            ball.check_collision_with_walls(10, 0, -10, 10)
        if len(self.balls) == 2:
            self.balls[0].check_collision_between_balls(self.balls[1])
        if len(self.balls) == 3:
            self.balls[0].check_collision_between_balls(self.balls[1])
            self.balls[0].check_collision_between_balls(self.balls[2])
            self.balls[1].check_collision_between_balls(self.balls[2])
        for i, ball_visualization in enumerate(self.ball_visualizations):
            ball_visualization.set_center(self.balls[i].get_position())
        for i, rope_visualization in enumerate(self.rope_visualizations):
            x_ball, y_ball = self.balls[i].get_position()
            x_rope, y_rope = self.ropes[i].get_position()
            rope_visualization.set_data([x_rope, x_ball], [y_rope, y_ball])
        return self.ball_visualizations + self.rope_visualizations

    def run(self):
        ani = animation.FuncAnimation(
            self.fig,
            self.update,  # No need for partial
            frames=self.frame_count,
            interval=self.frame_interval,  # Convert seconds to milliseconds
            blit=True
        )
        plt.show()
