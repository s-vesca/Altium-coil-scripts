import numpy as np
import matplotlib.pyplot as plt
import math
from altium_gen import AltiumScriptGenerator

# ==========================================
# Parametri sensore
# ==========================================
Npts = 2000 
x_offset = 100                  # [mm]
y_offset = 100                  # [mm]

Dint = 39.5                     # [mm]
Dext = 49.0                     # [mm]

Rin  = Dint/2
Rout = Dext/2

Rmid = (Rin + Rout)/2
Amp  = (Rout - Rin)/2

periods         = 4             #[-]
delta_deg       = 10.0           #[°]

coil_ph_deg     = 0/periods             #[°]

revpt_angle_deg = 135+45/2
revpt_amp_deg = 0.5
revpt_via_angle_pos = 7 / 4

trace_w         = 0.2           #[mm]
via_rad         = 0.3           #[mm]

nw = 2

delta   = np.deg2rad(delta_deg)
coil_ph = np.deg2rad(coil_ph_deg)

# nw avvolgimenti sfalsati di delta°
start_phases = np.deg2rad([ii*delta_deg + coil_ph_deg for ii in range(nw)])
via_phases = np.array([[val * math.pi / periods + start_phases[jj] for jj in range(nw)] for val in range(2*periods)])

# ==========================================

angle_pts = np.linspace(0,2*np.pi,Npts)

r_top = np.zeros([len(angle_pts),nw])
r_bot = np.zeros([len(angle_pts),nw])

x_top = np.zeros([len(angle_pts),nw])
y_top = np.zeros([len(angle_pts),nw])
x_bot = np.zeros([len(angle_pts),nw])
y_bot = np.zeros([len(angle_pts),nw])

th_base = 0
th_base_prev = 0

jump_idx = [[] for jj in range(nw)]

for jj in range(nw):
    for ii in range(len(angle_pts)):

        th = angle_pts[ii] - jj * delta - coil_ph
        if (th > math.radians(revpt_angle_deg - revpt_amp_deg)) and (th < math.radians(revpt_angle_deg + revpt_amp_deg)):
            continue
        th_base = th
        while(th_base > 2*math.pi/periods):
            th_base = th_base - 2*math.pi/periods
        while(th_base < 0.0):
            th_base = th_base + 2*math.pi/periods

        if(th_base >= 0 and th_base < math.pi/periods):
            r_top[ii][jj] = Rmid + Amp * math.cos(th*periods)
            r_bot[ii][jj] = Rmid - Amp * math.cos(th*periods)
            if(th_base_prev >= math.pi/periods):
                #save index
                jump_idx[jj].append(ii)
        else:
            r_top[ii][jj] = Rmid - Amp * math.cos(th*periods)
            r_bot[ii][jj] = Rmid + Amp * math.cos(th*periods)
            if(th_base_prev >= 0 and th_base_prev < math.pi/periods):
                #save index
                jump_idx[jj].append(ii)

        th_base_prev = th_base

    for ii in range(len(angle_pts)):
        th = angle_pts[ii]
        x_top[ii][jj] = r_top[ii][jj] * math.cos(th)
        y_top[ii][jj] = r_top[ii][jj] * math.sin(th)
        x_bot[ii][jj] = r_bot[ii][jj] * math.cos(th)
        y_bot[ii][jj] = r_bot[ii][jj] * math.sin(th)


ag = AltiumScriptGenerator()

print(jump_idx)

for jj in range(nw):
    list_idx = jump_idx[jj]
    for ii in range(len(list_idx)+1):
        if ii == 0:
            first_idx = 0
        else:
            first_idx = list_idx[ii-1]

        if ii == (len(list_idx)):
            last_idx = len(angle_pts)
        else:
            last_idx = list_idx[ii]

        plt.figure(3)
        kk = first_idx
        while kk < (last_idx-1):
            ag.add_track(x_offset + x_top[kk][jj],y_offset + y_top[kk][jj],x_offset + x_top[kk+1][jj],y_offset + y_top[kk+1][jj],trace_w,'TopLayer')
            ag.add_track(x_offset + x_bot[kk][jj],y_offset + y_bot[kk][jj],x_offset + x_bot[kk+1][jj],y_offset + y_bot[kk+1][jj],trace_w,'BottomLayer')
            if(np.abs(x_offset + x_top[kk][jj]-(x_offset + x_top[kk+1][jj]))>1):
                print("mandi")
            plt.plot([x_offset + x_top[kk][jj],x_offset + x_top[kk+1][jj]],[y_offset + y_top[kk][jj],y_offset + y_top[kk+1][jj]],'red')
            kk += 1

for jj in range(nw):
    for ii in range(len(via_phases)):
        ph = via_phases[ii][jj]

        ag.add_via(x_offset + (Rmid + Amp + via_rad-trace_w/2)*math.cos(ph),y_offset + (Rmid + Amp + via_rad-trace_w/2)*math.sin(ph),via_rad*2,via_rad,'TopLayer','BottomLayer')
        ag.add_via(x_offset + (Rmid - Amp - via_rad+trace_w/2)*math.cos(ph),y_offset + (Rmid - Amp - via_rad+trace_w/2)*math.sin(ph),via_rad*2,via_rad,'TopLayer','BottomLayer')

    ag.add_via(x_offset + Rmid * math.cos(coil_ph + math.radians(revpt_angle_deg + revpt_amp_deg * revpt_via_angle_pos) + delta * jj), y_offset + Rmid * math.sin(coil_ph + math.radians(revpt_angle_deg + revpt_amp_deg * revpt_via_angle_pos) + delta * jj),via_rad*2,via_rad,'TopLayer','BottomLayer')
    ag.add_via(x_offset + Rmid * math.cos(coil_ph + math.radians(revpt_angle_deg - revpt_amp_deg * revpt_via_angle_pos) + delta * jj), y_offset + Rmid * math.sin(coil_ph + math.radians(revpt_angle_deg - revpt_amp_deg * revpt_via_angle_pos) + delta * jj),via_rad*2,via_rad,'TopLayer','BottomLayer')

ag.save_script("test.pas")

plt.figure(1)
plt.plot(angle_pts,r_top,'r.',label='top')
plt.plot(angle_pts,r_bot,'b.',label='bot')
plt.legend()

plt.figure(2)
for jj in range(nw): 
    plt.plot(x_top[:,jj],y_top[:,jj],'r.',label='top',markersize=1)
    plt.plot(x_bot[:,jj],y_bot[:,jj],'b.',label='bot',markersize=1)
    plt.plot((Rmid + Amp + via_rad-trace_w) * np.array([math.cos(val) for val in via_phases[:,jj]]),(Rmid + Amp + via_rad-trace_w) * np.array([math.sin(val) for val in via_phases[:,jj]]), 'g.',label = 'via', markersize = 10)
    plt.plot((Rmid - Amp - via_rad+trace_w) * np.array([math.cos(val) for val in via_phases[:,jj]]),(Rmid - Amp - via_rad+trace_w) * np.array([math.sin(val) for val in via_phases[:,jj]]), 'g.',label = 'via', markersize = 10)
plt.legend()
plt.axis('square')
plt.grid()
plt.show()