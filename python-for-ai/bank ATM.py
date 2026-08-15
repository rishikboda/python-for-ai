balance = 10000
pin = 1234
name = "rishik"
while True:
    print('"1" : to check the balance')
    print('"2" : to deposit')
    print('"3" : to withdrawl')
    print('"4" : to exit')
    choice = int(input("enter the choice"))

    if choice == 1:
        account_no = int(input("enter the account number"))
        user_pin = int(input("enter your pin number"))

        if pin == user_pin:
            print(f"your avaliable balance = {balance} of account number {account_no}")
            print(f"account holder name = {name}")
        else:
            print("invaild pin please enter the correct pin")
    elif choice == 2:
        if pin == user_pin:
            account_no = int(input("enter the account number"))
            user_pin = int(input("enter your pin number"))

            amount = int(input("enter the amount you want to deposite"))
            balance += amount
            print(
                f"available balance after deposite = {balance} in your account number {account_no}"
            )
            print(f"account holder name = {name}")
        else:
            print("invaild pin please enter the correct pin")

    elif choice == 3:
        if pin == user_pin:
            account_no = int(input("enter the account number"))
            user_pin = int(input("enter your pin number"))

            amount = int(input("enter the amount you want to withdrawl"))
            if amount <= balance:
                balance -= amount
                print(
                    f"your balance after withdrawl = {balance} in your account number{account_no}"
                )
                print(f"account holder name {name}")
            else:
                print("insufficient balance")
        else:
            print("invaild pin please enter the correct pin")

    elif choice == 4:
        print("thanks for banking with us")
        break
    else:
        print("please enter the valid number")
