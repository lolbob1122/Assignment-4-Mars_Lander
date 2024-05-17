import marsatm as ma
import matplotlib.pyplot as plt
from math import cos, sin, pi, sqrt
import test2 as t
# Constants
g0 = 3.711  # Mars gravity in m/s^2
v0 = 262  # Initial velocity in m/s
CdS = 4.92  # Drag coefficient * reference area
V_e = 4400  # Effective exhaust velocity in m/s
m_zfw = 699  # Mass of the rover in kg
gamma = -20  # Initial flight path angle in degrees
k = 0.05  # Proportional constant for control input
t = 0  # Initial time
dt = 0.1  # Time step in seconds
marsatm = ma.marsatm

print(t.test)

# Lists to store the results for plotting
ttab = []
vxtab = []
vytab = []
xtab = []
ytab = []

# Initial conditions
vx = v0 * cos(gamma * pi / 180)
vy = v0 * sin(gamma * pi / 180)
x = 0
y = 20

# Simulation loop
while y > 0 and t < 10.0:  # Continue until the rover lands or 10 seconds pass
    p, rho, temp, c = marsatm(y)
    
    # Calculate speed and drag force
    v = sqrt(vx**2 + vy**2)
    Fdrag = CdS * 0.5 * rho * v**2
    
    # Decompose drag force into x and y components
    Fdrag_x = Fdrag * (vx / v)
    Fdrag_y = Fdrag * (vy / v)
    
    # Calculate net forces in x and y directions
    Fxtot = -Fdrag_x
    Fytot = -m_zfw * g0 - Fdrag_y
    
    # Calculate thrust
    mass_flow = m_zfw * g0 / V_e + k * (m_zfw * g0 - m_zfw * g0 * cos(gamma * pi / 180)) / dt
    F_thrust = mass_flow * V_e
    
    # Calculate accelerations in x and y directions
    ax = (Fxtot + F_thrust) / m_zfw
    ay = (Fytot + F_thrust) / m_zfw
    
    # Update velocities
    vx = vx + ax * dt
    vy = vy + ay * dt
    
    # Update positions
    x = x + vx * dt
    y = y + vy * dt
    
    # Update time
    t = t + dt
    
    # Store the results for plotting
    ttab.append(t)
    vxtab.append(vx)
    vytab.append(vy)
    xtab.append(x)
    ytab.append(y)

# Plot the trajectory
plt.plot(xtab, ytab)
plt.xlabel('Horizontal Distance (m)')
plt.ylabel('Vertical Distance (m)')
plt.title('Rover Entry Trajectory on Mars with Thrust')
plt.show()
