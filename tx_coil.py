import numpy as np
import matplotlib.pyplot as plt
import math
from altium_gen import AltiumScriptGenerator

# ==============================================================================
# Parametri sensore
# ==============================================================================
Npts = 2000

x_offset = 100                      # [mm]
y_offset = 100                      # [mm]

Dint = 58.50                         # [mm]
Dext = 64.75                           # [mm]

Rin  = Dint/2
Rout = Dext/2

Rmid = (Rin + Rout)/2
Amp  = (Rout - Rin)/2

n_turns_per_layer = 2               #[-]
delta_deg         = 10.0            #[°]

coil_ph_deg     = -11.25      #[°]
coil_ph_aperture_deg = 0            #[°]

chamfer_angle_deg = 45              #[°]
chamfer_n = 4                       #[-]
chamfer_radial_amplitude = 6.75     #[mm]
chamfer_center_radius   = 37.5      #[mm]
chamfer_angular_amplitude_deg = 14  #[°]

trace_w         = 0.45              #[mm]
via_rad         = 0.25              #[mm]

delta   = np.deg2rad(delta_deg)
coil_ph = np.deg2rad(coil_ph_deg)
coil_ph_aperture = np.deg2rad(coil_ph_aperture_deg)
chamfer_angle = np.deg2rad(chamfer_angle_deg)
chamfer_angular_amplitude = np.deg2rad(chamfer_angular_amplitude_deg)
# ==============================================================================

angle_pts1 = np.linspace(coil_ph +  coil_ph_aperture,n_turns_per_layer * 2 * np.pi + coil_ph, Npts)
angle_pts2 = np.linspace(coil_ph,n_turns_per_layer * 2 * np.pi + coil_ph - coil_ph_aperture, Npts)

R_max = Rmid + (Rout-Rin) / (2)-2*trace_w
R_min = Rmid - (Rout-Rin) / (2)+2*trace_w

print(R_max)
print(R_min)

chamfer_angular_distance = 2 * math.pi / chamfer_n

dr = (R_max - R_min) / (n_turns_per_layer * 2 * math.pi)
r1 = np.zeros(len(angle_pts1))
r2 = np.zeros(len(angle_pts2))
x1 = np.zeros(len(angle_pts1))
y1 = np.zeros(len(angle_pts1))
x2 = np.zeros(len(angle_pts2))
y2 = np.zeros(len(angle_pts2))

ag = AltiumScriptGenerator()

for ii in range(len(angle_pts1)):
    th = angle_pts1[ii]
    th_reduced = th % (2 * math.pi / 4)

    r1[ii] = R_min + dr * (th-coil_ph)

    x_c = (trace_w/2 + chamfer_center_radius) * math.cos(chamfer_angle)
    y_c = (trace_w/2 + chamfer_center_radius) * math.sin(chamfer_angle)

    #calculate angle of chamfer center polar coordinates
    th_c = math.atan2(Rout * math.sin(th_reduced) - y_c,Rout * math.cos(th_reduced) - x_c)

    #calculate cartesian coordinates of chamfer center
    x_ch = (chamfer_radial_amplitude) * math.cos(th_c)
    y_ch = (chamfer_radial_amplitude) * math.sin(th_c)

    r_var = Rout - math.sqrt((x_ch + x_c)**2 + (y_ch + y_c)**2)

    if((th_reduced >= (chamfer_angle - chamfer_angular_amplitude / 2) and th_reduced <= (chamfer_angle + chamfer_angular_amplitude / 2))):
        r1[ii] -= r_var
    
    x1[ii] = r1[ii] * math.cos(th)
    y1[ii] = r1[ii] * math.sin(th)

for ii in range(len(angle_pts2)):
    th = angle_pts2[ii]
    th_reduced = th % (2 * math.pi / 4)

    r2[ii] = R_max - dr * (th-coil_ph)

    x_c = (trace_w/2+chamfer_center_radius) * math.cos(chamfer_angle)
    y_c = (trace_w/2+chamfer_center_radius) * math.sin(chamfer_angle)
    
    #calculate angle of chamfer center polar coordinates
    th_c = math.atan2(Rout * math.sin(th_reduced) - y_c,Rout * math.cos(th_reduced) - x_c)
    
    #calculate cartesian coordinates of chamfer center
    x_ch = (chamfer_radial_amplitude) * math.cos(th_c)
    y_ch = (chamfer_radial_amplitude) * math.sin(th_c)
    
    r_var = Rout - math.sqrt((x_ch + x_c)**2 + (y_ch + y_c)**2)
    
    if((th_reduced >= (chamfer_angle - chamfer_angular_amplitude / 2) and th_reduced <= (chamfer_angle + chamfer_angular_amplitude / 2))):
        r2[ii] -= r_var
    
    x2[ii] = r2[ii] * math.cos(th)
    y2[ii] = r2[ii] * math.sin(th)

for ii in range(len(angle_pts1)-1):
    ag.add_track(x_offset + x1[ii],y_offset + y1[ii],x_offset + x1[ii+1],y_offset + y1[ii+1],trace_w,'InLayer2')

for ii in range(len(angle_pts2)-1):    
    ag.add_track(x_offset + x2[ii],y_offset + y2[ii],x_offset + x2[ii+1],y_offset + y2[ii+1],trace_w,'BottomLayer')

ag.add_via(x_offset+(R_max+0*(via_rad-trace_w/2)) * math.cos(coil_ph),y_offset + (R_max+0*(via_rad-trace_w/2)) * math.sin(coil_ph),2*via_rad,via_rad,'InLayer2','BottomLayer')
ag.add_via(x_offset+(R_min-via_rad+trace_w/2) * math.cos(angle_pts2[-1]),y_offset+(R_min-via_rad+trace_w/2) * math.sin(angle_pts2[-1]),2*via_rad,via_rad,'InLayer2','BottomLayer')
ag.save_script("test.pas")

plt.plot(x1,y1,'r') 
plt.plot(x2,y2,'b')
plt.axis('square')
plt.show()

