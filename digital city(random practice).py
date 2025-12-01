import bpy
import random

if bpy.context.object is not None and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60
bpy.context.scene.frame_current = 1

row_count = 10
col_count = 10
gap = 4   

for x in range(row_count):
    for y in range(col_count):

        x_pos = x * gap
        y_pos = y * gap
        
        base_size = 1
        
        bpy.ops.mesh.primitive_cube_add(size=base_size, location=(x_pos, y_pos, 0))
        obj = bpy.context.object
        
        bpy.ops.object.mode_set(mode='EDIT')           
        bpy.ops.transform.translate(value=(0, 0, base_size / 2)) 
        bpy.ops.object.mode_set(mode='OBJECT')         
        
        rand_width_x = random.uniform(1.0, 3.5)  
        rand_depth_y = random.uniform(1.0, 3.5)  
        rand_height  = random.uniform(2.0, 15.0) 

        obj.scale[0] = rand_width_x
        obj.scale[1] = rand_depth_y
        

        mat = bpy.data.materials.new(name="RandColor")
        mat.diffuse_color = (random.random(), random.random(), random.random(), 1)
        obj.data.materials.append(mat)
        
        obj.scale[2] = 0
        obj.keyframe_insert(data_path="scale", frame=1)

        obj.scale[2] = rand_height
        obj.keyframe_insert(data_path="scale", frame=60)