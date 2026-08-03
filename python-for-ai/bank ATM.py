balance = 10000
while True:
    print("\"1\" : to check the balance")
    print("\"2\" : to deposit")
    print("\"3\" : to withdrawl")
    print("\"4\" : to exit")
    choice = int(input("enter the choice"))
    

    
    if choice==1:
        print(f"your avaliable balance{balance}")
    elif choice==2:
        amount= int(input("enter the amount you want to deposite"))
        balance +=amount
        print(f"available balance after deposite = {balance}")
    elif choice==3:
        amount = int(input("enter the amount you want to withdrawl"))
        if amount<=balance:
            balance -=amount
            print(f"your balance after withdrawl = {balance}")
        else:
            print("insufficient balance")
    elif choice==4:
        print("thanks for banking with us")
        break
    else:
        print("please enter the valid number")