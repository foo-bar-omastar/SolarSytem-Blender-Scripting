# Blender using Python Scripting - Outer Solar System
Simulating the outer Solar System (Jupiter, Saturn, Uranus, Neptune and Pluto) and visualize the result in Blender using Python Scripting.

**Please note that the scripts are only used for setting up the position of the planets and animation of planet movements**

Before executing the python script, ensure all Textures for planets have been downloaded and setup separately in Blender as per below guidelines:

* Create Six Spheres, preferably proportinal in size and relative to each other
* Since planets in reality are quite far from each other, it is recommended that the distances be reduced in proportion to loosely emulate the actual solar system
* The textures for each of the planets can be downloaded from any website, such as [http://planetpixelemporium.com/planets.html](http://planetpixelemporium.com/planets.html)

Once the above is done, the python script can be executed. Ensure that the names of the objects in the script match the planet object names.

The python script adds keyframes to Blender for the corresponding positions of the planets. Each time step is 100 days. Thus, with the default setting of 24 frames per second, each second of the animation corresponds to 24*100 days. Altogether that gives us 365 frames (thus corresponding to 100 years). The initial data for the planets is from September 5, 1994, at 0h00 GST. Thus, at the end of the animation we are at year 2094.

The camera animation is added manually and rendered in a way where the camera is locked on to the sun.

## Output Video: https://www.youtube.com/watch?v=PxX3_PVr2cg
