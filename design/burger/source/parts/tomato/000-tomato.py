base=part('bottom_bun')
D=base.diameter
h=param('tomato_height',3.0)
r=D*0.437
edge_r=param('tomato_edge_radius',0.65)
body=Pos(0,0,h/2)*Cylinder(r,h)
body=fillet(body.edges().filter_by(GeomType.CIRCLE),edge_r)
body=body-Box(base.cavity_w,base.cavity_w,20)
loop_outer=param('hanger_outer_radius',4.2)
loop_inner=param('hanger_inner_radius',2.0)
loop_y=param('hanger_center_y',24.8)
loop_angle=param('hanger_rotation_deg',-39.4)
loop_th=h
root_y=param('hanger_root_y',20.0)
# Integral tomato eye, slightly extended toward the rear diagonal lettuce valley.
outline=Wire([
 Edge.make_line((-loop_outer,root_y,0),(loop_outer,root_y,0)),
 Edge.make_line((loop_outer,root_y,0),(loop_outer,loop_y,0)),
 Edge.make_three_point_arc((loop_outer,loop_y,0),(0,loop_y+loop_outer,0),(-loop_outer,loop_y,0)),
 Edge.make_line((-loop_outer,loop_y,0),(-loop_outer,root_y,0))
])
eye=Solid.extrude(Face(outline),(0,0,loop_th))
eye=fillet(eye.edges(),0.45)
hole=(Pos(0,loop_y,loop_th/2)*Cylinder(loop_inner,loop_th+2)) & Pos(0,loop_y+loop_inner/2,loop_th/2)*Box(2*loop_inner,loop_inner,loop_th+2)
eye=eye-hole
body=body+Rot(0,0,loop_angle)*eye
body.color=srgb('#D74436')
publish('tomato',body,'番茄片与挂孔',material='petg')
