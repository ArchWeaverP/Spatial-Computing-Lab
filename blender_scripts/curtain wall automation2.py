import bpy

# ==========================================
# 1. Setup & Functions (설정 및 도구 준비)
# ==========================================

# Settings
floor_count = 10
room_count = 6
module_size = 3
asset_names = {
    "window": "window_3x3",
    "door": "door_3x3",
    "parapet": "parapet_0.5"
}

# Helper Function: Get or Create Collection
def get_collection(name):
    if name not in bpy.data.collections:
        new_col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(new_col)
    return bpy.data.collections[name]

# Helper Function: Clear Collection (The "Cleaner")
def clear_collection(col):
    for obj in col.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

# ==========================================
# 2. Preparation (현장 정리)
# ==========================================

# Define Collections
# 'Original_Assets': Where source models live (Safe zone)
# 'Generated_Building': Where new building goes (Construction zone)
asset_col = get_collection("Original_Assets")
build_col = get_collection("Generated_Building")

# Clean the construction site ONLY (Prevent Overlapping)
clear_collection(build_col)

# Get Source Objects safely
assets = {}
missing_assets = []

for key, name in asset_names.items():
    obj = bpy.data.objects.get(name)
    if obj:
        assets[key] = obj
        # Move source to asset collection if needed
        if obj.name not in asset_col.objects:
            # Unlink from other collections first to avoid duplication
            for c in obj.users_collection:
                c.objects.unlink(obj)
            asset_col.objects.link(obj)
    else:
        missing_assets.append(name)

# Hide originals from viewport
bpy.context.view_layer.layer_collection.children['Original_Assets'].hide_viewport = True

# ==========================================
# 3. Construction (시공 시작)
# ==========================================

if missing_assets:
    print(f"Error: Missing assets {missing_assets}")
else:
    print("Start Construction...")

    for floor in range(floor_count):
        for room in range(room_count):
            
            # --- Logic: Select Asset Type ---
            target_obj = None
            
            if floor == 0:
                target_obj = assets["door"]
            elif floor == floor_count - 1:
                target_obj = assets["parapet"]
            else:
                target_obj = assets["window"]
            
            # --- Logic: Create Instance ---
            new_obj = target_obj.copy()
            
            # [Special Case] Independent Object (Deep Copy)
            # Example: 5th Floor (index 4), 3rd Room (index 2)
            if floor == 4 and room == 2:
                # Duplicate Data (Mesh) for independence
                new_obj.data = target_obj.data.copy()
                new_obj.name = f"Window_Special_{floor+1}F_{room+1}"
                print(f"Special window created at {floor+1}F - {room+1}")
            else:
                # Linked Duplicate (Shared Data) for efficiency
                new_obj.name = f"{target_obj.name.split('_')[0]}_{floor+1}F_{room+1}"
            
            # --- Placement ---
            # Link to the construction collection
            build_col.objects.link(new_obj)
            
            # Set Location
            new_obj.location = (room * module_size, 0, floor * module_size)

    print("Construction Complete!")