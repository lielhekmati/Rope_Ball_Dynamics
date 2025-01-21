import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Simulation:
    """
    A class to simulate a physics-based environment with balls connected by ropes.

    Attributes:
        balls (list): A list of Ball objects in the simulation.
        ropes (list): A list of Rope objects in the simulation.
        bounds (tuple): The boundary limits as (upper, lower, left, right).
        frame_count (int): The total number of frames for the animation.
        frame_interval (float): Time interval between frames in seconds.
        fig (matplotlib.figure.Figure): The figure for the simulation plot.
        ax (matplotlib.axes._axes.Axes): The axes for the simulation plot.
        ball_visualizations (list): Visual representations of the balls.
        rope_visualizations (list): Visual representations of the ropes.
    """
    def __init__(self, balls, ropes, bounds, frame_count, frame_interval):
        """
        Initializes the simulation environment.

        Args:
            balls (list): A list of Ball objects.
            ropes (list): A list of Rope objects.
            bounds (tuple): Tuple specifying (upper, lower, left, right) boundary limits.
            frame_count (int): Total number of frames in the animation.
            frame_interval (float): Time interval between frames in seconds.
        """
        self.balls = balls
        self.ropes = ropes
        self.bounds = bounds
        self.frame_count = frame_count
        self.frame_interval = frame_interval

        # Set up the figure and axes for the animation
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(bounds[2], bounds[3])  # Set x-axis limits
        self.ax.set_ylim(bounds[1], bounds[0])  # Set y-axis limits
        self.ax.set_aspect('equal')  # Equal scaling for x and y axes

        # Visualization placeholders
        self.ball_visualizations = []  # Stores ball visual elements
        self.rope_visualizations = []  # Stores rope visual elements

        # Initialize visual elements
        self.setup_balls_visualization()
        self.setup_ropes_visualization()
        self.setup_visuals()

    def setup_balls_visualization(self):
        """ Creates the visual representation of the balls and stores them."""
        color_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22']
        for i, ball in enumerate(self.balls):
            visualization = plt.Circle(ball.get_position(), ball.get_radius(), color=color_list[i])
            self.ball_visualizations.append(visualization)

    def setup_ropes_visualization(self):
        """ Creates the visual representation of the ropes and stores them."""
        for i, rope in enumerate(self.ropes):
            visualization = self.ax.plot([rope.x, rope.y], [self.balls[i].x, self.balls[i].y], color='black')[0]
            self.rope_visualizations.append(visualization)

    def setup_visuals(self):
        """ Adds the visual elements of balls and ropes to the plot."""
        for ball_visualization in self.ball_visualizations:
            self.ax.add_patch(ball_visualization)
        for rope_visualization in self.rope_visualizations:
            self.ax.add_line(rope_visualization)

    def update(self, frame):
        """ Updates the positions of balls and ropes for each animation frame."""
        # Update ball positions based on forces
        for i in range(len(self.balls)):
            f_x_rope, f_y_rope = self.ropes[i].get_force(self.balls[i].get_position())
            mass = self.balls[i].get_mass()
            sigma_f_x = f_x_rope
            sigma_f_y = f_y_rope - mass * 9.8  # Include gravitational force
            self.balls[i].update_position(sigma_f_x, sigma_f_y)

        # Check collisions with walls
        for ball in self.balls:
            ball.check_collision_with_walls(10, 0, -10, 10)

        # Check collisions between balls
        if len(self.balls) == 2:
            self.balls[0].check_collision_between_balls(self.balls[1])
        if len(self.balls) > 2:
            for i in range(len(self.balls)):
                for j in range(i+1, len(self.balls)):
                    self.balls[i].check_collision_between_balls(self.balls[j])

        # Update visual elements
        for i, ball_visualization in enumerate(self.ball_visualizations):
            ball_visualization.set_center(self.balls[i].get_position())
        for i, rope_visualization in enumerate(self.rope_visualizations):
            x_ball, y_ball = self.balls[i].get_position()
            x_rope, y_rope = self.ropes[i].get_position()
            rope_visualization.set_data([x_rope, x_ball], [y_rope, y_ball])

        return self.ball_visualizations + self.rope_visualizations

    def run(self):
        """update the simulation at each frame"""
        ani = animation.FuncAnimation(
            self.fig,
            self.update,  # No need for partial
            frames=self.frame_count,
            interval=self.frame_interval,  # Convert seconds to milliseconds
            blit=True
        )
        plt.show()
