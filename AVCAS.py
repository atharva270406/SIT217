import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import logging
from datetime import datetime
from IPython.display import HTML

# Setup logging
log_file = "avcas_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Simulation parameters
GRID_WIDTH = 100
GRID_HEIGHT = 60
vehicle_pos = [10, 30]
vehicle_speed = 1
obstacle_pos = [random.randint(40, 90), random.randint(10, 50)]
fail_safe_triggered = False
DETECTION_RADIUS = 10  # Visual range in grid units

# Logging helper
def log_event(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")
    logging.info(message)

# Sensor failure simulation
def simulate_sensor_failure():
    return random.random() < 0.02

# Obstacle detection within range
def obstacle_in_range():
    dx = vehicle_pos[0] - obstacle_pos[0]
    dy = vehicle_pos[1] - obstacle_pos[1]
    distance = (dx**2 + dy**2)**0.5
    return distance <= DETECTION_RADIUS

# Animation function
def update(frame):
    global vehicle_pos, fail_safe_triggered

    plt.cla()
    plt.xlim(0, GRID_WIDTH)
    plt.ylim(0, GRID_HEIGHT)

    # Simulate sensor failure
    if simulate_sensor_failure():
        fail_safe_triggered = True
        log_event("Sensor failure detected. Entering fail-safe mode.")
    else:
        fail_safe_triggered = False

    # Emergency braking if obstacle is in range
    if obstacle_in_range() and not fail_safe_triggered:
        log_event("Obstacle within detection range. Emergency braking triggered.")
        vehicle_speed_effective = 0
    else:
        vehicle_speed_effective = vehicle_speed

    # Move vehicle if not in fail-safe
    if not fail_safe_triggered:
        vehicle_pos[0] += vehicle_speed_effective

    # Draw vehicle
    vehicle_color = 'gray' if fail_safe_triggered else 'green'
    plt.plot(vehicle_pos[0], vehicle_pos[1], 'o', color=vehicle_color, markersize=10, label='Vehicle')

    # Draw detection radius
    detection_circle = plt.Circle((vehicle_pos[0], vehicle_pos[1]), DETECTION_RADIUS, color='blue', alpha=0.2)
    plt.gca().add_patch(detection_circle)

    # Draw obstacle
    plt.plot(obstacle_pos[0], obstacle_pos[1], 'rs', markersize=10, label='Obstacle')

    # Show detection status
    if obstacle_in_range():
        plt.text(obstacle_pos[0], obstacle_pos[1] + 2, "In Range", color='red', fontsize=9)

    plt.legend(loc='upper right')
    plt.title("AVCAS Simulation with Sensor Range")

# Create figure and animation
fig = plt.figure(figsize=(10, 6))
anim = animation.FuncAnimation(fig, update, frames=100, interval=200)

# Display animation in Colab
HTML(anim.to_jshtml())
