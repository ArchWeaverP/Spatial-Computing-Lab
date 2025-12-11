# 가상의 카페 매출 계산하기 if문 연습
cafe_name = "Coffee house"
coffee_price = 3000
daily_sales = 100

total_income = coffee_price * daily_sales

print(f"{cafe_name} 카페의 오늘 매출은 {total_income:,}원입니다.")

if total_income >= 500000:
    print("흑자입니다! 잘하고 있어요.")
else:
    print("적자 위기입니다. 마케팅이 필요해요.")


#for문 연습
for floor in range(1, 11):
    if floor == 4:
        print(f"{floor}층: [경고]철근 누락 의심! 정밀 점검 필요!")
    else:
        print(f"{floor}층: 안전 점검 이상 무")


#def문 연습
def say_hello():
    print("안녕하세요! 설계팀입니다.")
    print("오늘도 안전 작업 합시다.")

say_hello()

def calculate_area(width, depth):
    area = width * depth
    print(f"면적은{area:,}입니다.")
calculate_area(100, 200)
calculate_area(5, 5)

def check_safety(floor):
    if floor == 4:
        print(f"[긴급] {floor}층에서 결합이 발견되었습니다!")
    else:
        print(f"{floor}층: 이상 없습니다.")

check_safety(1) #1층 점검
check_safety(4) #4층 점검


print("=== 20층 건물 안전 점검을 시작합니다 ===")
for i in range(1, 21):
    check_safety(i)

print("=== 점검 완료 ===")