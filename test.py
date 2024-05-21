import numpy as np
import matplotlib.pyplot as plt
from marsatm import marsatm

# Constants
g0 = 3.711  # Martian gravity in m/s^2
CdS = 4.92  # Drag coefficient * reference area in m^2
ve = 4400   # Effective exhaust velocity in m/s
m_zfw = 699.0  # Zero fuel weight in kg
kv = 0.05  # Control gain for thrust

# Initial conditions
v0 = 262  # Initial velocity in m/s
h0 = 20000  # Initial altitude in meters
gamma0 = np.radians(-20)  # Initial flight path angle in radians
dt = 0.1  # Time step in seconds
max_burn_rate = 5  # Maximum burn rate in kg/s
altitude_threshold = 0.3  # Altitude threshold below which thrusters are not used in meters

# Initial state
vx = v0 * np.cos(gamma0)
vy = v0 * np.sin(gamma0)
x = 0
y = h0 
mass = m_zfw  # Starting with zero fuel

# Lists for storing results for plotting
x_list = [x]
y_list = [y]
vx_list = [vx]
vy_list = [vy]
mass_list = [mass]
time_list = [0]
thrust_list = [0]

def get_drag_force(v, h):
    p, rho, temp, c = marsatm(h)
    F_drag = 0.5 * CdS * rho * v**2
    return F_drag

def thrust_control(h, vy, mass):
    if h < altitude_threshold:
        return 0  # Do not use thrusters below the altitude threshold

    vy_ref = -2.0  # Target landing speed in m/s
    delta_vy = vy_ref - vy
    burn_rate = mass * g0 / ve + kv * delta_vy
    burn_rate = min(burn_rate, max_burn_rate)  # Cap the burn rate at maximum
    burn_rate = max(burn_rate, 0)  # Ensure burn rate is non-negative
    return burn_rate

t = 0
while y > 0:
    v = np.sqrt(vx**2 + vy**2)
    gamma = np.arctan2(vy, vx)
    
    F_drag = get_drag_force(v, y)
    burn_rate = thrust_control(y, vy, mass)
    thrust = burn_rate * ve
    
    ax = -(F_drag / mass) * np.cos(gamma)
    ay = -(F_drag / mass) * np.sin(gamma) - g0 + (thrust / mass)
    
    # Backward Euler integration
    vx -= ax * dt
    vy -= ay * dt
    x += vx * dt
    y += vy * dt
    mass -= burn_rate * dt
    
    # Store results
    x_list.append(x)
    y_list.append(y)
    vx_list.append(vx)
    vy_list.append(vy)
    mass_list.append(mass)
    thrust_list.append(thrust)
    time_list.append(t)
    
    t += dt

# Step 3: Plotting results
plt.figure(figsize=(12, 10))

plt.subplot(231)
plt.plot(x_list, y_list)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Trajectory')

plt.subplot(232)
plt.plot(time_list, np.sqrt(np.array(vx_list)**2 + np.array(vy_list)**2))
plt.xlabel('Time (s)')
plt.ylabel('Speed (m/s)')
plt.title('Speed vs Time')

plt.subplot(233)
plt.plot(time_list, mass_list)
plt.xlabel('Time (s)')
plt.ylabel('Mass (kg)')
plt.title('Mass vs Time')

plt.subplot(234)
plt.plot(time_list, y_list)
plt.xlabel('Time (s)')
plt.ylabel('Altitude (m)')
plt.title('Altitude vs Time')

plt.subplot(235)
plt.plot(time_list, np.degrees(np.arctan2(vy_list, vx_list)))
plt.xlabel('Time (s)')
plt.ylabel('Flight Path Angle (degrees)')
plt.title('Flight Path Angle vs Time')

plt.subplot(236)
plt.plot(time_list, thrust_list)
plt.xlabel('Time (s)')
plt.ylabel('Thrust (N)')
plt.title('Thrust vs Time')

plt.tight_layout()
plt.show()

# Step 4: Optimization
def simulate_landing(hT, mfuel):
    # Reset initial conditions
    vx = v0 * np.cos(gamma0)
    vy = v0 * np.sin(gamma0)
    x = 0
    y = h0
    mass = m_zfw + mfuel
    t = 0

    while y > 0:
        v = np.sqrt(vx**2 + vy**2)
        gamma = np.arctan2(vy, vx)
        
        F_drag = get_drag_force(v, y)
        burn_rate = thrust_control(y, vy, mass) if y < hT else 0
        thrust = burn_rate * ve
        
        ax = -(F_drag / mass) * np.cos(gamma)
        ay = -(F_drag / mass) * np.sin(gamma) - g0 + (thrust / mass)
        
        # Backward Euler integration
        vx -= ax * dt
        vy -= ay * dt
        x += vx * dt
        y += vy * dt
        mass -= burn_rate * dt
        
        t += dt
        
        # Terminate if fuel runs out
        if mass <= m_zfw:
            mass = m_zfw
            break
    
    return y, np.sqrt(vx**2 + vy**2)

# Determine optimal values for hT and mfuel
hT = 1000  # Initial guess for thrust altitude in meters
mfuel = 500  # Initial guess for fuel mass in kg

final_altitude, final_speed = simulate_landing(hT, mfuel)

while final_speed > 2.0:  # Target landing speed is less than 3 m/s
    hT -= 100  # Decrease thrust altitude
    final_altitude, final_speed = simulate_landing(hT, mfuel)
    if hT <= 0:
        break

while final_speed < 2.0:
    mfuel -= 10  # Decrease fuel mass
    final_altitude, final_speed = simulate_landing(hT, mfuel)
    if mfuel <= 0:
        break

print(f"Optimal thrust altitude (hT): {hT} meters")
print(f"Optimal fuel mass (mfuel): {mfuel} kg")
print(f"Final landing speed: {final_speed} m/s")