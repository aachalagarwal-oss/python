wallets={}
def add_user(id,name):
    if id in wallets:
        print("User id exist")
    else:
        wallets[id]={
            "name":name,
            "balance":0
        }
        print("User created")


def add_balance(id,amount):
    if id not in wallets:
        print("User doesn't exist")
    elif amount<0:
        print("Insufficient balance to add")
    else:
        wallets[id]["balance"]+=amount
        print("Balance entered")

def remove_balance(id,amount):
    if id not in wallets:
        print("User doesn't exist")
    elif amount<0:
        print("Insufficient balance to remove")
    elif(wallets[id]["balance"]<amount):
        print("insufficient balance")
    else:
        wallets[id]["balance"]-=amount
        print("Balance removed")

def remove_user(id):
    if id not in wallets:
        print("User doesn't exist")

    else:
        del wallets[id]
        print("User deleted")

def show_balance(id):
    if id not in wallets:
        print("User doesn't exist")
    else:
        print(f"Balance is",wallets[id]["balance"])



while(True):
    number=input("Choose 1 for adding user, 2 for adding balance, 3 for removing balance, 4 for showing balance,5 for removing user,6 for exit")

    match number:
        case "1":
            id=input("Enter the id")
            name=input("Enter the name")
            add_user(id,name)

        case "2":
            id=input("Enter the id")
            amount=int (input("Enter the amount"))
            add_balance(id,amount)

        case "3":
            id=input("Enter the id")
            amount=int (input("Enter the amount"))
            remove_balance(id,amount)

        case "4":
            id=input("Enter the id")
            show_balance(id)

        case "5":
            id=input("Enter the id")
            remove_user(id)
                

        case "6":
            print('Exit done')
            break



        
