import marsatm as ma
import matplotlib.pyplot as plt
from math import cos, sin, tan, pi
g0 = 3.711
v0 = 262
CdS = 4.92
V_e = 4400
m_zfw = 699
h0 = 20
gamma = -20
t = 0
dt = 0.1
ttab = []
vxtab = []
vytab = []
xtab = []
ytab = []
vx = v0 * cos(gamma * pi / 180 )
vy = v0 * sin(gamma * pi / 180 )
while t < 10.0:
        
    t = t + dt
    ax = Fxtot / m
    ay = Fytot / m
    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    ttab.append(t)
    vxtab.append(vx)
    vytab.append(vy)
    xtab.append(x)
    ytab.append(y)
plt.plot(xtab, ytab)


plt.show()