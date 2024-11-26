import bpy
import os
import math

Z_ROTATION_OFFSET=-135
CLOCKWISE=True
FACINGS=8
RENDER_WIDTH=120
RENDER_HEIGHT=120
ACTION_LIST = [
    'stand',
    'walk',
    'attack',
]
OUTPUT_DIR = "c:\\tmp\\firdge-x4"

def render_sprites():
    dest_dir = os.path.join(os.path.abspath(OUTPUT_DIR), "v2-1")
    normal_dir = os.path.join(os.path.abspath(OUTPUT_DIR), "v2_normal")
    
    s=bpy.context.scene

    s.render.resolution_x = RENDER_WIDTH
    s.render.resolution_y = RENDER_HEIGHT
    
    index = 0
    
    for _name in ACTION_LIST:
        if _name in bpy.data.actions:
            a = bpy.data.actions.get(_name)
            
            #assign the action
            bpy.context.active_object.animation_data.action = bpy.data.actions.get(a.name)
            
            #dynamically set the last frame to render based on action
            s.frame_end = int(bpy.context.active_object.animation_data.action.frame_range[1])
            
            original_z_rotation = bpy.context.active_object.rotation_euler[2] # backup the z rotate
            angle_step = -360 / FACINGS if CLOCKWISE else 360 / FACINGS
            for i in range(FACINGS):
                angle = i * angle_step + Z_ROTATION_OFFSET
                    
                bpy.context.active_object.rotation_euler[2] = math.radians(angle)
                
                for r in range(s.frame_start, s.frame_end+1):
                    
                    s.frame_current = r
                    s.render.filepath = os.path.join(dest_dir, "obj %04d.png" % (index))
                                      
                    bpy.ops.render.render( #{'dict': "override"},
                          #'INVOKE_DEFAULT',  
                          False,            # undo support
                          animation=False, 
                          write_still=True
                    )
                    index = index + 1
                     
                bpy.context.active_object.rotation_euler[2] = original_z_rotation # restore the z rotate
            
render_sprites()
