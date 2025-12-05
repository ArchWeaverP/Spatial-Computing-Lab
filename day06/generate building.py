import bpy
import random
import math

# ==========================================
# 1. 설정 (Setup)
# ==========================================

floor_count = 12
width_count = 6
depth_count = 4
module_size = 3
open_probability = 0.15

# 🎬 공정 속도
slab_duration = 5
wall_duration = 10
gap_time = 2

asset_names = {
    "window": "window_3x3",
    "open_window": "win_open",
    "door": "door_3x3",
    "parapet": "parapet_0.5"
}

# --- 도구 함수 ---
def get_collection(name):
    if name not in bpy.data.collections:
        new_col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(new_col)
    return bpy.data.collections[name]

def create_material(name, color):
    if name in bpy.data.materials: return bpy.data.materials[name]
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = color
    return mat

# ==========================================
# 2. 현장 정리
# ==========================================

# 기존 핸들러가 있다면 삭제 (충돌 방지)
if "construction_handler" in bpy.app.handlers.frame_change_post:
    bpy.app.handlers.frame_change_post.clear()

total_frames = floor_count * (slab_duration + wall_duration + gap_time) + 50
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = total_frames
bpy.context.scene.frame_current = 1

# 객체 삭제
objs_to_remove = []
for obj in bpy.data.objects:
    if obj.name.startswith(("Slab_", "Wall_", "Site_Ground")):
        objs_to_remove.append(obj)
for obj in objs_to_remove:
    bpy.data.objects.remove(obj, do_unlink=True)

# 컬렉션 설정
asset_col = get_collection("Original_Assets")
build_col = get_collection("Generated_Building")

# 에셋 로딩
assets = {}
missing = []
for key, name in asset_names.items():
    obj = bpy.data.objects.get(name)
    if obj:
        assets[key] = obj
        if obj.name not in asset_col.objects:
            for c in obj.users_collection: c.objects.unlink(obj)
            asset_col.objects.link(obj)
        obj.hide_render = True
    else:
        missing.append(name)
        
bpy.context.view_layer.layer_collection.children['Original_Assets'].hide_viewport = True

# ==========================================
# 3. 시공 시작 (키프레임 방식)
# ==========================================

if missing:
    print(f"Error: Missing {missing}")
else:
    print("Start Construction...")
    
    total_width = width_count * module_size
    total_depth = depth_count * module_size
    
    current_frame = 1
    
    for floor in range(floor_count):
        
        # ----------------------------------------
        # [Step 1] 슬라브 (Slab)
        # ----------------------------------------
        
        bpy.ops.mesh.primitive_cube_add(size=1)
        slab = bpy.context.object
        slab.name = f"Slab_{floor+1}F"
        
        for c in slab.users_collection: c.objects.unlink(slab)
        build_col.objects.link(slab)
        
        # 위치 잡기
        slab.location.x = total_width / 2
        slab.location.y = total_depth / 2
        slab.location.z = floor * module_size 
        
        slab.data.materials.append(create_material("Slab_Mat", (0.2, 0.2, 0.2, 1)))
        
        # ★ [절대 실패 없는 키프레임 로직] ★
        
        # 1. 일단 무조건 0으로 만듭니다. (숨기기)
        slab.scale = (0, 0, 0)
        
        # 2. '1프레임'에 도장을 쾅! 찍습니다. 
        # (너는 태초부터 0이었던 거야)
        slab.keyframe_insert(data_path="scale", frame=1)
        
        # 3. '시작 시간'까지도 0을 유지합니다.
        slab.keyframe_insert(data_path="scale", frame=current_frame)
        
        # 4. '끝나는 시간'에 비로소 커집니다.
        slab.scale = (total_width, total_depth, 0.3) # 목표 크기 입력
        slab.keyframe_insert(data_path="scale", frame=current_frame + slab_duration)
        
        current_frame += slab_duration
        
        
        # ----------------------------------------
        # [Step 2] 벽체 (Wall)
        # ----------------------------------------
        
        for side in range(4):
            if side % 2 == 0: room_cnt = width_count
            else: room_cnt = depth_count
            rot_angle = side * (math.pi / 2)
            
            for room in range(room_cnt):
                target = None
                if floor == 0:
                    if side == 0 and room == int(room_cnt/2): target = assets["door"]
                    else: target = assets["window"]
                elif floor == floor_count - 1:
                    target = assets["parapet"]
                else:
                    target = assets["open_window"] if random.random() < open_probability else assets["window"]
                
                new_obj = target.copy()
                new_obj.hide_render = False
                build_col.objects.link(new_obj)
                
                local_x = room * module_size
                local_z = floor * module_size
                new_obj.rotation_euler[2] = rot_angle
                
                if side == 0: new_obj.location = (local_x, 0, local_z)
                elif side == 1: new_obj.location = (total_width, local_x, local_z)
                elif side == 2: new_obj.location = (total_width - local_x, total_depth, local_z)
                elif side == 3: new_obj.location = (0, total_depth - local_x, local_z)
                
                new_obj.name = f"Wall_{floor+1}F_{side}_{room}"
                
                # ★ 벽체도 똑같이! 
                new_obj.scale = (0, 0, 0) # 1. 0으로 만듦
                new_obj.keyframe_insert(data_path="scale", frame=1) # 2. 1프레임 고정
                new_obj.keyframe_insert(data_path="scale", frame=current_frame) # 3. 대기
                
                new_obj.scale = (1, 1, 1) # 4. 커짐
                new_obj.keyframe_insert(data_path="scale", frame=current_frame + wall_duration)

        current_frame += wall_duration
        
    
    # [Step 3] 대지
    bpy.ops.mesh.primitive_plane_add(size=200)
    ground = bpy.context.object
    ground.name = "Site_Ground"
    for c in ground.users_collection: c.objects.unlink(ground)
    build_col.objects.link(ground)
    ground.location = (total_width/2, total_depth/2, -0.1)
    ground.data.materials.append(create_material("Asphalt", (0.05, 0.05, 0.05, 1)))

    # 실행 후 1프레임으로 강제 이동
    bpy.context.scene.frame_set(1)
    print("Done! Press Space to play.")