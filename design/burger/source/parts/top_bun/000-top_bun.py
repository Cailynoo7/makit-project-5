# cell: top_bun
# cell: top_bun
from math import sin,cos,pi,sqrt,atan,degrees,hypot,exp
from random import Random
base=part('bottom_bun')
D=base.diameter
h=param('top_height',18.5)
r=D*0.45
power=param('crown_fullness',2.6)
edge_r=param('top_rim_radius',1.0)
skirt_inset=param('crown_skirt_inset',0.9)
skirt_h=param('crown_skirt_height',2.6)
guide_hole=param('cap_guide_bore',3.8)
socket_d=param('stem_socket_outer',6.2)
socket_w=param('stem_socket_width',4.8)
socket_drop=param('stem_socket_drop',1.4)
cross_span=param('stem_cross_span',4.06)
cross_web=param('stem_cross_web',1.16)
pocket_w=param('housing_relief_width',16.8)
pocket_depth=param('housing_relief_depth',2.0)
seed_l=param('sesame_length',2.2)
seed_w=param('sesame_width',1.6)
seed_h=param('sesame_height',0.9)
count=int(param('sesame_count',24))
scatter=int(param('sesame_scatter_seed',47))
def crown(rx,hh):
 pts=[]
 for k in range(61):
  t=pi/2*(1-k/60)
  if k==0: p=(rx-skirt_inset,0,0)
  elif k==60: p=(0,0,hh)
  else:
   z=hh*cos(t)**(2/power)
   rr=rx*sin(t)**(2/power)-skirt_inset*exp(-(z/skirt_h)**2)
   p=(rr,0,z)
  pts.append(p)
 wire=Wire([Edge.make_line((0,0,0),pts[0]),Edge.make_spline(pts),Edge.make_line(pts[-1],(0,0,0))])
 return revolve(Face(wire),axis=Axis.Z)
outer=crown(r,h)
outer=fillet(outer.edges().sort_by(Axis.Z)[:1],edge_r)
# Solid bun: no broad internal shell cavity.
body=outer
# Local switch-housing clearance is shallow and leaves the central stem socket intact.
relief=Pos(0,0,-0.1)*extrude(RectangleRounded(pocket_w,pocket_w,0.8),pocket_depth+0.1)
socket_profile=RectangleRounded(socket_w,socket_d,0.6)
relief=relief-Pos(0,0,-1)*extrude(socket_profile,pocket_depth+2)
body=body-relief
socket_top=pocket_depth+0.3
body=body+Pos(0,0,-socket_drop)*extrude(socket_profile,socket_top+socket_drop)
for x,y in base.guide_xy:
 body=body-Pos(x,y,3.4)*Cylinder(guide_hole/2,7.2)
# The raised upper stack uses a longer socket; its roof remains on the real stem top.
roof=param('stem_bore_roof_local',0.55)
cut_h=roof+socket_drop+0.1
body=body-Pos(0,0,(roof-socket_drop-0.1)/2)*Box(cross_span,cross_web,cut_h)
body=body-Pos(0,0,(roof-socket_drop-0.1)/2)*Box(cross_web,cross_span,cut_h)
body.color=srgb('#D99548')
publish('top_bun',body,'实心圆顶面包',material='pla')
# Rejection sampling uses no angular progression or ring phase: no spiral pattern.
rng=Random(scatter)
points=[]
for attempt in range(10000):
 x,y=rng.uniform(-r*0.86,r*0.86),rng.uniform(-r*0.86,r*0.86)
 rad=hypot(x,y)
 if rad>r*0.86: continue
 if any(hypot(x-px,y-py)<4.5 for px,py in points): continue
 points.append((x,y))
 if len(points)==count: break
assert len(points)==count
seeds=[]
for x,y in points:
 rad=hypot(x,y)
 u=rad/r
 z=h*(1-u**power)**(1/power)
 slope=(h/r)*u**(power-1)*(1-u**power)**(1/power-1)
 tilt=degrees(atan(slope))
 from math import atan2
 yaw=degrees(atan2(y,x))
 seed=scale(Sphere(1),by=(seed_l/2,seed_w/2,seed_h/2))
 seed=Pos(x,y,z+0.12)*Rot(0,0,yaw)*Rot(0,tilt,0)*Rot(0,0,rng.uniform(0,360))*seed
 seeds.append(seed)
# Subtract the complete external bun solid: only the exposed sesame cap remains.
seed_body=Compound(children=seeds)-outer
assert len(seed_body.solids())==count
seed_body.color=srgb('#FFF0CD')
publish('sesame',seed_body,'自然散点白芝麻',material='pla')
