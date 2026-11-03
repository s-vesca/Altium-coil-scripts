import math
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from altium_gen import AltiumScriptGenerator

#5 strands (5 positions), 2 layers

RMAX            = 70e-3             #[m] external radius
RMIN            = 35e-3             #[m] internal radius
NTURNS          = 8                 #[-] number of turns
STRAND_THICK    = 0.3e-3            #[m] strand thickness
STRAND_GAP      = 0.3e-3            #[m] strand gap

NPTS_PER_TURN = 200
STRAND_SECTORS_NSTEPS = int(NPTS_PER_TURN * 10 / 360)

plot_t = STRAND_THICK / 0.3527 * 1000

theta = np.linspace(10*math.pi/180,NTURNS*2*math.pi,NPTS_PER_TURN*NTURNS)

R_inc = (RMAX-RMIN)/NTURNS

S1_layer    = np.empty(len(theta))
S1_x        = np.empty(len(theta))
S1_y        = np.empty(len(theta))
S2_layer    = np.empty(len(theta))
S2_x        = np.empty(len(theta))
S2_y        = np.empty(len(theta))
S3_layer    = np.empty(len(theta))
S3_x        = np.empty(len(theta))
S3_y        = np.empty(len(theta))
S4_layer    = np.empty(len(theta))
S4_x        = np.empty(len(theta))
S4_y        = np.empty(len(theta))
S5_layer    = np.empty(len(theta))
S5_x        = np.empty(len(theta))
S5_y        = np.empty(len(theta))


#strand position loop: L1-P0,L2-P0,L2-P1,L2-P2,L2-P3,L2-P4,L1-P4,L1-P3,L1-P2,L1-P1,L1-P0
Strand_pos = Enum('strand_pos', [('L1P0', 0),
                                 ('L2P0', 1),
                                 ('L2P1', 2),
                                 ('L2P2', 3),
                                 ('L2P3', 4),
                                 ('L2P4', 5),
                                 ('L1P4', 6),
                                 ('L1P3', 7),
                                 ('L1P2', 8),
                                 ('L1P1', 9)])

strand1_pos = 0
strand2_pos = 2
strand3_pos = 4
strand4_pos = 6
strand5_pos = 8

for ii in range(len(theta)):
    th = theta[ii]

    #position p3 is the centered one
    r_p2 = RMIN + R_inc/(2*math.pi)*th

    r_p0 = r_p2 - 2 * (STRAND_THICK + STRAND_GAP)
    r_p1 = r_p2 - 1 * (STRAND_THICK + STRAND_GAP)
    r_p4 = r_p2 + 2 * (STRAND_THICK + STRAND_GAP)
    r_p3 = r_p2 + 1 * (STRAND_THICK + STRAND_GAP)

    if(ii % STRAND_SECTORS_NSTEPS == 0):
        if(not(ii % (STRAND_SECTORS_NSTEPS * 2) == 0)):
            #new position
            strand1_pos = strand1_pos + 1
            strand2_pos = strand2_pos + 1
            strand3_pos = strand3_pos + 1
            strand4_pos = strand4_pos + 1
            strand5_pos = strand5_pos + 1

    if(strand1_pos > 9):
        strand1_pos = 0

    if(strand2_pos > 9):
        strand2_pos = 0
    
    if(strand3_pos > 9):
        strand3_pos = 0

    if(strand4_pos > 9):
        strand4_pos = 0

    if(strand5_pos > 9):
        strand5_pos = 0


    #find strand 1 layer
    if((strand1_pos >= 1) and (strand1_pos < 6)):
        S1_layer[ii] = 1
    else:
        S1_layer[ii] = 0

    #find strand 1 radius
    if((strand1_pos == Strand_pos.L1P0.value) or (strand1_pos == Strand_pos.L2P0.value)):
        r = r_p0
    elif((strand1_pos == Strand_pos.L1P1.value) or (strand1_pos == Strand_pos.L2P1.value)):
        r = r_p1
    elif((strand1_pos == Strand_pos.L1P2.value) or (strand1_pos == Strand_pos.L2P2.value)):
        r = r_p2
    elif((strand1_pos == Strand_pos.L1P3.value) or (strand1_pos == Strand_pos.L2P3.value)):
        r = r_p3
    elif((strand1_pos == Strand_pos.L1P4.value) or (strand1_pos == Strand_pos.L2P4.value)):
        r = r_p4
    else:
        print("error")

    S1_x[ii] = r * math.cos(th)
    S1_y[ii] = r * math.sin(th)

    #find strand 2 layer
    if((strand2_pos >= 1) and (strand2_pos < 6)):
        S2_layer[ii] = 1
    else:
        S2_layer[ii] = 0

    #find strand 2 radius
    if((strand2_pos == Strand_pos.L1P0.value) or (strand2_pos == Strand_pos.L2P0.value)):
        r = r_p0
    elif((strand2_pos == Strand_pos.L1P1.value) or (strand2_pos == Strand_pos.L2P1.value)):
        r = r_p1
    elif((strand2_pos == Strand_pos.L1P2.value) or (strand2_pos == Strand_pos.L2P2.value)):
        r = r_p2
    elif((strand2_pos == Strand_pos.L1P3.value) or (strand2_pos == Strand_pos.L2P3.value)):
        r = r_p3
    elif((strand2_pos == Strand_pos.L1P4.value) or (strand2_pos == Strand_pos.L2P4.value)):
        r = r_p4
    else:
        print("error")

    S2_x[ii] = r * math.cos(th)
    S2_y[ii] = r * math.sin(th)

    #find strand 3 layer
    if((strand3_pos >= 1) and (strand3_pos < 6)):
        S3_layer[ii] = 1
    else:
        S3_layer[ii] = 0

    #find strand 3 radius
    if((strand3_pos == Strand_pos.L1P0.value) or (strand3_pos == Strand_pos.L2P0.value)):
        r = r_p0
    elif((strand3_pos == Strand_pos.L1P1.value) or (strand3_pos == Strand_pos.L2P1.value)):
        r = r_p1
    elif((strand3_pos == Strand_pos.L1P2.value) or (strand3_pos == Strand_pos.L2P2.value)):
        r = r_p2
    elif((strand3_pos == Strand_pos.L1P3.value) or (strand3_pos == Strand_pos.L2P3.value)):
        r = r_p3
    elif((strand3_pos == Strand_pos.L1P4.value) or (strand3_pos == Strand_pos.L2P4.value)):
        r = r_p4
    else:
        print("error")

    S3_x[ii] = r * math.cos(th)
    S3_y[ii] = r * math.sin(th)

    #find strand 4 layer
    if((strand4_pos >= 1) and (strand4_pos < 6)):
        S4_layer[ii] = 1
    else:
        S4_layer[ii] = 0

    #find strand 4 radius
    if((strand4_pos == Strand_pos.L1P0.value) or (strand4_pos == Strand_pos.L2P0.value)):
        r = r_p0
    elif((strand4_pos == Strand_pos.L1P1.value) or (strand4_pos == Strand_pos.L2P1.value)):
        r = r_p1
    elif((strand4_pos == Strand_pos.L1P2.value) or (strand4_pos == Strand_pos.L2P2.value)):
        r = r_p2
    elif((strand4_pos == Strand_pos.L1P3.value) or (strand4_pos == Strand_pos.L2P3.value)):
        r = r_p3
    elif((strand4_pos == Strand_pos.L1P4.value) or (strand4_pos == Strand_pos.L2P4.value)):
        r = r_p4
    else:
        print("error")

    S4_x[ii] = r * math.cos(th)
    S4_y[ii] = r * math.sin(th)

    #find strand 5 layer
    if((strand5_pos >= 1) and (strand5_pos < 6)):
        S5_layer[ii] = 1
    else:
        S5_layer[ii] = 0

    #find strand 5 radius
    if((strand5_pos == Strand_pos.L1P0.value) or (strand5_pos == Strand_pos.L2P0.value)):
        r = r_p0
    elif((strand5_pos == Strand_pos.L1P1.value) or (strand5_pos == Strand_pos.L2P1.value)):
        r = r_p1
    elif((strand5_pos == Strand_pos.L1P2.value) or (strand5_pos == Strand_pos.L2P2.value)):
        r = r_p2
    elif((strand5_pos == Strand_pos.L1P3.value) or (strand5_pos == Strand_pos.L2P3.value)):
        r = r_p3
    elif((strand5_pos == Strand_pos.L1P4.value) or (strand5_pos == Strand_pos.L2P4.value)):
        r = r_p4
    else:
        print("error")

    S5_x[ii] = r * math.cos(th)
    S5_y[ii] = r * math.sin(th)

S1_x_L1 = [S1_x[ii] if S1_layer[ii] == 0 else math.nan for ii in range(len(S1_x))]
S1_x_L2 = [S1_x[ii] if S1_layer[ii] == 1 else math.nan for ii in range(len(S1_x))]
S1_y_L1 = [S1_y[ii] if S1_layer[ii] == 0 else math.nan for ii in range(len(S1_y))]
S1_y_L2 = [S1_y[ii] if S1_layer[ii] == 1 else math.nan for ii in range(len(S1_y))]

S2_x_L1 = [S2_x[ii] if S2_layer[ii] == 0 else math.nan for ii in range(len(S2_x))]
S2_x_L2 = [S2_x[ii] if S2_layer[ii] == 1 else math.nan for ii in range(len(S2_x))]
S2_y_L1 = [S2_y[ii] if S2_layer[ii] == 0 else math.nan for ii in range(len(S2_y))]
S2_y_L2 = [S2_y[ii] if S2_layer[ii] == 1 else math.nan for ii in range(len(S2_y))]

S3_x_L1 = [S3_x[ii] if S3_layer[ii] == 0 else math.nan for ii in range(len(S3_x))]
S3_x_L2 = [S3_x[ii] if S3_layer[ii] == 1 else math.nan for ii in range(len(S3_x))]
S3_y_L1 = [S3_y[ii] if S3_layer[ii] == 0 else math.nan for ii in range(len(S3_y))]
S3_y_L2 = [S3_y[ii] if S3_layer[ii] == 1 else math.nan for ii in range(len(S3_y))]

S4_x_L1 = [S4_x[ii] if S4_layer[ii] == 0 else math.nan for ii in range(len(S4_x))]
S4_x_L2 = [S4_x[ii] if S4_layer[ii] == 1 else math.nan for ii in range(len(S4_x))]
S4_y_L1 = [S4_y[ii] if S4_layer[ii] == 0 else math.nan for ii in range(len(S4_y))]
S4_y_L2 = [S4_y[ii] if S4_layer[ii] == 1 else math.nan for ii in range(len(S4_y))]

S5_x_L1 = [S5_x[ii] if S5_layer[ii] == 0 else math.nan for ii in range(len(S5_x))]
S5_x_L2 = [S5_x[ii] if S5_layer[ii] == 1 else math.nan for ii in range(len(S5_x))]
S5_y_L1 = [S5_y[ii] if S5_layer[ii] == 0 else math.nan for ii in range(len(S5_y))]
S5_y_L2 = [S5_y[ii] if S5_layer[ii] == 1 else math.nan for ii in range(len(S5_y))]

plt.plot(S1_x_L1,S1_y_L1,color="red",linewidth=plot_t)
plt.plot(S1_x_L2,S1_y_L2,color="brown",linewidth=plot_t)

plt.plot(S2_x_L1,S2_y_L1,color="red",linewidth=plot_t)
plt.plot(S2_x_L2,S2_y_L2,color="brown",linewidth=plot_t)

plt.plot(S3_x_L1,S3_y_L1,color="red",linewidth=plot_t)
plt.plot(S3_x_L2,S3_y_L2,color="brown",linewidth=plot_t)

plt.plot(S4_x_L1,S4_y_L1,color="red",linewidth=plot_t)
plt.plot(S4_x_L2,S4_y_L2,color="brown",linewidth=plot_t)

plt.plot(S5_x_L1,S5_y_L1,color="red",linewidth=plot_t)
plt.plot(S5_x_L2,S5_y_L2,color="brown",linewidth=plot_t)

ag = AltiumScriptGenerator()

for ii in range(len(S1_x)-1):
    if((S1_layer[ii] == 0) and (S1_layer[ii+1] == 0)):
        #both points on first layer
        ag.add_track(S1_x[ii]*1000+250, S1_y[ii]*1000+250, S1_x[ii+1]*1000+250, S1_y[ii+1]*1000+250, STRAND_THICK*1000, 'TopLayer')
    elif((S1_layer[ii] == 1) and (S1_layer[ii+1] == 1)):
        #both points on second layer
        ag.add_track(S1_x[ii]*1000+250, S1_y[ii]*1000+250, S1_x[ii+1]*1000+250, S1_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer1')
    else:
        #points in different layers
        via_x = (S1_x[ii]+S1_x[ii+1])/2
        via_y = (S1_y[ii]+S1_y[ii+1])/2
        ag.add_via(via_x*1000+250,via_y*1000+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','InLayer1')
        if(S1_layer[ii] == 0):
            ag.add_track(S1_x[ii]*1000+250, S1_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'TopLayer')
            ag.add_track(via_x*1000+250, via_y*1000+250, S1_x[ii+1]*1000+250, S1_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer1')
        else:
            ag.add_track(S1_x[ii]*1000+250, S1_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'InLayer1')
            ag.add_track(via_x*1000+250, via_y*1000+250, S1_x[ii+1]*1000+250, S1_y[ii+1]*1000+250, STRAND_THICK*1000, 'TopLayer')

for ii in range(len(S2_x)-1):
    if((S2_layer[ii] == 0) and (S2_layer[ii+1] == 0)):
        ag.add_track(S2_x[ii]*1000+250, S2_y[ii]*1000+250, S2_x[ii+1]*1000+250, S2_y[ii+1]*1000+250, STRAND_THICK*1000, 'TopLayer')
    elif((S2_layer[ii] == 1) and (S2_layer[ii+1] == 1)):
        ag.add_track(S2_x[ii]*1000+250, S2_y[ii]*1000+250, S2_x[ii+1]*1000+250, S2_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer1')
    else:
        #points in different layers
        via_x = (S2_x[ii]+S2_x[ii+1])/2
        via_y = (S2_y[ii]+S2_y[ii+1])/2
        ag.add_via(via_x*1000+250,via_y*1000+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','InLayer1')
        if(S2_layer[ii] == 0):
            ag.add_track(S2_x[ii]*1000+250, S2_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'TopLayer')
            ag.add_track(via_x*1000+250, via_y*1000+250, S2_x[ii+1]*1000+250, S2_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer1')
        else:
            ag.add_track(S2_x[ii]*1000+250, S2_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'InLayer1')
            ag.add_track(via_x*1000+250, via_y*1000+250, S2_x[ii+1]*1000+250, S2_y[ii+1]*1000+250, STRAND_THICK*1000, 'TopLayer')

for ii in range(len(S3_x)-1):
    if((S3_layer[ii] == 0) and (S3_layer[ii+1] == 0)):
        ag.add_track(S3_x[ii]*1000+250, S3_y[ii]*1000+250, S3_x[ii+1]*1000+250, S3_y[ii+1]*1000+250, STRAND_THICK*1000, 'TopLayer')
    elif((S3_layer[ii] == 1) and (S3_layer[ii+1] == 1)):
        ag.add_track(S3_x[ii]*1000+250, S3_y[ii]*1000+250, S3_x[ii+1]*1000+250, S3_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer1')
    else:
        #points in different layers
        via_x = (S3_x[ii]+S3_x[ii+1])/2
        via_y = (S3_y[ii]+S3_y[ii+1])/2
        ag.add_via(via_x*1000+250,via_y*1000+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','InLayer1')
        if(S3_layer[ii] == 0):
            ag.add_track(S3_x[ii]*1000+250, S3_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'TopLayer')
            ag.add_track(via_x*1000+250, via_y*1000+250, S3_x[ii+1]*1000+250, S3_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer1')
        else:
            ag.add_track(S3_x[ii]*1000+250, S3_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'InLayer1')
            ag.add_track(via_x*1000+250, via_y*1000+250, S3_x[ii+1]*1000+250, S3_y[ii+1]*1000+250, STRAND_THICK*1000, 'TopLayer')

for ii in range(len(S4_x)-1):
    if((S4_layer[ii] == 0) and (S4_layer[ii+1] == 0)):
        ag.add_track(S4_x[ii]*1000+250, S4_y[ii]*1000+250, S4_x[ii+1]*1000+250, S4_y[ii+1]*1000+250, STRAND_THICK*1000, 'TopLayer')
    elif((S4_layer[ii] == 1) and (S4_layer[ii+1] == 1)):
        ag.add_track(S4_x[ii]*1000+250, S4_y[ii]*1000+250, S4_x[ii+1]*1000+250, S4_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer1')
    else:
        #points in different layers
        via_x = (S4_x[ii]+S4_x[ii+1])/2
        via_y = (S4_y[ii]+S4_y[ii+1])/2
        ag.add_via(via_x*1000+250,via_y*1000+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','InLayer1')
        if(S4_layer[ii] == 0):
            ag.add_track(S4_x[ii]*1000+250, S4_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'TopLayer')
            ag.add_track(via_x*1000+250, via_y*1000+250, S4_x[ii+1]*1000+250, S4_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer1')
        else:
            ag.add_track(S4_x[ii]*1000+250, S4_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'InLayer1')
            ag.add_track(via_x*1000+250, via_y*1000+250, S4_x[ii+1]*1000+250, S4_y[ii+1]*1000+250, STRAND_THICK*1000, 'TopLayer')

for ii in range(len(S5_x)-1):
    if((S5_layer[ii] == 0) and (S5_layer[ii+1] == 0)):
        ag.add_track(S5_x[ii]*1000+250, S5_y[ii]*1000+250, S5_x[ii+1]*1000+250, S5_y[ii+1]*1000+250, STRAND_THICK*1000, 'TopLayer')
    elif((S5_layer[ii] == 1) and (S5_layer[ii+1] == 1)):
        ag.add_track(S5_x[ii]*1000+250, S5_y[ii]*1000+250, S5_x[ii+1]*1000+250, S5_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer1')
    else:
        #points in different layers
        via_x = (S5_x[ii]+S5_x[ii+1])/2
        via_y = (S5_y[ii]+S5_y[ii+1])/2
        ag.add_via(via_x*1000+250,via_y*1000+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','InLayer1')
        if(S5_layer[ii] == 0):
            ag.add_track(S5_x[ii]*1000+250, S5_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'TopLayer')
            ag.add_track(via_x*1000+250, via_y*1000+250, S5_x[ii+1]*1000+250, S5_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer1')
        else:
            ag.add_track(S5_x[ii]*1000+250, S5_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'InLayer1')
            ag.add_track(via_x*1000+250, via_y*1000+250, S5_x[ii+1]*1000+250, S5_y[ii+1]*1000+250, STRAND_THICK*1000, 'TopLayer')

#ag.add_via(RMIN *1000+250,0+250,1,0.6,'TopLayer','BottomLayer')
#ag.add_via((RMIN- 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,0+250,1,0.6,'TopLayer','BottomLayer')
#ag.add_via((RMIN- 1 * (STRAND_THICK + STRAND_GAP)) *1000+250,0+250,1,0.6,'TopLayer','BottomLayer')
#ag.add_via((RMIN+ 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,0+250,1,0.6,'TopLayer','BottomLayer')
#ag.add_via((RMIN+ 1 * (STRAND_THICK + STRAND_GAP)) *1000+250,0+250,1,0.6,'TopLayer','BottomLayer')
#
#ag.add_track((RMIN- 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250,(RMIN+ 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250, STRAND_THICK*1000, 'TopLayer')
#ag.add_track((RMIN- 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250,(RMIN+ 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250, STRAND_THICK*1000, 'InLayer1')
#ag.add_track((RMIN- 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250,(RMIN+ 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250, STRAND_THICK*1000, 'InLayer2')
#ag.add_track((RMIN- 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250,(RMIN+ 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250, STRAND_THICK*1000, 'BottomLayer')

ag.add_via(RMAX *1000+250,0+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')
ag.add_via((RMAX- 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,0+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')
ag.add_via((RMAX- 1 * (STRAND_THICK + STRAND_GAP)) *1000+250,0+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')
ag.add_via((RMAX+ 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,0+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')
ag.add_via((RMAX+ 1 * (STRAND_THICK + STRAND_GAP)) *1000+250,0+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')

ag.add_track((RMAX- 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250,(RMAX+ 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250, STRAND_THICK*1000, 'TopLayer')
ag.add_track((RMAX- 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250,(RMAX+ 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250, STRAND_THICK*1000, 'InLayer1')
ag.add_track((RMAX- 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250,(RMAX+ 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250, STRAND_THICK*1000, 'InLayer2')
ag.add_track((RMAX- 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250,(RMAX+ 2 * (STRAND_THICK + STRAND_GAP)) *1000+250,250, STRAND_THICK*1000, 'BottomLayer')

r_10deg = RMIN + R_inc/(2*math.pi)*(10.0*math.pi/180.0)

ag.add_via((r_10deg)*math.cos(10.0*math.pi/180.0)  * 1000 + 250, r_10deg*math.sin(10.0*math.pi/180.0)  * 1000 + 250, STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')
ag.add_via((r_10deg)*math.cos(-10.0*math.pi/180.0) * 1000 + 250, r_10deg*math.sin(-10.0*math.pi/180.0) * 1000 + 250, STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')

ag.add_via((r_10deg - 2 * (STRAND_THICK + STRAND_GAP))*math.cos(10.0*math.pi/180.0)  * 1000 + 250, (r_10deg - 2 * (STRAND_THICK + STRAND_GAP))*math.sin(10.0*math.pi/180.0)  * 1000 + 250, STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')
ag.add_via((r_10deg - 2 * (STRAND_THICK + STRAND_GAP))*math.cos(-10.0*math.pi/180.0) * 1000 + 250, (r_10deg - 2 * (STRAND_THICK + STRAND_GAP))*math.sin(-10.0*math.pi/180.0) * 1000 + 250, STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')

ag.add_via((r_10deg - 1 * (STRAND_THICK + STRAND_GAP))*math.cos(10.0*math.pi/180.0)  * 1000 + 250, (r_10deg - 1 * (STRAND_THICK + STRAND_GAP))*math.sin(10.0*math.pi/180.0)  * 1000 + 250, STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')
ag.add_via((r_10deg - 1 * (STRAND_THICK + STRAND_GAP))*math.cos(-10.0*math.pi/180.0) * 1000 + 250, (r_10deg - 1 * (STRAND_THICK + STRAND_GAP))*math.sin(-10.0*math.pi/180.0) * 1000 + 250, STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')

ag.add_via((r_10deg + 2 * (STRAND_THICK + STRAND_GAP))*math.cos(10.0*math.pi/180.0)  * 1000 + 250, (r_10deg + 2 * (STRAND_THICK + STRAND_GAP))*math.sin(10.0*math.pi/180.0)  * 1000 + 250, STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')
ag.add_via((r_10deg + 2 * (STRAND_THICK + STRAND_GAP))*math.cos(-10.0*math.pi/180.0) * 1000 + 250, (r_10deg + 2 * (STRAND_THICK + STRAND_GAP))*math.sin(-10.0*math.pi/180.0) * 1000 + 250, STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')

ag.add_via((r_10deg + 1 * (STRAND_THICK + STRAND_GAP))*math.cos(10.0*math.pi/180.0)  * 1000 + 250, (r_10deg + 1 * (STRAND_THICK + STRAND_GAP))*math.sin(10.0*math.pi/180.0)  * 1000 + 250, STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')
ag.add_via((r_10deg + 1 * (STRAND_THICK + STRAND_GAP))*math.cos(-10.0*math.pi/180.0) * 1000 + 250, (r_10deg + 1 * (STRAND_THICK + STRAND_GAP))*math.sin(-10.0*math.pi/180.0) * 1000 + 250, STRAND_THICK*1000,STRAND_THICK*1000/2,'TopLayer','BottomLayer')

##########################################################################################

for ii in range(len(theta)):
    th = - theta[ii]

    #position p3 is the centered one
    r_p2 = RMIN + R_inc/(2*math.pi)*(-th)

    r_p0 = r_p2 - 2 * (STRAND_THICK + STRAND_GAP)
    r_p1 = r_p2 - 1 * (STRAND_THICK + STRAND_GAP)
    r_p4 = r_p2 + 2 * (STRAND_THICK + STRAND_GAP)
    r_p3 = r_p2 + 1 * (STRAND_THICK + STRAND_GAP)

    if(ii % STRAND_SECTORS_NSTEPS == 0):
        if(not(ii % (STRAND_SECTORS_NSTEPS * 2) == 0)):
            #new position
            strand1_pos = strand1_pos + 1
            strand2_pos = strand2_pos + 1
            strand3_pos = strand3_pos + 1
            strand4_pos = strand4_pos + 1
            strand5_pos = strand5_pos + 1

    if(strand1_pos > 9):
        strand1_pos = 0

    if(strand2_pos > 9):
        strand2_pos = 0
    
    if(strand3_pos > 9):
        strand3_pos = 0

    if(strand4_pos > 9):
        strand4_pos = 0

    if(strand5_pos > 9):
        strand5_pos = 0


    #find strand 1 layer
    if((strand1_pos >= 1) and (strand1_pos < 6)):
        S1_layer[ii] = 1
    else:
        S1_layer[ii] = 0

    #find strand 1 radius
    if((strand1_pos == Strand_pos.L1P0.value) or (strand1_pos == Strand_pos.L2P0.value)):
        r = r_p0
    elif((strand1_pos == Strand_pos.L1P1.value) or (strand1_pos == Strand_pos.L2P1.value)):
        r = r_p1
    elif((strand1_pos == Strand_pos.L1P2.value) or (strand1_pos == Strand_pos.L2P2.value)):
        r = r_p2
    elif((strand1_pos == Strand_pos.L1P3.value) or (strand1_pos == Strand_pos.L2P3.value)):
        r = r_p3
    elif((strand1_pos == Strand_pos.L1P4.value) or (strand1_pos == Strand_pos.L2P4.value)):
        r = r_p4
    else:
        print("error")

    S1_x[ii] = r * math.cos(th)
    S1_y[ii] = r * math.sin(th)

    #find strand 2 layer
    if((strand2_pos >= 1) and (strand2_pos < 6)):
        S2_layer[ii] = 1
    else:
        S2_layer[ii] = 0

    #find strand 2 radius
    if((strand2_pos == Strand_pos.L1P0.value) or (strand2_pos == Strand_pos.L2P0.value)):
        r = r_p0
    elif((strand2_pos == Strand_pos.L1P1.value) or (strand2_pos == Strand_pos.L2P1.value)):
        r = r_p1
    elif((strand2_pos == Strand_pos.L1P2.value) or (strand2_pos == Strand_pos.L2P2.value)):
        r = r_p2
    elif((strand2_pos == Strand_pos.L1P3.value) or (strand2_pos == Strand_pos.L2P3.value)):
        r = r_p3
    elif((strand2_pos == Strand_pos.L1P4.value) or (strand2_pos == Strand_pos.L2P4.value)):
        r = r_p4
    else:
        print("error")

    S2_x[ii] = r * math.cos(th)
    S2_y[ii] = r * math.sin(th)

    #find strand 3 layer
    if((strand3_pos >= 1) and (strand3_pos < 6)):
        S3_layer[ii] = 1
    else:
        S3_layer[ii] = 0

    #find strand 3 radius
    if((strand3_pos == Strand_pos.L1P0.value) or (strand3_pos == Strand_pos.L2P0.value)):
        r = r_p0
    elif((strand3_pos == Strand_pos.L1P1.value) or (strand3_pos == Strand_pos.L2P1.value)):
        r = r_p1
    elif((strand3_pos == Strand_pos.L1P2.value) or (strand3_pos == Strand_pos.L2P2.value)):
        r = r_p2
    elif((strand3_pos == Strand_pos.L1P3.value) or (strand3_pos == Strand_pos.L2P3.value)):
        r = r_p3
    elif((strand3_pos == Strand_pos.L1P4.value) or (strand3_pos == Strand_pos.L2P4.value)):
        r = r_p4
    else:
        print("error")

    S3_x[ii] = r * math.cos(th)
    S3_y[ii] = r * math.sin(th)

    #find strand 4 layer
    if((strand4_pos >= 1) and (strand4_pos < 6)):
        S4_layer[ii] = 1
    else:
        S4_layer[ii] = 0

    #find strand 4 radius
    if((strand4_pos == Strand_pos.L1P0.value) or (strand4_pos == Strand_pos.L2P0.value)):
        r = r_p0
    elif((strand4_pos == Strand_pos.L1P1.value) or (strand4_pos == Strand_pos.L2P1.value)):
        r = r_p1
    elif((strand4_pos == Strand_pos.L1P2.value) or (strand4_pos == Strand_pos.L2P2.value)):
        r = r_p2
    elif((strand4_pos == Strand_pos.L1P3.value) or (strand4_pos == Strand_pos.L2P3.value)):
        r = r_p3
    elif((strand4_pos == Strand_pos.L1P4.value) or (strand4_pos == Strand_pos.L2P4.value)):
        r = r_p4
    else:
        print("error")

    S4_x[ii] = r * math.cos(th)
    S4_y[ii] = r * math.sin(th)

    #find strand 5 layer
    if((strand5_pos >= 1) and (strand5_pos < 6)):
        S5_layer[ii] = 1
    else:
        S5_layer[ii] = 0

    #find strand 5 radius
    if((strand5_pos == Strand_pos.L1P0.value) or (strand5_pos == Strand_pos.L2P0.value)):
        r = r_p0
    elif((strand5_pos == Strand_pos.L1P1.value) or (strand5_pos == Strand_pos.L2P1.value)):
        r = r_p1
    elif((strand5_pos == Strand_pos.L1P2.value) or (strand5_pos == Strand_pos.L2P2.value)):
        r = r_p2
    elif((strand5_pos == Strand_pos.L1P3.value) or (strand5_pos == Strand_pos.L2P3.value)):
        r = r_p3
    elif((strand5_pos == Strand_pos.L1P4.value) or (strand5_pos == Strand_pos.L2P4.value)):
        r = r_p4
    else:
        print("error")

    S5_x[ii] = r * math.cos(th)
    S5_y[ii] = r * math.sin(th)

S1_x_L1 = [S1_x[ii] if S1_layer[ii] == 0 else math.nan for ii in range(len(S1_x))]
S1_x_L2 = [S1_x[ii] if S1_layer[ii] == 1 else math.nan for ii in range(len(S1_x))]
S1_y_L1 = [S1_y[ii] if S1_layer[ii] == 0 else math.nan for ii in range(len(S1_y))]
S1_y_L2 = [S1_y[ii] if S1_layer[ii] == 1 else math.nan for ii in range(len(S1_y))]

S2_x_L1 = [S2_x[ii] if S2_layer[ii] == 0 else math.nan for ii in range(len(S2_x))]
S2_x_L2 = [S2_x[ii] if S2_layer[ii] == 1 else math.nan for ii in range(len(S2_x))]
S2_y_L1 = [S2_y[ii] if S2_layer[ii] == 0 else math.nan for ii in range(len(S2_y))]
S2_y_L2 = [S2_y[ii] if S2_layer[ii] == 1 else math.nan for ii in range(len(S2_y))]

S3_x_L1 = [S3_x[ii] if S3_layer[ii] == 0 else math.nan for ii in range(len(S3_x))]
S3_x_L2 = [S3_x[ii] if S3_layer[ii] == 1 else math.nan for ii in range(len(S3_x))]
S3_y_L1 = [S3_y[ii] if S3_layer[ii] == 0 else math.nan for ii in range(len(S3_y))]
S3_y_L2 = [S3_y[ii] if S3_layer[ii] == 1 else math.nan for ii in range(len(S3_y))]

S4_x_L1 = [S4_x[ii] if S4_layer[ii] == 0 else math.nan for ii in range(len(S4_x))]
S4_x_L2 = [S4_x[ii] if S4_layer[ii] == 1 else math.nan for ii in range(len(S4_x))]
S4_y_L1 = [S4_y[ii] if S4_layer[ii] == 0 else math.nan for ii in range(len(S4_y))]
S4_y_L2 = [S4_y[ii] if S4_layer[ii] == 1 else math.nan for ii in range(len(S4_y))]

S5_x_L1 = [S5_x[ii] if S5_layer[ii] == 0 else math.nan for ii in range(len(S5_x))]
S5_x_L2 = [S5_x[ii] if S5_layer[ii] == 1 else math.nan for ii in range(len(S5_x))]
S5_y_L1 = [S5_y[ii] if S5_layer[ii] == 0 else math.nan for ii in range(len(S5_y))]
S5_y_L2 = [S5_y[ii] if S5_layer[ii] == 1 else math.nan for ii in range(len(S5_y))]

plt.plot(S1_x_L1,S1_y_L1,color="cyan",linewidth=plot_t)
plt.plot(S1_x_L2,S1_y_L2,color="blue",linewidth=plot_t)

plt.plot(S2_x_L1,S2_y_L1,color="cyan",linewidth=plot_t)
plt.plot(S2_x_L2,S2_y_L2,color="blue",linewidth=plot_t)

plt.plot(S3_x_L1,S3_y_L1,color="cyan",linewidth=plot_t)
plt.plot(S3_x_L2,S3_y_L2,color="blue",linewidth=plot_t)

plt.plot(S4_x_L1,S4_y_L1,color="cyan",linewidth=plot_t)
plt.plot(S4_x_L2,S4_y_L2,color="blue",linewidth=plot_t)

plt.plot(S5_x_L1,S5_y_L1,color="cyan",linewidth=plot_t)
plt.plot(S5_x_L2,S5_y_L2,color="blue",linewidth=plot_t)

for ii in range(len(S1_x)-1):
    if((S1_layer[ii] == 0) and (S1_layer[ii+1] == 0)):
        ag.add_track(S1_x[ii]*1000+250, S1_y[ii]*1000+250, S1_x[ii+1]*1000+250, S1_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer2')
    elif((S1_layer[ii] == 1) and (S1_layer[ii+1] == 1)):
        ag.add_track(S1_x[ii]*1000+250, S1_y[ii]*1000+250, S1_x[ii+1]*1000+250, S1_y[ii+1]*1000+250, STRAND_THICK*1000, 'BottomLayer')
    else:
        #points in different layers
        via_x = (S1_x[ii]+S1_x[ii+1])/2
        via_y = (S1_y[ii]+S1_y[ii+1])/2
        ag.add_via(via_x*1000+250,via_y*1000+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'InLayer2','BottomLayer')
        if(S1_layer[ii] == 0):
            ag.add_track(S1_x[ii]*1000+250, S1_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'InLayer2')
            ag.add_track(via_x*1000+250, via_y*1000+250, S1_x[ii+1]*1000+250, S1_y[ii+1]*1000+250, STRAND_THICK*1000, 'BottomLayer')
        else:
            ag.add_track(S1_x[ii]*1000+250, S1_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'BottomLayer')
            ag.add_track(via_x*1000+250, via_y*1000+250, S1_x[ii+1]*1000+250, S1_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer2')

for ii in range(len(S2_x)-1):
    if((S2_layer[ii] == 0) and (S2_layer[ii+1] == 0)):
        ag.add_track(S2_x[ii]*1000+250, S2_y[ii]*1000+250, S2_x[ii+1]*1000+250, S2_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer2')
    elif((S2_layer[ii] == 1) and (S2_layer[ii+1] == 1)):
        ag.add_track(S2_x[ii]*1000+250, S2_y[ii]*1000+250, S2_x[ii+1]*1000+250, S2_y[ii+1]*1000+250, STRAND_THICK*1000, 'BottomLayer')
    else:
        #points in different layers
        via_x = (S2_x[ii]+S2_x[ii+1])/2
        via_y = (S2_y[ii]+S2_y[ii+1])/2
        ag.add_via(via_x*1000+250,via_y*1000+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'InLayer2','BottomLayer')
        if(S2_layer[ii] == 0):
            ag.add_track(S2_x[ii]*1000+250, S2_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'InLayer2')
            ag.add_track(via_x*1000+250, via_y*1000+250, S2_x[ii+1]*1000+250, S2_y[ii+1]*1000+250, STRAND_THICK*1000, 'BottomLayer')
        else:
            ag.add_track(S2_x[ii]*1000+250, S2_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'BottomLayer')
            ag.add_track(via_x*1000+250, via_y*1000+250, S2_x[ii+1]*1000+250, S2_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer2')

for ii in range(len(S3_x)-1):
    if((S3_layer[ii] == 0) and (S3_layer[ii+1] == 0)):
        ag.add_track(S3_x[ii]*1000+250, S3_y[ii]*1000+250, S3_x[ii+1]*1000+250, S3_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer2')
    elif((S3_layer[ii] == 1) and (S3_layer[ii+1] == 1)):
        ag.add_track(S3_x[ii]*1000+250, S3_y[ii]*1000+250, S3_x[ii+1]*1000+250, S3_y[ii+1]*1000+250, STRAND_THICK*1000, 'BottomLayer')
    else:
        #points in different layers
        via_x = (S3_x[ii]+S3_x[ii+1])/2
        via_y = (S3_y[ii]+S3_y[ii+1])/2
        ag.add_via(via_x*1000+250,via_y*1000+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'InLayer2','BottomLayer')
        if(S3_layer[ii] == 0):
            ag.add_track(S3_x[ii]*1000+250, S3_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'InLayer2')
            ag.add_track(via_x*1000+250, via_y*1000+250, S3_x[ii+1]*1000+250, S3_y[ii+1]*1000+250, STRAND_THICK*1000, 'BottomLayer')
        else:
            ag.add_track(S3_x[ii]*1000+250, S3_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'BottomLayer')
            ag.add_track(via_x*1000+250, via_y*1000+250, S3_x[ii+1]*1000+250, S3_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer2')

for ii in range(len(S4_x)-1):
    if((S4_layer[ii] == 0) and (S4_layer[ii+1] == 0)):
        ag.add_track(S4_x[ii]*1000+250, S4_y[ii]*1000+250, S4_x[ii+1]*1000+250, S4_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer2')
    elif((S4_layer[ii] == 1) and (S4_layer[ii+1] == 1)):
        ag.add_track(S4_x[ii]*1000+250, S4_y[ii]*1000+250, S4_x[ii+1]*1000+250, S4_y[ii+1]*1000+250, STRAND_THICK*1000, 'BottomLayer')
    else:
        #points in different layers
        via_x = (S4_x[ii]+S4_x[ii+1])/2
        via_y = (S4_y[ii]+S4_y[ii+1])/2
        ag.add_via(via_x*1000+250,via_y*1000+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'InLayer2','BottomLayer')
        if(S4_layer[ii] == 0):
            ag.add_track(S4_x[ii]*1000+250, S4_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'InLayer2')
            ag.add_track(via_x*1000+250, via_y*1000+250, S4_x[ii+1]*1000+250, S4_y[ii+1]*1000+250, STRAND_THICK*1000, 'BottomLayer')
        else:
            ag.add_track(S4_x[ii]*1000+250, S4_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'BottomLayer')
            ag.add_track(via_x*1000+250, via_y*1000+250, S4_x[ii+1]*1000+250, S4_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer2')

for ii in range(len(S5_x)-1):
    if((S5_layer[ii] == 0) and (S5_layer[ii+1] == 0)):
        ag.add_track(S5_x[ii]*1000+250, S5_y[ii]*1000+250, S5_x[ii+1]*1000+250, S5_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer2')
    elif((S5_layer[ii] == 1) and (S5_layer[ii+1] == 1)):
        ag.add_track(S5_x[ii]*1000+250, S5_y[ii]*1000+250, S5_x[ii+1]*1000+250, S5_y[ii+1]*1000+250, STRAND_THICK*1000, 'BottomLayer')
    else:
        #points in different layers
        via_x = (S5_x[ii]+S5_x[ii+1])/2
        via_y = (S5_y[ii]+S5_y[ii+1])/2
        ag.add_via(via_x*1000+250,via_y*1000+250,STRAND_THICK*1000,STRAND_THICK*1000/2,'InLayer2','BottomLayer')
        if(S5_layer[ii] == 0):
            ag.add_track(S5_x[ii]*1000+250, S5_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'InLayer2')
            ag.add_track(via_x*1000+250, via_y*1000+250, S5_x[ii+1]*1000+250, S5_y[ii+1]*1000+250, STRAND_THICK*1000, 'BottomLayer')
        else:
            ag.add_track(S5_x[ii]*1000+250, S5_y[ii]*1000+250, via_x*1000+250, via_y*1000+250, STRAND_THICK*1000, 'BottomLayer')
            ag.add_track(via_x*1000+250, via_y*1000+250, S5_x[ii+1]*1000+250, S5_y[ii+1]*1000+250, STRAND_THICK*1000, 'InLayer2')

ag.save_script("test")

plt.axis('equal')
plt.show()