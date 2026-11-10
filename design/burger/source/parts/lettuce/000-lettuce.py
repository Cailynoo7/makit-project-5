# cell: lettuce
from math import sin,cos,pi,atan2,hypot
base=part('bottom_bun')
D=base.diameter
th=param('lettuce_thickness',1.5)
wave=param('lettuce_wave',1.25)
corner_drop=param('lettuce_corner_drape',2.4)
lobes=param('lettuce_lobes',12)
center_w=param('lettuce_switch_opening',14.8)
flange_clearance=param('switch_flange_clearance',0.4)
guide_top=param('guide_height_above_tomato',10.9)
R=D/2
pts=[]
for i in range(25):
 x=-R+2*R*i/24
 row=[]
 for j in range(25):
  y=-R+2*R*j/24
  rr=hypot(x,y)/R
  a=atan2(y,x)
  z=3.4-0.5*rr**2+wave*sin(lobes*a+0.4)*rr**6-corner_drop*rr**6*((1+cos(4*a))/2)**4
  row.append((x,y,z-th))
 pts.append(row)
f=Face.make_surface_from_array_of_points(pts,tol=0.01,min_deg=3,max_deg=3)
body=Solid.extrude(f,(0,0,th))
outline=[]
for i in range(144):
 a=2*pi*i/144
 rr=R*(0.964+0.03*sin(lobes*a+0.4))
 outline.append((rr*cos(a),rr*sin(a),0))
foot=Face(Wire([Edge.make_spline(outline,periodic=True)]))
body=body & extrude(foot,10,both=True)
body=body+Pos(0,0,1.7)*Cylinder(D*0.34,3.4)
# Small clearance above the curved cheese underside avoids mesh contact ambiguity.
cheese_cut=Pos(0,0,3.28)*Rot(0,0,45)*Solid.extrude(part('cheese').f,(0,0,15))
body=body-cheese_cut
body=body-Pos(0,0,10)*Box(center_w,center_w,22)
body=body-Pos(0,0,flange_clearance/2)*Box(base.cavity_w,base.cavity_w,flange_clearance)
# Four posts also register the cheese and oppose top-cap tilt. Broad inner land holds glue.
for x,y in base.guide_xy:
 body=body+Pos(x,y,guide_top/2)*Cylinder(base.guide_d/2,guide_top)
# Four glue lands contact cheese away from functional guides.
for x,y in [(10,10),(-10,10),(-10,-10),(10,-10)]:
 body=body+Pos(x,y,1.7)*Cylinder(1.5,3.4)
body=body-cheese_cut
# Restore only guide portions extending above the cheese, outside cheese-cut footprint.
for x,y in base.guide_xy:
 body=body+Pos(x,y,guide_top/2)*Cylinder(base.guide_d/2,guide_top)
# Trim the small curled underside at the actual tomato contact face.
body=body-Pos(0,0,-part('tomato').h)*part('tomato').body
body.color=srgb('#88B544')
publish('lettuce',body,'波浪菜叶与导向',material='petg')
