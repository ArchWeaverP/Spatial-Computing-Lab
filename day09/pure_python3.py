#Function (함수)
#입력을 받아서 특정 작업을 수행하고 결과를 돌려주는 것 (input, output)
#def (define, 정의하다)

#def 함수이름(재료):
    # 할 일 (본문)
    # return 결과물

#건축 면적 계산기
def calculate_area(width, height): #함수를 정의함 calcuate_area 함수에 (width, height) 를 입력하면 area = width * height 라는 명령을 통해서 area 라는 결과값을 도출해냄, 즉 calculate_area(width, height)라는 함수로 area를 구할 수 있음
    area = width * height
    return area
room1 = calculate_area(3, 4)
room2 = calculate_area(5, 5)

print("Room 1 area:", room1)
print("Room 2 area:", room2)
#함수의 효율성 : 함수가 실행될 때만 메모리를 사용하고 삭제하기 때문에 효율적임
#1.Main 실행 : 프로그램이 시작되면 Main 이라는 작업공간(프레임) 생성
#2.함수 호출 : 원래 하던 일을 멈추고 Main 위에 Stack Frame 을 생성, 이름은 함수의 이름
#3.작업 수행 : 이 Stack Frame 에서 변수를 생성(함수에 포함된 변수)
#4.return(복귀) : 함수가 끝나고 return 이 실행되면 결과값만 main 에 반영, 함수로 사용된 Stack Frame 파괴됨(pop)
#5.Main 복귀 : 원래 하던 일 시작

#### 중요! 따라서 함수 안에서 만든 변수는 함수가 끝나면 컴퓨터가 읽지 못 함, Stack Frame 안의 변수이기 때문, 함수가 끝나면 Stack Frame 도 사라짐




def get_total_price(price, tax_rate):
    total_price = price * tax_rate
    return total_price

brick_price = 1000
brick_tax = 1.3
total = get_total_price(brick_price, brick_tax)

print("벽돌의 최종 가격:", total)



def get_total_price(price, tax_rate=1.1): #tax_rate 를 입력하지않으면 자동으로 1.1 로 처리, 즉 기본값을 입력함
    return price * tax_rate

print(get_total_price(1000))
print(get_total_price(1000, 1.2))


def get_delivery_fee(distance=0):
    return 3000 + distance

print(get_delivery_fee())
print(get_delivery_fee(1000)) #뭔가 어설퍼서 수정 필요, 거리와 돈은 단위가 다름

def get_delivery_fee(distance_km=0):
    base_fee = 3000 #기본요금
    cost_per_km = 500 #1km 당 추가요금
    #총 배송비는 기본요금 + (거리*단가)
    total_fee = base_fee + (distance_km * cost_per_km) #total_fee 대신 바로 return = base_fee + (distance_km * cost_per_km) 로 해도 됨
    return total_fee

print(get_delivery_fee()) #기본 배송 (1km 이내)
print(get_delivery_fee(5)) #5km 거리 배송 (1km 이상의 거리)


print("함수 조립하기")

def get_item_price(price, tax_rate=1.1):
    return price * tax_rate

def get_delivery_fee(distance_km=0):
    base_fee = 3000
    cost_per_km = 500
    return base_fee + (distance_km * cost_per_km)

brick_price = 1000
distance = 10

total_price = get_item_price(brick_price) + get_delivery_fee(distance)

print(total_price)