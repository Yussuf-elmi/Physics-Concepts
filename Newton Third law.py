#!/usr/bin/env python3
"""
Newton's Third Law — Visual Demo

Run this file in VS Code or any Python environment.
A matplotlib window will open and animate two masses with equal & opposite forces.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# === Parameters (edit these if you want, no need for input prompts) ===
m1 = 1.0        # kg, mass of object 1
m2 = 2.0        # kg, mass of object 2
F = 5.0         # N, force applied on mass1 to the right (mass2 gets -F)
dt_force = 0.5  # seconds, duration of applied force
total_time = 5  # total simulation time
dt = 0.02       # timestep for integration

# === Physics setup ===
a1 = F / m1
a2 = -F / m2

print("=== Newton's Third Law: Visualization ===")
print(f"Force on mass1: +{F:.2f} N → Acceleration a1 = {a1:.2f} m/s²")
print(f"Force on mass2: -{F:.2f} N → Acceleration a2 = {a2:.2f} m/s²")
print("Equal & opposite forces, different accelerations (because of different masses).")

# Initial positions and velocities
x1, v1 = -1.0, 0.0
x2, v2 =  1.0, 0.0

positions1 = []
positions2 = []
times = np.arange(0, total_time, dt)

for t in times:
    if t <= dt_force:
        cur_a1, cur_a2 = a1, a2
    else:
        cur_a1, cur_a2 = 0, 0

    v1 += cur_a1 * dt
    v2 += cur_a2 * dt
    x1 += v1 * dt
    x2 += v2 * dt

    positions1.append(x1)
    positions2.append(x2)

# === Visualization with matplotlib ===
fig, ax = plt.subplots(figsize=(8, 3))
ax.set_xlim(-5, 5)
ax.set_ylim(-2, 2)
ax.set_yticks([])
ax.set_xlabel("Position (m)")
ax.set_title("Newton's Third Law — Equal & Opposite Forces")

# Draw ground line
ax.hlines(-1, -5, 5, linewidth=1)

# Mass markers
mass1_circle = plt.Circle((positions1[0], 0), 0.2, color="blue")
mass2_circle = plt.Circle((positions2[0], 0), 0.2, color="red")
ax.add_patch(mass1_circle)
ax.add_patch(mass2_circle)

# Text info
info_text = ax.text(-4.5, 1.5, "", fontsize=9, family="monospace")

# Arrow scale (for drawing forces visually)
arrow_scale = 0.15

def update(i):
    t = times[i]
    x1, x2 = positions1[i], positions2[i]
    mass1_circle.center = (x1, 0)
    mass2_circle.center = (x2, 0)

    # Forces during force application
    if t <= dt_force:
        cur_F1, cur_F2 = F, -F
    else:
        cur_F1, cur_F2 = 0, 0

    # Clear old arrows
    [c.remove() for c in ax.collections if isinstance(c, plt.Quiver)]
    # Draw new arrows
    ax.quiver([x1], [0], [cur_F1 * arrow_scale], [0], angles="xy", scale_units="xy", scale=1, color="blue")
    ax.quiver([x2], [0], [cur_F2 * arrow_scale], [0], angles="xy", scale_units="xy", scale=1, color="red")

    info_text.set_text(
        f"t = {t:.2f} s\n"
        f"Force1 = {cur_F1:.2f} N, a1 = {cur_F1/m1 if m1!=0 else 0:.2f} m/s²\n"
        f"Force2 = {cur_F2:.2f} N, a2 = {cur_F2/m2 if m2!=0 else 0:.2f} m/s²"
    )

    return mass1_circle, mass2_circle, info_text

ani = animation.FuncAnimation(fig, update, frames=len(times), interval=dt*1000, blit=False, repeat=False)

plt.tight_layout()
plt.show()
