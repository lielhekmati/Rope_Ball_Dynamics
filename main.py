from Ball import Ball
from Rope import Rope
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functools import partial
import math


def momentum_calc(v1, m1, v2, m2):
    u1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
    u2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
    return u1, u2


def collision(obj1, obj2):
    v1_x, v1_y = obj1.get_velocity()
    mass1 = obj1.get_mass()
    if isinstance(obj2, str):
        if obj2 == 'x':
            obj1.set_velocity(v1_x, -v1_y)
        elif obj2 == 'y':
            obj1.set_velocity(-v1_x, v1_y)

    elif isinstance(obj2, Ball):
        # Handle ball-to-ball collisions
        v2_x, v2_y = obj2.get_velocity()
        mass2 = obj2.get_mass()
        ux_1, ux_2 = momentum_calc(v1_x, mass1, v2_x, mass2)
        uy_1, uy_2 = momentum_calc(v1_y, mass1, v2_y, mass2)

        obj1.set_velocity(ux_1 , uy_1 * 0.98)
        obj2.set_velocity(ux_2, uy_2 * 0.98)


def find_reposition_point(ball1 , ball2):
    x1, y1 = ball1.get_position()
    x2, y2 = ball2.get_position()
    r1 = ball1.get_radius()
    r2 = ball2.get_radius()
    gradient = (y2 - y1) / (x2 - x1)
    x = x1 + (r1 + r2)/math.sqrt(1+gradient**2)
    y = gradient * (x - x1) + y1
    return x, y


def check_collision_between_balls(ball1, ball2):
    x1, y1 = ball1.get_position()
    x2, y2 = ball2.get_position()
    r1 = ball1.get_radius()
    r2 = ball2.get_radius()
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    merged = is_merged([ball1, ball2])
    if distance <= r1 + r2:
        print('collision')
        if x1 < x2:
            x, y = find_reposition_point(ball1, ball2)
            ball2.set_position(x, y)
        else:
            x, y = find_reposition_point(ball2, ball1)
            ball1.set_position(x, y)
        if not merged:
            collision(ball1, ball2)






def check_collision_with_walls(ball, upper, lower, left, right):
    x, y = ball.get_position()
    r = ball.get_radius()

    # Check for wall collisions and adjust positions
    if y - r < lower:
        collision(ball, 'x')
        ball.set_position(x, lower + r)
    elif y + r > upper:
        collision(ball, 'x')
        ball.set_position(x, upper - r)

    if x - r < left:
        collision(ball, 'y')
        ball.set_position(left + r, y)
    elif x + r > right:
        collision(ball, 'y')
        ball.set_position(right - r, y)

def is_merged(balls):

    velocity_threshold = 0.3
    distance_threshold = 1
    v1_x, v1_y = balls[0].get_velocity()
    v2_x, v2_y = balls[1].get_velocity()
    x1, y1 = balls[0].get_position()
    x2, y2 = balls[1].get_position()
    r1 = balls[0].get_radius()
    r2 = balls[1].get_radius()

    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    relative_velocity = math.sqrt((v1_y - v2_y)**2 + (v1_x - v2_x)**2)

    if abs(r1+r2 - distance) < distance_threshold and abs(relative_velocity) < velocity_threshold:
        print(1)
        return True

    return False


def update(frame, balls, ropes, ball_visualizations, rope_visualizations):

    for i in range(len(balls)):
        f_x_rope, f_y_rope = ropes[i].get_force(balls[i].get_position())
        mass = balls[i].get_mass()
        sigma_f_x = f_x_rope
        sigma_f_y = f_y_rope - mass * 9.8
        balls[i].update_position(sigma_f_x, sigma_f_y)

    for ball in balls:
        check_collision_with_walls(ball, 10, 0, -10, 10)
    check_collision_between_balls(balls[0], balls[1])


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
    ball1 = Ball(1.5, [0, 5], 3)
    ball2 = Ball(1, [5, 5], 3)

    rope1 = Rope([1, 10], 7, 50)
    rope2 = Rope([1, 10], 7, 50)

    balls = [ball1, ball2]
    ropes = [rope1, rope2]
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


print("hello")