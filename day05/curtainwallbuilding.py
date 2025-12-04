import bpy
import random
import math

# ==========================================
# 1. Setup & Functions (설정)
# ==========================================

floor_count = 12           # 층수
width_count = 6            # 가로(X) 모듈 개수
depth_count = 4            # 세로(Y) 모듈 개수
module_size = 3            # 모듈 크기 (3m)
open_probability = 0.15    # 창문 열림 확률

asset_names = {
    "window": "window_3x3",
    "open_window": "win_open",
    "door": "door_3x3",
    "parapet": "parapet_0.5"
}

def get_collection(name):
    if name not in bpy.data.collections:
        new_col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(new_col)
    return bpy.data.collections[name]

def clear_collection(col):
    for obj in col.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
        
def create_asphalt_material(name):
    # 1. 이미 있으면 그거 씀
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    
    # 2. 새 재질 만들기 & 노드 사용 켜기 (중요!)
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # 3. 기존 노드 가져오기 (Principled BSDF)
    # 블렌더가 기본으로 만들어주는 '만능 재질 노드'입니다.
    bsdf = nodes.get("Principled BSDF")
    
    # --- 아스팔트 레시피 ---
    
    # (1) 색상: 진한 회색
    bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1)
    
    # (2) 거칠기: 빛 반사를 줄여서 매트하게 (0=거울, 1=고무)
    bsdf.inputs['Roughness'].default_value = 0.9 
    
    # (3) 노이즈 텍스처 (자글자글한 무늬 만들기)
    tex_noise = nodes.new('ShaderNodeTexNoise')
    tex_noise.inputs['Scale'].default_value = 100.0  # 알갱이 크기 (클수록 작아짐)
    tex_noise.inputs['Detail'].default_value = 15.0  # 디테일하게
    
    # (4) 범프 노드 (무늬를 울퉁불퉁하게 만들기)
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.4      # 튀어나온 정도
    
    # 4. 노드 연결하기 (전선 연결)
    # 노이즈(Factor) -> 범프(Height) -> BSDF(Normal)
    links.new(tex_noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    return mat

# ==========================================
# 2. Preparation (현장 정리)
# ==========================================

asset_col = get_collection("Original_Assets")
build_col = get_collection("Generated_Building")

clear_collection(build_col)

# 에셋 로딩 및 정리
assets = {}
missing_list = []

for key, name in asset_names.items():
    obj = bpy.data.objects.get(name)
    if obj:
        assets[key] = obj
        if obj.name not in asset_col.objects:
            for c in obj.users_collection:
                c.objects.unlink(obj)
            asset_col.objects.link(obj)
        obj.hide_render = True 
    else:
        missing_list.append(name)

bpy.context.view_layer.layer_collection.children['Original_Assets'].hide_viewport = True

# ==========================================
# 3. Construction Logic (3D 시공)
# ==========================================

if missing_list:
    print(f"Error: Missing assets {missing_list}")
else:
    print("Start 3D Construction...")

    # 건물 전체 크기 계산
    total_width = width_count * module_size
    total_depth = depth_count * module_size

    # --- [Step 1] 4면 벽체 세우기 (Wall) ---
    for side in range(4):
        # 0:남(Front), 1:동(Right), 2:북(Back), 3:서(Left)
        if side % 2 == 0:
            current_room_count = width_count
        else:
            current_room_count = depth_count

        rotation_angle = side * (math.pi / 2)

        for floor in range(floor_count):
            for room in range(current_room_count):
                
                # 자재 선정
                target_obj = None
                if floor == 0:
                    # 앞면(Side 0)의 중앙에만 문 배치
                    if side == 0 and room == int(current_room_count / 2):
                        target_obj = assets["door"]
                    else:
                        target_obj = assets["window"]
                elif floor == floor_count - 1:
                    target_obj = assets["parapet"]
                else:
                    if random.random() < open_probability:
                        target_obj = assets["open_window"]
                    else:
                        target_obj = assets["window"]

                # 배치
                new_obj = target_obj.copy()
                new_obj.hide_render = False 
                build_col.objects.link(new_obj)

                # 로컬 좌표 (회전 전)
                local_x = room * module_size
                local_z = floor * module_size
                
                # 회전 적용
                new_obj.rotation_euler[2] = rotation_angle
                
                # 월드 좌표 변환 (4면 배치)
                if side == 0:   # Front
                    new_obj.location = (local_x, 0, local_z)
                elif side == 1: # Right
                    new_obj.location = (total_width, local_x, local_z)
                elif side == 2: # Back
                    new_obj.location = (total_width - local_x, total_depth, local_z)
                elif side == 3: # Left
                    new_obj.location = (0, total_depth - local_x, local_z)
                
                new_obj.name = f"Wall{side}_{floor+1}F_{room+1}"


    # --- [Step 2] 층간 슬라브 깔기 (Slabs) ---
    # 각 층마다 얇은 바닥판을 깔아서 내부를 구획합니다.
    
    # 슬라브용 재질 만들기 (진한 회색)
    if "Slab_Mat" not in bpy.data.materials:
        mat_slab = bpy.data.materials.new("Slab_Mat")
        mat_slab.diffuse_color = (0.2, 0.2, 0.2, 1) # Dark Grey

    # 지붕까지 포함해야 하니까 floor_count + 1 번 반복
    for floor in range(floor_count):
        # 1. 큐브(슬라브) 생성 (크기 1m짜리)
        bpy.ops.mesh.primitive_cube_add(size=1)
        slab = bpy.context.object
        slab.name = f"Slab_{floor}F"
        
        # 2. 컬렉션 정리 (기본 컬렉션에서 빼고 우리 현장에 넣기)
        bpy.context.collection.objects.unlink(slab)
        build_col.objects.link(slab)
        
        # 3. 크기 맞추기 (건물 전체 크기)
        slab.scale.x = total_width
        slab.scale.y = total_depth
        slab.scale.z = 0.3  # 두께 30cm
        
        # 4. 위치 잡기 (건물 중앙)
        # 큐브 중심이 가운데라 width/2, depth/2 만큼 이동해줘야 함
        slab.location.x = total_width / 2
        slab.location.y = total_depth / 2
        slab.location.z = floor * module_size # 층 높이에 맞춰 배치
        
        # 5. 재질 적용
        slab.data.materials.append(bpy.data.materials["Slab_Mat"])
        
    
    # --- [Step 3] 대지 만들기 (Ground/Site) ---
    # 건물 밑에 아주 큰 바닥판을 깝니다.
    
    bpy.ops.mesh.primitive_plane_add(size=500) # 200m 크기
    ground = bpy.context.object
    ground.name = "Site_Ground"
    
    # 컬렉션 정리
    bpy.context.collection.objects.unlink(ground)
    build_col.objects.link(ground)
    
    # 위치 살짝 내리기 (1층 바닥이랑 겹치지 않게)
    ground.location.x = total_width / 2
    ground.location.y = total_depth / 2
    ground.location.z = -0.1
    
    # 대지 재질 (아스팔트 느낌)
    # 아스팔트 함수를 호출해서 재질을 가져옵니다.
    asphalt_mat = create_asphalt_material("Asphalt_Road")
    ground.data.materials.append(asphalt_mat)