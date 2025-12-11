# pure python and CS basic 학습

a = 10
b = a

print(id(a))
print(id(b))

# a 와 b 의 reference 는 동일하게 출력됨. (id 는 주소값을 묻는 연산자)
# 10이라는 객체에 a라는 이름표가 붙어있던 상황에서 b라는 이름표도 추가된 것.
# 이 경우 reference count 는 2가 됨

a = 10
b = a
print(a is b) #결과값은 True

b = 20
print(a is b) #결과값은 False

#print 는 출력을 명령, is 는 == 가 아닌 매모리 주소가 같은지 물어보는 연산자

# Stack : 변수 이름 (a,b), 주소값이 저장됨
# Heap : 실제 데이터 객체(10,20)가 저장됨


#가변과 불변
#b = a 참조 복사, 공유문서라고 생각하면 이해하기 쉬움 원본 영향 있음
#b = a[:] 값 복사, 파일 복사라고 생각하면 이해하기 쉬움 원본 영향 없음
#ex
orig_data = [100, 200, 300]
temp_data = orig_data #이 경우 참조 복사가 되기 때문에 원본에 영향을 줌
#임시 데이터가 아닌 원본 데이터도 함께 수정이 됨
del temp_data[0] #임시 데이터에서 첫 번째 값을 지움

print(temp_data) #원하는 결과 출력됨
print(orig_data) #원본 데이터는 지워지면 안되는데 임시데이터와 함께 지워짐

orig_data = [100, 200, 300]
temp_data = orig_data[:] #[:] 슬라이싱 : 복사본만 수정하는 방법, 새로운 메모리 할당
#[:]를 사용하면 heap 영역에 똑같은 값을 가진 새로운 리스트 객체 생성하여 원본과 분리 시킴
del temp_data[0]

print(temp_data) #원하는 결과 출력됨
print(orig_data) #원본 데이터 유지

#immutabel(불변) : 정수(int), 실수(float), 문자열(str), 튜플(tuple). 내용물 변경 불가 (바꾸려면 새 객체 생성)\
#값이 변하지 않음, 예기치 않은 변경으로 인한 버그가 적어 안전
#변경하고 싶다면 새롭게 덮어씌워야 함

#mutable(가변) : 리스트(list), 딕셔너리(dict), 집합(set). 메모리 주소 변경 없이 내부 데이터 수정 가능 (참조 공유시 주의 필요)
#데이터를 유연하게 관리, 여러 곳에서 동시 참조 시 값이 바뀌면 혼란을 초래할 수 있음

#즉 불변과 가변은 데이터가 생성된 후에 그 값을 바꿀 수 있는지에 따라 달라짐



#true false (boolean logic)
#기본 and, or, not
#and (논리곱) : 둘 다 참인 경우 참 true and true → true / true and false → false
#or (논리합) : 둘 중 하나만 참인 경우도 참 true or false → true / false and false → false
#not (부정) : 반대로 뒤집은 것, not true → false
#응용 nand, nor, xor, xnor
#nand (not and) : and 의 반대, 둘 다 참인 경우만 아니면 됨 not (A and B) 시스템 안전장치 (두 개의 위험 스위치가 동시에 눌리면 작동 중지)
#nor (not or) : or의 반대, 둘 다 아니어야 함 not (a or b) 주말도 아니고 공휴일도 아니어야 출근한다
#xor (exclusive or) : 서로 다를 때만 참 (배타적 논리합) 기호 : ^ 혹은 !=(다르다)
#xnor (exclusive nor) : xor의 반대, 서로 같을 때만 참 기호 : ==(같다)


#파이썬은 들여쓰기(tap 혹은 space 4칸)로 구역을 나눔, 코드의 구역을 묶음
#파이썬은 비어있거나 없는것을 거짓으로 봄

cart = [] #카트는 빈 리스트(카트를 비우라는 명령), 내용물이 없는 상태로 false 취급
#0, "", [], none 은 false 취급
if cart:
    print("결제하시겠습니까?")
else:
    print("장바구니가 비어있습니다.")


cart = ["사과", "과자", "우유"]
if len(cart) > 0:
    print("결제완료")
    cart = []
else:
    print("장바구니가 비어있음")

print("현재 장바구니 상태:", cart)



cart = []
cart.append("커피")
cart.append("빵")

print(cart) #커피, 빵 출력됨



cart = [] # 빈 장바구니
balance = 5000 #잔액

cart.append("사과") # 사과를 담음
cart.append("과자") # 과자를 담음

if len(cart) > 0 and balance >= 3000: # 개수가 2개(사과, 과자) 2>0 true, 잔액이 3000 이상이므로 true, and조건에 맞춰 둘 다 참이므로 참
    print("결제완료") #참이니까 실행
    cart = [] #장바구니 비움
    balance = balance - 3000 #잔액 - 3000
else: #참이 아닌경우에 적용, 현재 상황에선 참이므로 건너 뜀
    print("장바구니가 비어있거나 잔액이 부족합니다.")
print("남은 잔액:", balance)
print("현재 장바구니 상태:", cart)

