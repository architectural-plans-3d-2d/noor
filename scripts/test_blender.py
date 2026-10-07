import bpy
bpy.ops.wm.obj_import(filepath='models/daata_hamlet.obj')
print('Object names in Blender:', [o.name for o in bpy.data.objects])
