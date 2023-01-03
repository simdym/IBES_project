import numpy as np
import matplotlib.pyplot as plt

# Parameters for Moen & Korteweg model
r_0 = 2               # Using value for arteries (2mm)
h = 1                 # Using value for arteries (1mm)
p = 0.994 * 1000      # (Gram per mL) * 1000 = kg/m^3
E_0 = 88926           # 667mmHg = 88926Pa (from paper)
a = 0.018             # From paper

# Height in cm, ptt in ms
# Returns mmHg
def MoenAndKorteweg(height, pttList): 
    bp = []
    d = 0.5 * (height / 100)
    for ptt in pttList:
        bp.append((1/a) * (2 * np.log(d/(ptt*10**-3)) + 2*r_0*p/(h*E_0)))
    return bp



# Parameters for Gesche et. al model
k_1 = 700
k_2 = -1              
k_3 = 766.000
k_4 = 9
k_5 = 30               # Modify to fit values (error between cuff measurement and model)


# bcf approx 0.5 for measurement between heart and finger, height in cm, ptt in ms
# Result in mmHg
def Gesche(bcf, height, pttList):
    bp = []
    for ptt in pttList:
        pwv = (bcf * height) / ptt
        bp.append(k_1 * pwv * np.exp(k_2 * pwv) + k_3 * pwv ** k_4 - k_5)
    return bp
    