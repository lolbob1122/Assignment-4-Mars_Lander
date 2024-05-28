# Marslander.py
import numpy as np
import matplotlib.pyplot as plt
from marsatm import marsinit, marsatm

# Constants
g0 = 3.711  # gravity on Mars in m/s^2
CDS = 4.92  # Drag coefficient times area in m^2
ve = 4400  # Effective exhaust velocity in m/s
m_zfw = 699.0  # Zero fuel mass in kg
m_fuel = 64.5  # Fuel mass in kg
k_v = 0.05  # Gain for the controller

# Initialize the atmosphere table
marstable = marsinit()

# Initial conditions
V = 262  # Initial velocity in m/s
V_yref = -2
h = 20000  # Initial altitude in meters
h_burn = 1745  # Altitude to start burn
x = 0  # Initial x coordinate
gamma = np.deg2rad(-20)  # Flight path angle in radians
m = m_zfw + m_fuel  # Initial mass

# Simulation parameters
dt = 0.05  # Time step in seconds
time = 0
trajectory = []

while h > 0:
    p, rho, temp, sound = marsatm(h/1000)
    V_abs = V
    F_drag = 0.5 * CDS * rho * V_abs**2
    if V_yref - V * np.sin(gamma) > 0:
        m_flow = (m * g0 / ve) - k_v * V * np.sin(gamma) if m_fuel > 0 else 0
        m_flow = 5 if m_flow > 5 else m_flow
    else:
        m_flow = 0
    m_flow = m_flow if h <= h_burn else 0
    m_flow = 0 if h < 0.3 else m_flow
    F_thrust = m_flow * ve
    dvx = ((-F_thrust - F_drag) * np.cos(gamma) / m) * dt
    dvy = (((-F_thrust - F_drag) * np.sin(gamma) - m * g0) / m) * dt
    Vx = V * np.cos(gamma) + dvx
    Vy = V * np.sin(gamma) + dvy
    V = np.hypot(Vx, Vy)
    gamma = np.arctan2(Vy, Vx)
    m_fuel -= m_flow * dt
    h += Vy * dt
    x += Vx * dt
    time += dt
    trajectory.append((time, h, V, np.rad2deg(gamma), m_flow, x))
    print(Vy, h, m_fuel)

# Convert trajectory to numpy array for easy slicing
trajectory = np.array(trajectory)
time = trajectory[:, 0]
height = trajectory[:, 1]
velocity = trajectory[:, 2]
angle = trajectory[:, 3]
m_flow = trajectory[:, 4]
x = trajectory[:, 5]
# Plotting results
plt.figure(figsize=(12, 8))

plt.subplot(231)
plt.plot(time, height)
plt.xlabel('Time (s)')
plt.ylabel('Altitude (m)')
plt.title('Altitude vs Time')

plt.subplot(232)
plt.plot(time, velocity)
plt.xlabel('Time (s)')
plt.ylabel('Speed (m/s)')
plt.title('Speed vs Time')

plt.subplot(233)
plt.plot(time, angle)
plt.xlabel('Time (s)')
plt.ylabel('Flight Path Angle (degrees)')
plt.title('Flight Path Angle vs Time')

plt.subplot(234)
plt.plot(time, m_flow)
plt.xlabel('Time (s)')
plt.ylabel('Mass flow')
plt.title('Mass flow vs Time')

plt.subplot(235)
plt.plot(x, height)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Trajectory')

plt.subplot(236)
plt.plot(velocity, height)
plt.xlabel('Velocity (m/s)')
plt.ylabel('Altitude (m)')
plt.title('Velocity vs Altitude')

plt.tight_layout()
plt.show()
