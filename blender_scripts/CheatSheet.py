import bpy
import random
import math

# --- 1. 기본 조작 (생성 & 변형) ---
bpy.ops.mesh.primitive_cube_add(size=1)  # 큐브 소환
obj = bpy.context.object                 # 방금 만든 놈 잡기

obj.location = (10, 0, 5)                # 위치 이동 (X, Y, Z)
obj.rotation_euler = (0, 0, math.radians(90)) # 회전 (라디안 사용!)
obj.scale = (2, 2, 0.5)                  # 크기 변형

# --- 2. 데이터 관리 (복제 & 정리) ---
target = bpy.data.objects.get("MyAsset") # 에셋 찾기
new_obj = target.copy()                  # 껍데기 복사 (가벼움, 수정시 같이 바뀜)
new_obj.data = target.data.copy()        # 알맹이까지 독립 복사 (무거움, 따로 놂)

# 컬렉션(폴더) 다루기
my_col = bpy.data.collections.new("My_Collection") # 새 폴더 만들기
bpy.context.scene.collection.children.link(my_col) # 씬에 등록하기
my_col.objects.link(new_obj)             # 폴더에 물건 넣기

# --- 3. 재질 (Material) ---
mat = bpy.data.materials.new(name="Red_Mat") # 재질 만들기
mat.use_nodes = True                         # 노드 사용 켜기
bsdf = mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (1, 0, 0, 1) # RGBA (빨강)
obj.data.materials.append(mat)               # 물체에 입히기

# --- 4. 애니메이션 (Time) ---
# 방법 A: 키프레임 (도장 찍기)
obj.scale = (0, 0, 0)
obj.keyframe_insert(data_path="scale", frame=1) # 1프레임에 '0' 기록

# 방법 B: 핸들러 (실시간 조종)
def my_handler(scene):
    current = scene.frame_current
    # 매 프레임마다 실행될 로직...
bpy.app.handlers.frame_change_post.append(my_handler) # 등록
bpy.app.handlers.frame_change_post.clear()            # 삭제 (초기화)