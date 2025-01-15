import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)  # For waypoints

# Box properties
box_size = 40
box_speed = .8  # Maximum speed
deviation_distance = 1 # Distance for RRT deviation
waypoint_tolerance = 10
goal_bias = 0.2  # Probability of choosing the goal as the random sample
collision_radius = box_size + 60  # Minimum safe distance
rrt_star_radius = 100  # Radius for RRT* rewiring
rewire = True  # Switch to enable or disable rewiring

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RRT* with Collision Avoidance")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def avoid_collision(pos1, pos2, direction1, direction2):
    """Adjust paths to avoid collisions dynamically."""
    if distance(pos1, pos2) < collision_radius:
        # Adjust the paths
        pos1[1] += deviation_distance if direction1[0] > 0 else -deviation_distance
        pos2[1] -= deviation_distance if direction2[0] < 0 else deviation_distance

def generate_rrt_path(start, goal, other_pos, max_iter=200  ):
    """Generate a RRT* path with goal bias."""
    nodes = {tuple(start): None}  # Dictionary to store nodes and their parents
    for _ in range(max_iter):
        if random.random() < goal_bias:
            rand_point = goal
        else:
            rand_point = (
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT)
            )

        nearest_node = find_nearest_node(nodes, rand_point)
        new_node = steer(nearest_node, rand_point)
        if not velocity_obstacle(new_node, (0, 0), other_pos, (0, 0)):
            nodes[tuple(new_node)] = nearest_node
            if distance(new_node, goal) < waypoint_tolerance:
                # Backtrack to reconstruct the path
                waypoints = [new_node]
                current_node = new_node
                while current_node != start:
                    current_node = nodes[tuple(current_node)]
                    waypoints.insert(0, current_node)
                return waypoints

    return [start, goal]

def find_nearest_node(nodes, point):
    """Find the nearest node in the RRT to a given point."""
    nearest_dist = float('inf')
    nearest_node = None
    for node in nodes:
        dist = distance(node, point)
        if dist < nearest_dist:
            nearest_dist = dist
            nearest_node = node
    return nearest_node

def steer(from_node, to_pos):
    """Steers from a node towards a point using a constant step size."""
    direction = [to_pos[0] - from_node[0], to_pos[1] - from_node[1]]
    dist = distance(from_node, to_pos)
    if dist < deviation_distance:
        return to_pos
    unit_dir = [deviation_distance * (direction[0] / dist), deviation_distance * (direction[1] / dist)]
    return (from_node[0] + unit_dir[0], from_node[1] + unit_dir[1])

def calculate_velocity(current_pos, next_waypoint):
    """Calculate the velocity to move towards a given waypoint."""
    direction = [next_waypoint[0] - current_pos[0], next_waypoint[1] - current_pos[1]]
    dist = distance(current_pos, next_waypoint)
    if dist == 0:
        return [0, 0]
    return [box_speed * (direction[0] / dist), box_speed * (direction[1] / dist)]

def velocity_obstacle(pos1, vel1, pos2, vel2):
    """Check for collision avoidance using velocity obstacles."""
    d_cpa = distance(pos1, pos2)
    return d_cpa < collision_radius

def update_position_and_path(box_pos, box_path, box_vel, other_pos):
    """Update the box's position and adjust the path dynamically if necessary."""
    if box_path:
        target = box_path[0]
        if distance(box_pos, target) < waypoint_tolerance:
            box_path.pop(0)
        else:
            box_vel = calculate_velocity(box_pos, target)
            box_pos[0] += box_vel[0]
            box_pos[1] += box_vel[1]
    return box_pos, box_path, box_vel

# Define start and goal positions for the head-on scenario
start_pos_red = (100, HEIGHT // 2)  # Red box starts on the left
goal_pos_red = (WIDTH - 100, HEIGHT // 2)  # Red box moves to the right
start_pos_blue = (WIDTH - 100, HEIGHT // 2)  # Blue box starts on the right
goal_pos_blue = (100, HEIGHT // 2)  # Blue box moves to the left

# Initialize positions and paths
red_pos = list(start_pos_red)
blue_pos = list(start_pos_blue)
red_path = generate_rrt_path(start_pos_red, goal_pos_red, tuple(blue_pos))
blue_path = generate_rrt_path(start_pos_blue, goal_pos_blue, tuple(red_pos))
red_vel = [0, 0]
blue_vel = [0, 0]
moving = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                moving = True

    if moving:
        # Avoid collision before updating positions
        avoid_collision(red_pos, blue_pos, red_vel, blue_vel)

        # Update positions and paths for both boxes
        red_pos, red_path, red_vel = update_position_and_path(red_pos, red_path, red_vel, blue_pos)
        blue_pos, blue_path, blue_vel = update_position_and_path(blue_pos, blue_path, blue_vel, red_pos)

        # Stop when both boxes reach their goals
        if not red_path and not blue_path:
            moving = False

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (*red_pos, box_size, box_size))
    pygame.draw.rect(screen, BLUE, (*blue_pos, box_size, box_size))
    for p in red_path:
        pygame.draw.circle(screen, GREEN, (int(p[0]), int(p[1])), 3)
    for p in blue_path:
        pygame.draw.circle(screen, GREEN, (int(p[0]), int(p[1])), 3)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
