import numpy as np
import bpy
from math import *
from mathutils import *


# Gravitational constant when the mass of the sun is 1.
G = 2.95912208286e-4

# Planet names and order
planets = ('Sun','Jupiter','Saturn','Uranus','Neptune','Pluto')

# The data below is obtained from here: https://ssd.jpl.nasa.gov/horizons.cgi

# Masses relative to the sun (the increased sun mass is to account for the inner planets)
masses = np.array([1.00000597682, 
                   0.000954786104043, 
                   0.000285583733151, 
                   0.0000437273164546, 
                   0.0000517759138449, 
                   6.571141277023631e-09])

# Positions of the planets in astronomical units (au) on September 5, 1994, at 0h00 GST.
positions = np.array([[0., 0., 0.],
                    [-3.502576677887171E+00, -4.111754751605156E+00,  9.546986420486078E-02],
                    [9.075323064717326E+00, -3.443060859273154E+00, -3.008002285860299E-01],
                    [8.309900066449559E+00, -1.782348877489204E+01, -1.738826162402036E-01],
                    [1.147049510166812E+01, -2.790203169301273E+01,  3.102324955757055E-01],
                    [-1.553841709421204E+01, -2.440295115792555E+01,  7.105854443660053E+00]])

# Velocities of the planets relative to the sun in au/day on September 5, 1994, at 0h00 GST.
velocities = np.array([[0., 0., 0.],
                    [5.647185685991568E-03, -4.540768024044625E-03, -1.077097723549840E-04],
                    [1.677252496875353E-03,  5.205044578906008E-03, -1.577215019146763E-04],
                    [3.535508197097127E-03,  1.479452678720917E-03, -4.019422185567764E-05],
                    [2.882592399188369E-03,  1.211095412047072E-03, -9.118527716949448E-05],
                    [2.754640676017983E-03, -2.105690992946069E-03, -5.607958889969929E-04]])

# Compute total linear momentum
ptot = (masses[:,np.newaxis]*velocities).sum(axis=0)

# Recompute velocities relative to the center of mass
velocities -= ptot/masses.sum()

# Linear momenta of the planets: p = m*v
momenta = masses[:,np.newaxis]*velocities

# Function for Newtonian acceleration field
def acc(x, masses = masses, G = G):
    N = masses.shape[0]
    d = x.shape[-1]
    dx_pairs = x[:, np.newaxis] - x[np.newaxis, :]
    msq_pairs = masses[:, np.newaxis]*masses[np.newaxis, :]
    
    # Remove self-self interactions
    dx_pairs = np.delete(dx_pairs.reshape((N*N,d)),slice(None,None,N+1), axis = 0).reshape((N,N-1,d))
    msq_pairs = np.delete(msq_pairs.reshape((N*N)),slice(None,None,N+1), axis = 0).reshape((N,N-1))
    
    # Compute pairwise distances
    dist_pairs = np.sqrt((dx_pairs**2).sum(axis=-1))
    
    # Compute the gravitational force using Newton's law
    forces = -G*(dx_pairs*msq_pairs[:,:,np.newaxis]/dist_pairs[:,:,np.newaxis]**3).sum(axis=1)
    
    # Return accelerations
    return forces/masses[:,np.newaxis]

# Select time step and total integration time (measured in days)
h = 100 # Time stepsize in days
totaltime = 100*365 # Total simulation time in days

# Preallocate output vectors at each step
t_out = np.arange(0.,totaltime,h)
x_out = np.zeros(t_out.shape + positions.shape, dtype=float)
x_out[0,:,:] = positions
v_out = np.zeros_like(x_out)
v_out[0,:,:] = velocities

# Use Symplectic Euler method for integration
for x0, x1, v0, v1 in zip(x_out[:-1],x_out[1:],v_out[:-1],v_out[1:]):
    x1[:,:] = x0 + h*v0
    v1[:,:] = v0 + h*acc(x1)


# -------------------------
# Adding the Blender code below
# -------------------------

obj_Sun = bpy.data.objects['Sun']
obj_Jupiter = bpy.data.objects['Jupiter']
obj_Saturn = bpy.data.objects['Saturn']
obj_Uranus = bpy.data.objects['Uranus']
obj_Neptune = bpy.data.objects['Neptune']
obj_Pluto = bpy.data.objects['Pluto']

# Clear all previous animation data
obj_Sun.animation_data_clear()
obj_Jupiter.animation_data_clear()
obj_Saturn.animation_data_clear()
obj_Uranus.animation_data_clear()
obj_Neptune.animation_data_clear()
obj_Pluto.animation_data_clear()


# set first and last frame index
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = 365

# loop of frames and insert keyframes every frame
nlast = bpy.context.scene.frame_end

for n in range(nlast):
    # Set frame like this
    bpy.context.scene.frame_set(n)

    # Set current location like this
    obj_Sun.location.x = x_out[n,0,0]
    obj_Sun.location.y = x_out[n,0,1]
    obj_Sun.location.z = x_out[n,0,2]

    obj_Jupiter.location.x = x_out[n,1,0]
    obj_Jupiter.location.y = x_out[n,1,1]
    obj_Jupiter.location.z = x_out[n,1,2]

    obj_Saturn.location.x = x_out[n,2,0]
    obj_Saturn.location.y = x_out[n,2,1]
    obj_Saturn.location.z = x_out[n,2,2]

    obj_Uranus.location.x = x_out[n,3,0]
    obj_Uranus.location.y = x_out[n,3,1]
    obj_Uranus.location.z = x_out[n,3,2]

    obj_Neptune.location.x = x_out[n,4,0]
    obj_Neptune.location.y = x_out[n,4,1]
    obj_Neptune.location.z = x_out[n,4,2]

    obj_Pluto.location.x = x_out[n,5,0]
    obj_Pluto.location.y = x_out[n,5,1]
    obj_Pluto.location.z = x_out[n,5,2]

    # Insert new keyframe for "location" like this
    obj_Sun.keyframe_insert(data_path="location")
    obj_Jupiter.keyframe_insert(data_path="location")
    obj_Saturn.keyframe_insert(data_path="location")
    obj_Uranus.keyframe_insert(data_path="location")
    obj_Neptune.keyframe_insert(data_path="location")
    obj_Pluto.keyframe_insert(data_path="location")
