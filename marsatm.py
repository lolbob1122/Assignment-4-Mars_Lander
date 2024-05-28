marstable = []  # Declare marstable as a global variable
def marsinit():
    global marstable  # Use the global marstable
    with open('Assignment-4-Mars_Lander/marsatm.txt') as f:
        for line in f:
            marstable.append(line.split())
        marstable = marstable[2:]  # Skip the first two lines as they are headers
def marsatm(h):
    global marstable  # Use the global marstable
    h = float(h)/1000  # Convert input altitude to a float
    columns = list(zip(*marstable))  # Transpose the table to get columns
    altitudes = [float(i) for i in columns[0]]  # Convert altitude column to floats
    densities = [float(i) for i in columns[2]]
    temperatures = [float(i) for i in columns[1]]
    speeds_of_sound = [float(i) for i in columns[3]]
    # Simple linear interpolation between the two altitudes closest to h
    for i in range(len(altitudes) - 1):
        if altitudes[i] <= h <= altitudes[i + 1]:
            h1, h2 = altitudes[i], altitudes[i + 1]
            rho1, rho2 = densities[i], densities[i + 1]
            t1, t2 = temperatures[i], temperatures[i + 1]
            c1, c2 = speeds_of_sound[i], speeds_of_sound[i + 1]
            # Interpolate
            k = (h - h1) / (h2 - h1)
            rho = rho1 + k * (rho2 - rho1)
            temp = t1 + k * (t2 - t1)
            c = c1 + k * (c2 - c1)
            p = rho * temp * 191.84
            return p, rho, temp, c
    # If the altitude is outside the range in the table, handle it
    raise ValueError(f"Altitude {h} km is out of the range covered by the table.")
#------------------------------------------------------------#
# Running = True
# while Running:
#     h = input('Define altitude [km]: ')
#     try:
#         p, rho, temp, c = marsatm(h)
#         print(f"Pressure: {p}, Density: {rho}, Temperature: {temp}, Speed of Sound: {c}")
#     except ValueError as e:
#         print(e)
#     again = input("run again? [y/n]")
#     if again == 'y' or again == 'Y':
#         continue
    # else:
#       break