from Ball import Ball
from Rope import Rope
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functools import partial


def update(frame, balls, ropes, ball_visualizations, rope_visualizations):

    for i in range(len(balls)):
        f_x_rope, f_y_rope = ropes[i].get_force(balls[i].get_position())
        mass = balls[i].get_mass()
        # calculating sum of forces on both axises
        sigma_f_x = f_x_rope
        sigma_f_y = f_y_rope - mass * 9.8
        balls[i].update_position(sigma_f_x, sigma_f_y)

    for ball in balls:
        ball.check_collision_with_walls(10, 0, -10, 10)
    balls[0].check_collision_between_balls(balls[1])

    for i, ball_visualization in enumerate(ball_visualizations):
        ball_visualization.set_center(balls[i].get_position())
    for i, rope_visualization in enumerate(rope_visualizations):
        x_ball, y_ball = balls[i].get_position()
        x_rope, y_rope = ropes[i].get_position()
        rope_visualization.set_data([x_rope, x_ball], [y_rope, y_ball])
    return ball_visualizations + rope_visualizations


if __name__ == '__main__':
    flag = False
    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')

    # Create the balls and their visualizations
    ball1 = Ball(2, [0, 5], 3, [7, 0])
    ball2 = Ball(1, [5, 5], 5, [7, 0])
    # Create the Ropes
    rope1 = Rope([1, 10], 7, 50)
    rope2 = Rope([1, 10], 7, 50)

    balls = [ball1, ball2]
    ropes = [rope1, rope2]

    # Create the balls and their visualizations
    ball_visualizations = [
        plt.Circle(ball1.get_position(), ball1.radius, color='red'),
        plt.Circle(ball2.get_position(), ball2.radius, color='blue'),
    ]
    rope_visualizations = [
        ax.plot([rope1.x, rope1.y], [ball1.x, ball1.y], color='black')[0],
        ax.plot([rope2.x, rope2.y], [ball2.x, ball2.y], color='black')[0]
    ]

    # Add ball visualizations to the plot
    for ball_visualization in ball_visualizations:
        ax.add_patch(ball_visualization)

    # Add rope visualizations to the plot
    for rope_visualization in rope_visualizations:
        ax.add_line(rope_visualization)

    # Use partial to pass the balls and visualizations to the update function
    ani = animation.FuncAnimation(
        fig,
        partial(update, balls=balls, ropes=ropes, ball_visualizations=ball_visualizations, rope_visualizations=rope_visualizations),
        frames=200,
        interval=(1 / 200),
        blit=True
    )

    plt.show()


