# def marsinit():
  

# def marsatm(h, marstable):
#     return p, rho, temp, c

marstable = []

with open('Assignment-4-Mars_Lander\\marsatm.txt') as f:
    header = f.readline(2)
        
    for lines in f:
        marstable.append([lines.split()])
        print(lines)
    print(header, marstable)
            