#!/usr/bin/env python
# coding: utf-8

# Rezges-Lenges szimulacio

import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import argparse

# User interface for easier use
parser = argparse.ArgumentParser(description='Elastic pendulum simulation.')
parser.add_argument('-D', '--spring_constant',  default=50.0, type=np.float64)
parser.add_argument('-L', '--spring_length', default=1.2, type=np.float64)
parser.add_argument('-m', '--mass_of_body', default=2.0, type=np.float64)
parser.add_argument('-x', default=0.0, type=np.float64)
parser.add_argument('-y', default=0.0, type=np.float64)
parser.add_argument('-z', default=-1.0, type=np.float64)

args = parser.parse_args()

# Default Spring constant D
D = args.spring_constant

# Default Length L
L = args.spring_length

# Force of Gravity (vector format) 
G = np.array([0,0,-9.81], dtype=np.float64) # Can vary, based on where are you on earth.

# Linear body constant (at low velocity!)
C_lin = 1.0

# The mass of the body at the end of the elastic pendulum
m = args.mass_of_body


# Egyszeru mozgasegyenlet-megoldo
def lepes(xn, vn, m, F, dt):
    a = F(xn, vn, m) / m
    v_new = vn + a*dt
    x_new = xn + v_new*dt
    return (x_new, v_new)

# 3D rugo
def F_rugo(r, v, m):
    return (-D*r)

# 3D inga
def F_inga(r, v, m):
    # gravitacios ero:
    F_erinto = m * G * np.sin(r/L)
    return (F_erinto)


# 3D rugo linearis kozegellenallassal
def F_rugo_kozeg_lin(r, v, m):
    F = F_rugo(r, v, m) - C_lin*v
    return F

# 3D rugos-inga
def F_rugos_inga(r, v, m):
    F = F_rugo(r, v, m) + F_inga(r, v, m)
    return F

# 3D rugos-inga kozegellenallassal
def F_rugos_inga_kozeg(r, v, m):
    F = F_rugo_kozeg_lin(r, v, m) + F_inga(r, v, m)
    return F

def app():
    x0 = np.array([args.x, args.y, args.z], dtype=np.float64)
    v0 = np.array([0,0,0], dtype=np.float64)
    dt = 0.01

    F_fuggveny = F_rugos_inga # erofuggveny kivalasztasa

    x = x0; v = v0
    t = 0.0; t_max = 100.0

    t_list = []
    x_list = []
    v_list = []

    # szamitas
    while(t<=t_max+1e-6):
        t_list.append(t)
        v_list.append(v)
        x_list.append(x)
        x, v = lepes(x, v, m, F_fuggveny, dt)
        t += dt
        
    # tömbbé alakítjuk
    x_arr=np.asarray(x_list)
    v_arr=np.asarray(v_list)
    t_arr=np.asarray(t_list)

    # most kirajzoljuk
    """
    fig=plt.figure(figsize=(18,12))  
    ax1=fig.add_subplot(211) # két rész-grafikon
    ax2=fig.add_subplot(212)
    ax1.plot(t_list, x_arr[:,0], color="red") # az elsőbe az rx(t)
    ax1.plot(t_list, x_arr[:,1], color="blue")
    ax1.plot(t_list, x_arr[:,2], color="green")
    ax2.plot(t_list, v_arr[:,0], color="red")# a másodikba a vx(t)
    ax2.plot(t_list, v_arr[:,1], color="blue")
    ax2.plot(t_list, v_arr[:,2], color="green")
    ax1.grid()
    ax2.grid()
    ax1.set_xlabel("t")
    ax1.set_ylabel("x(t)")
    ax2.set_xlabel("t")
    ax2.set_ylabel("v_x(t)")
    """

    # 3D plot
    """
    fig2 = plt.figure(figsize=(15,15))
    ax1 = fig2.add_subplot(111, projection='3d')
    ax1.plot(x_arr[:,0], x_arr[:,1], x_arr[:,2])
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')
    """
    
    # 3D anim
    history_len = x_arr.shape[0]
    fig3 = plt.figure(figsize=(15,15))
    axf3 = fig3.add_subplot(projection='3d')
    axf3.grid()

    fixation_point = np.array([0.0, 0.0, L], dtype=np.float64)

    line, = axf3.plot([], [], [], '.-', lw=1, ms=2)
    body, = axf3.plot([], [], [], 'ro')
    pend, = axf3.plot([], [], [], '-', color='green')
    axf3.set(xlim3d=(x_arr[:,:].min(), x_arr[:,:].max()), xlabel='X')
    axf3.set(ylim3d=(x_arr[:,:].min(), x_arr[:,:].max()), ylabel='Y')
    axf3.set(zlim3d=(x_arr[:,:].min(), x_arr[:,:].max()), zlabel='Z')
    time_template = 'time = %.1fs'
    time_template = 'time = %.1fs'
    time_template = 'time = %.1fs'
    time_text = axf3.text(0.05, 0.05, 0.9, s='', transform=axf3.transAxes)

    def animate(i, x, y, z):
        line.set_data(x[:i], y[:i])
        line.set_3d_properties(z[:i])
        body.set_data(x[i], y[i])
        body.set_3d_properties(z[i])
        pend.set_data(np.array([fixation_point[0], x[i]]),np.array([fixation_point[1], y[i]]))
        pend.set_3d_properties(np.array([fixation_point[2], z[i]]))
        time_text.set_text(time_template % (i*dt))
        return line, body, pend, time_text

    ani = animation.FuncAnimation(
            fig3, animate, fargs=(x_arr[:,0], x_arr[:,1], x_arr[:,2]),
    interval=dt, blit=True)

    plt.show()

def main():
    app() 

if __name__ == "__main__":
    main()
