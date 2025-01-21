from Ball import Ball
from Rope import Rope
from Simulation import Simulation


if __name__ == '__main__':
    # Define the balls
    ball1 = Ball(2, [0, 5], 3, [7, 0])
    ball2 = Ball(1, [5, 5], 5, [7, 0])
    ball3 = Ball(1, [7, 5], 5, [7, 0])

    # Define the ropes
    rope1 = Rope([1, 10], 7, 50)
    rope2 = Rope([1, 10], 7, 50)
    rope3 = Rope([1, 10], 7, 50)

    # Create the simulation
    sim = Simulation(
        balls=[ball1, ball2, ball3],
        ropes=[rope1, rope2, rope3],
        bounds=(10, 0, -10, 10),  # Upper, lower, left, right bounds
        frame_count=200,
        frame_interval=1/200
    )

    sim.run()

