Rope-and-Ball Simulation

Project Overview:
This project simulates the interaction between balls connected to ropes, constrained within a bounded area. 
The simulation visualizes dynamic behaviors such as collisions, forces exerted by ropes, and the response of balls to these forces and boundaries.

Features:
- Dynamic Ball Movement: Balls respond to forces from ropes and collisions with walls and other balls.
- Elastic Rope Forces: Ropes exert force when stretched beyond their natural length, following Hooke's law.
- Wall and Ball Collisions: Balls collide with walls and each other, conserving momentum during collisions.
- Real-Time Visualization: The simulation is animated using Matplotlib for an interactive view of the system.

Running the Simulation:
1. Define Balls: Create instances of the Ball class with desired properties (e.g., mass, position, velocity).
2. Define Ropes: Create instances of the Rope class, specifying anchor points, length, and elasticity.
3. Set Bounds: Specify the simulation's bounding box as (upper, lower, left, right).
4. Initialize Simulation: Pass the balls, ropes, and bounds to the Simulation class along with the frame count and interval.
5. Run the Simulation: Call the run() method to start the animation.
