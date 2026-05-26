import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
NUM_BOIDS = st.sidebar.slider("Number of Boids", 10, 200, 50)
WIDTH, HEIGHT = 800, 600
SPEED_LIMIT = 10
NEIGHBOR_RADIUS = 50
AVOID_RADIUS = 20

# Initialize boids
@st.cache_data
def init_boids(n):
    pos = np.random.rand(n, 2) * [WIDTH, HEIGHT]
    vel = (np.random.rand(n, 2) - 0.5) * SPEED_LIMIT
    return pos, vel

positions, velocities = init_boids(NUM_BOIDS)

def update_boids(pos, vel):
    for i in range(len(pos)):
        neighbors = []
        separation = np.zeros(2)
        alignment = np.zeros(2)
        cohesion = np.zeros(2)
        count = 0

        for j in range(len(pos)):
            if i == j:
                continue
            dist = np.linalg.norm(pos[i] - pos[j])
            if dist < NEIGHBOR_RADIUS:
                neighbors.append(j)
                alignment += vel[j]
                cohesion += pos[j]
                count += 1
                if dist < AVOID_RADIUS:
                    separation += pos[i] - pos[j]

        if count > 0:
            alignment /= count
            cohesion = (cohesion / count - pos[i])
            vel[i] += 0.05 * alignment + 0.01 * cohesion + 0.1 * separation

        # Limit speed
        speed = np.linalg.norm(vel[i])
        if speed > SPEED_LIMIT:
            vel[i] = (vel[i] / speed) * SPEED_LIMIT

        # Wrap around edges
        pos[i] = (pos[i] + vel[i]) % [WIDTH, HEIGHT]

    return pos, vel

# Streamlit animation loop
frame = st.empty()
for _ in range(300):
    positions, velocities = update_boids(positions, velocities)
    fig, ax = plt.subplots()
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.scatter(positions[:, 0], positions[:, 1], color='black', s=10)
    ax.set_xticks([])
    ax.set_yticks([])
    frame.pyplot(fig)
