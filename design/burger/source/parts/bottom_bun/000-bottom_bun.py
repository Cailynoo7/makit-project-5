diameter = param('body_diameter',50.0)
h = param('bottom_height',6.5)
r = diameter*0.456
edge_r = param('bottom_edge_radius',0.45)
foot_r = param('bottom_foot_radius',19.2)
top_round = param('bottom_top_edge_radius',0.8)
pin_w=param('pin_well_width',9.8)
floor=param('pin_well_floor',2.8)
cavity_w=param('switch_chamber_width',17.4)
guide_r=param('guide_circle_radius',14.5)
guide_d=param('guide_post_diameter',3.2)
guide_xy=[(guide_r,0),(0,guide_r),(-guide_r,0),(0,-guide_r)]
# Gentle upper side; inward slope increases progressively toward the rounded foot.
taper_power=param('bottom_taper_exponent',3.0)
pts=[]
for k in range(31):
 z=h*k/30
 rr=r-(r-foot_r)*(1-z/h)**taper_power
 pts.append((rr,0,z))
profile=Wire([
 Edge.make_line((0,0,0),pts[0]),
 Edge.make_spline(pts),
 Edge.make_line(pts[-1],(0,0,h)),
 Edge.make_line((0,0,h),(0,0,0))
])
body=revolve(Face(profile),axis=Axis.Z)
body=fillet(body.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[-1:],top_round)
body=fillet(body.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[:1],edge_r)
body=body-Pos(0,0,floor+10)*Box(pin_w,pin_w,20)
body.color=srgb('#DEA359')
publish('bottom_bun',body,'底面包',material='pla')
