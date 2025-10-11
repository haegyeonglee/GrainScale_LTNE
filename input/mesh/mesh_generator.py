#!/usr/bin/env python3

"""
This is script to generate mesh file with Gmsh. By specifying grain size (05mm/10mm/15mm/20mm/25mm/30mm),
the coordinate and diameter of the specific grain size will be given from the external file ('sq_circle_<grain_size>.txt').

Author: Haegyeong Lee
"""

import os
import sys
import gmsh

# Get the path of the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change current working directory to the script directory
os.chdir(script_dir)

############################################################################
#                                                                          #
#  Please provide grain size for the model: 05mm/10mm/15mm/20mm/25mm/30mm  #
#                                                                          #
############################################################################

grain_size = '05mm'

############################################################################

# File with coordinates and diameter of the grain
filename_circle = 'sq_circle_'+grain_size + ".txt"
filename = 'sq_circle_'+grain_size
filename_msh = filename + ".msh"

# 2D mesh size for outer boundary
xmin = 0
xmax = 0.29
ymin = 0
ymax = 0.40

# Outer boundary discretization
number_nodes_on_mesh_top_line = 290
number_nodes_on_mesh_bottom_line = 290
number_nodes_on_mesh_right_line = 400
number_nodes_on_mesh_left_line = 400



gmsh.initialize()
gmsh.model.add("main")

# Create outer boundary
t1 = gmsh.model.geo.addPoint(xmin, ymax, 0)
t2 = gmsh.model.geo.addPoint(xmax, ymax, 0)
t3 = gmsh.model.geo.addPoint(xmin, ymin, 0)
t4 = gmsh.model.geo.addPoint(xmax, ymin, 0)
outer_lines = []
outer_lines.append(gmsh.model.geo.addLine(t1, t2))
outer_lines.append(gmsh.model.geo.addLine(t2, t4))
outer_lines.append(gmsh.model.geo.addLine(t4, t3))
outer_lines.append(gmsh.model.geo.addLine(t3, t1))
outer_curve_loop = gmsh.model.geo.addCurveLoop(outer_lines)

# Create a circle at the center of the model
circle_lines = []

with open(filename_circle, 'r') as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith("x") or line.startswith("#") or len(line) == 0:
            continue
        cx, cy, diam = map(float, line.split())
        r = 0.5 * diam
        tag1 = gmsh.model.geo.addPoint(cx, cy + r, 0.0)
        tagc = gmsh.model.geo.addPoint(cx, cy, 0.0)
        tag2 = gmsh.model.geo.addPoint(cx, cy - r, 0.0)
        circle_lines.append(gmsh.model.geo.addCircleArc(tag1, tagc, tag2))
        circle_lines.append(gmsh.model.geo.addCircleArc(tag2, tagc, tag1))
        circle_curve_loop = gmsh.model.geo.addCurveLoop(circle_lines[-2:])

# Create hole surface
fluid_plane_surface = gmsh.model.geo.addPlaneSurface([outer_curve_loop] + [circle_curve_loop])
# Create hole surfaces = the grain
circle_plane_surface = gmsh.model.geo.addPlaneSurface([circle_curve_loop])

# Meshing controls

gmsh.model.geo.mesh.setTransfiniteCurve(outer_lines[0], number_nodes_on_mesh_top_line)
gmsh.model.geo.mesh.setTransfiniteCurve(outer_lines[1], number_nodes_on_mesh_right_line)
gmsh.model.geo.mesh.setTransfiniteCurve(outer_lines[2], number_nodes_on_mesh_bottom_line)
gmsh.model.geo.mesh.setTransfiniteCurve(outer_lines[3], number_nodes_on_mesh_left_line)

# Circle discretization
number_nodes_on_half_circle_bdy = int((diam*3.14)/0.001) # 0.0005 m for the whole circle

if number_nodes_on_half_circle_bdy % 2 == 0:
    number_nodes_on_half_circle_bdy = number_nodes_on_half_circle_bdy + 1


for line in circle_lines:
    gmsh.model.geo.mesh.setTransfiniteCurve(line, number_nodes_on_half_circle_bdy + 1)

# Add everything above to the model
gmsh.model.geo.synchronize()

# Define outer boundary names: left, right, bottom, top
tag_left = gmsh.model.addPhysicalGroup(1, [t4])
gmsh.model.setPhysicalName(1, tag_left, "left")
tag_right = gmsh.model.addPhysicalGroup(1, [t2])
gmsh.model.setPhysicalName(1, tag_right, "right")
tag_bottom = gmsh.model.addPhysicalGroup(1, [t3])
gmsh.model.setPhysicalName(1, tag_bottom, "bottom")
tag_top = gmsh.model.addPhysicalGroup(1, [t1])
gmsh.model.setPhysicalName(1, tag_top, "top")

# Define the fluid domain
tag_fluid = gmsh.model.addPhysicalGroup(2, [fluid_plane_surface])
gmsh.model.setPhysicalName(2, tag_fluid, "domain")

# Define the grain
tag_grain = gmsh.model.addPhysicalGroup(2, [circle_plane_surface])
gmsh.model.setPhysicalName(2, tag_grain, "g1")

# Mesh    
gmsh.model.geo.synchronize()
gmsh.option.setNumber("Mesh.Smoothing", 100)
gmsh.model.mesh.generate(2)

# Saving .msh file
gmsh.write(filename_msh)

# Finalizing and visualization on GUI
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()
gmsh.finalize()

sys.exit(0)

