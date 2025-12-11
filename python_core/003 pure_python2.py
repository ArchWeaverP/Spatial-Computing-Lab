cart = ["apple"]
balance = 0

if len(cart) == 0:
    print("Cart is empty")
elif balance < 3000: #elif = else if
    print("Inssufficient balance")
else:
    print("Payment complete! 3,000 won will be deducted")
    cart = []
    balance = balance - 3000


#remove & pop

cart = ["apple", "banana", "apple", "milk"]
cart.remove("banana") #delete banana
print(cart) # apple, apple, milk

cart = ["apple", "banana", "milk"]
removed_item = cart.pop(1)

print(removed_item) # banana
print(cart) # apple, milk

#for loop
# for item in sequence
# item을 가지고 할 작업

prices = [5000, 1200, 3000]
total = 0

for price in prices:
    total = total + price
    # 1. price = 5000, total = 0 + 5000 = 5000
    # 2. price = 1200, total = 5000 + 1200 = 6200
    # 3. price = 3000, total = 6200 + 3000 = 9200
    # 4. loop ends
    # 리스트의 요소들을 하나씩 꺼내서 반복하고 끝나면 종료함.

print("total:", total) #9200


item_prices = [500, 800, 300, 1000, 300]
total_price = 0

for item_price in item_prices:
    total_price = total_price + item_price

item_prices.remove(300)

print("total:", total_price)
print("list", item_prices)


#for + if

item_prices = [500, 800, 300, 1000, 300]
total_price = 0

for item_price in item_prices:
    if item_price > 500:
        total_price = total_price + item_price
print(total_price)