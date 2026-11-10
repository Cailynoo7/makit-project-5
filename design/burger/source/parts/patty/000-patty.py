from math import sin,cos,pi,exp,tanh
from random import Random
base=part('bottom_bun')
D=base.diameter
h=param('patty_height',5.0)
r=D*0.45
wav=param('patty_edge_texture',0.38)
shelf=param('switch_seat_height',2.5)
# A continuous displaced surface, with irregular bumps and shallow valleys.
relief=param('patty_surface_relief',0.65)
detail_count=int(param('patty_surface_features',150))
detail_seed=int(param('patty_surface_seed',73))
rng=Random(detail_seed)
features=[(rng.uniform(0,2*pi),rng.uniform(0.08,0.92),rng.uniform(0.75,1.55),rng.uniform(0.28,0.7),rng.uniform(-1,1)) for _ in range(detail_count)]
profile_keys=[(0,0.8),(0.1625,0),(0.5,0),(0.8375,0.1),(1,0.85)]
sections=[]
for j in range(17):
 t=j/16
 z=h*t
 for k in range(len(profile_keys)-1):
  t0,s0=profile_keys[k];t1,s1=profile_keys[k+1]
  if t0<=t<=t1:
   u=(t-t0)/(t1-t0); u=u*u*(3-2*u)
   shrink=s0+(s1-s0)*u
   break
 pts=[]
 for i in range(180):
  a=2*pi*i/180
  field=0
  for ac,tc,sw,sh,amp in features:
   da=(a-ac+pi)%(2*pi)-pi
   field+=amp*exp(-0.5*((r*da/sw)**2+((z-h*tc)/sh)**2))
  grain=relief*tanh(field)*max(0,sin(pi*t))**0.65
  rr=r-shrink+wav*(0.6*sin(17*a)+0.4*sin(29*a+0.9))+grain
  pts.append((rr*cos(a),rr*sin(a),z))
 sections.append(Face(Wire([Edge.make_spline(pts,periodic=True)])))
body=loft(sections)
body=body-Pos(0,0,shelf+10)*Box(base.cavity_w,base.cavity_w,20)
body=body-Box(base.pin_w,base.pin_w,20)
vendor=asset('design/burger/source/assets/29f4d60beb57a869d233939c629de23319458d225f0be6644fd86258533e3c9d.step')
# The switch and patty move down with the thinner lower bun; local datum is unchanged.
body=body-Pos(-49.9504975122655,86.0703258159004,-9.2)*vendor
body.color=srgb('#75412C')
publish('patty',body,'凹凸纹理肉饼',material='petg')
