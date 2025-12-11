import bpy
asset_name = "window_3x3"
floor_count = 10
room_count = 5
module_width = 3
module_height = 3

source_asset = bpy.data.objects.get(asset_name)

if source_asset is None:
    print(f"error '{asset_name} is disapeared.")
else:
    print(f"{asset_name} is found.")
    
    for floor in range(floor_count):
        for room in range(room_count):
            new_window = source_asset.copy()
            bpy.context.collection.objects.link(new_window)
    
            x_pos = room * module_width
            z_pos = floor * module_height
            
            new_window.location = (x_pos, 0, z_pos)
            
            new_window.name = f"window_{floor+1}F_{room+1}"
            
    print(f"total {floor_count * room_count} windows are completed")
    
    
