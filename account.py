ADD_TO_ACCOUNT = 1
WITHDRAWN_MONEY = 2
ACCOUNT_STATEMENT = 3
EXIT_APP = 4

balance = 0.0
limit = 500.0
transactions = " "
WITHDRAW_LIMITS = 3


def options():
    print()
    print("=====Bank System=====\n")
    print(f"{[ADD_TO_ACCOUNT]} Make a deposit")
    print(f"{[WITHDRAWN_MONEY]} Cash out")
    print(f"{[ACCOUNT_STATEMENT]} Account Statement")
    print(f"{[EXIT_APP]} Exit")
    return int(input('\nChoose a option: '))
print()


def add_to_account():
    global balance
    global limit
    global transactions

    value = float(input("\nType the value to add in the account: $"))

    if value >= 0:
        if limit < 500:
            additional_limit = min(500 - limit, value)
            limit += additional_limit
            balance += (value - additional_limit) 
            transactions += f"\nDeposited: ${value:.2f}"
            print(f"\nValue: ${value:.2f} successfully added.")
        else:
            balance += value
            transactions += f"\nDeposited: ${value:.2f}"
            print(f"\nValue: ${value:.2f} successfully added.")
    else:
        print('\nThe value must be at least 1 dollar')


def withdrawn_money():
    global balance
    global limit
    global transactions
    global WITHDRAW_LIMITS 

    value = float(input("\nType the value withdraw: $"))

    if WITHDRAW_LIMITS == 0:
        print('\nTransitions limit made')
        return

    
    if value <= balance:
        balance -= value
        WITHDRAW_LIMITS -= 1
        transactions += f"\nWithdrawn: ${value:.2f}"
        print(f"\nValue: ${value:.2f} withdraw.")
    elif (value <=  limit + balance) and (limit > 0):
        limit_used = (value - balance)
        limit -= limit_used
        balance = 0
        WITHDRAW_LIMITS -= 1
        transactions += f"\nWithdrawn: ${value:.2f}"
        print(f"\nValue: ${(value):.2f} withdrawn using limit.")
    else:
        print("\nNot enough limit.")
    
        
def account_statement():
    global balance
    global limit
    global transactions
    global WITHDRAW_LIMITS

    print()
    print("=====Account Statement=====")
    if WITHDRAW_LIMITS < 3:
        print(f"\nYou can make {WITHDRAW_LIMITS} withdraw. ")

    if limit < 500:
        print(f"\nLimit value available: ${limit:.2f}")
    
    print("\nNo transaction made." if transactions == " " else transactions)
    print()
    print(f"\nTotal balance account: ${balance:.2f}\n")
    print("===========================\n")


def exit():
    return print('\nThanks for using our system!!!')


def main():
    choose = options()
    while True:
        if choose == ADD_TO_ACCOUNT:
            add_to_account()
        elif choose == WITHDRAWN_MONEY:
            withdrawn_money()
        elif choose == ACCOUNT_STATEMENT:
            account_statement()
        elif choose == EXIT_APP:
            exit()
            break
        else:
            print('\nInvalid choise')

        choose = options()
    
main()