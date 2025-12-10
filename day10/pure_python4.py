#if / else

def get_delivery_fee(distance_km=0):
    if distance_km > 30:
        print("배송 불가 지역입니다.")
        return 0
    else: #함수 추가할 필요 없음. 이미 함수 안에 있음. 변수로 계산
        base_fee = 3000
        cost_per_km = 500
        return base_fee + (distance_km * cost_per_km)
    
print(get_delivery_fee(10))
print(get_delivery_fee(40))


#else 를 사용하지 않는 방법 (선호함)
#early return

def get_delivery_fee(distance_km=0):
    #만약 30km를 초과하면 배송 불가능 (예외 상황/거절해야할 상황) 먼저 처리해서 돌려보냄
    if distance_km > 30:
        print("배송 불가 지역입니다.")
        return 0 #여기서 30km 초과하는 곳은 배송불가지역으로 출력되어 결과값 끝
        #즉, 이방식에서는 굳이 else를 적을 필요가 없음
        #예외인 상황을 먼저 처리했기 때문에 이 예외가 아니라면 배송가능한 조건이라는 뜻
    #배송가능 (else를 적어봤자 같은의미, 그렇다면 글자를 줄이는것으로 효율적으로 코드 짜기)
    base_fee = 3000
    cost_per_km = 500
    return base_fee + (distance_km * cost_per_km)
    
print(get_delivery_fee(10))
print(get_delivery_fee(40))


def get_item_price (price, tax=1.1):
    return price * tax

def get_delivery_fee(distance_km=0):
    if distance_km > 30:
        print("배송 불가 지역입니다.")
        return 0
    base_fee = 3000
    cost_per_km = 500
    return base_fee + (distance_km * cost_per_km)

apple = 3000
distance = 60

delivery_fee = get_delivery_fee(distance)

if delivery_fee == 0:
    print("주문을 진행할 수 없습니다.")
else:
    total_price = get_item_price(apple) + get_delivery_fee(distance)
    print("총 결제금액:", total_price)
