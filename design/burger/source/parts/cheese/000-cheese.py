from math import pi,hypot
base=part('bottom_bun')
side=param('cheese_side',42.0)
th=param('cheese_thickness',1.4)
droop=param('cheese_corner_droop',2.0)
center_w=param('cheese_center_opening',15.2)
guide_hole=param('cheese_guide_hole',4.0)
corner_inset=param('cheese_corner_inset',5.0)
edge_r=param('cheese_edge_radius',0.3)
a=side/2
pts=[]
for i in range(13):
 x=-a+side*i/12
 row=[]
 for j in range(13):
  y=-a+side*j/12
  q=((x*y)/(a*a))**2
  rad=hypot(x,y)
  factor=1-corner_inset*q/rad if rad>0 else 1
  z=-droop*q
  row.append((x*factor,y*factor,z))
 pts.append(row)
f=Face.make_surface_from_array_of_points(pts,tol=0.005,min_deg=3,max_deg=3)
body=Solid.extrude(f,(0,0,th))
body=fillet(body.edges(),edge_r)
body=body-Rot(0,0,-45)*Box(center_w,center_w,20)
for x,y in base.guide_xy:
 body=body-Rot(0,0,-45)*Pos(x,y,0)*Cylinder(guide_hole/2,20)
body.color=srgb('#F2BC3E')
publish('cheese',body,'垂角芝士',material='pla')
