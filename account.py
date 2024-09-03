ADD_TO_ACCOUNT = 1
WITHDRAWN_MONEY = 2
ACCOUNT_STATEMENT = 3
EXIT_APP = 4

balance = 0.0
limit = 500.0
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

    value = float(input("\nType the value to add in the account: $"))

    if value >= 0:
        if limit < 500:
            additional_limit = min(500 - limit, value)
            limit += additional_limit
            balance += (value - additional_limit) 
            print(f"\nValue: ${value:.2f} successfully added.")
        else:
            balance += value
            print(f"\nValue: ${value:.2f} successfully added.")
    else:
        print('\nThe value must be at least 1 dollar')


def withdrawn_money():
    global balance
    global limit
    global WITHDRAW_LIMITS 

    value = float(input("\nType the value withdraw: $"))

    if WITHDRAW_LIMITS >= 1:
        if value <= balance:
            balance -= value
            WITHDRAW_LIMITS -= 1
            print(f"\nValue: ${value:.2f} withdraw.")
        elif (value <=  limit + balance) and (limit > 0):
            limit_used = (value - balance)
            limit -= limit_used
            balance = 0
            WITHDRAW_LIMITS -= 1
            print(f"\nValue: ${(value):.2f} withdrawn using limit.")
        else:
            print("\nNot enough limit.")
    else:
        print('\nTransitions limit made')


def account_statement():
    global balance
    global limit
    global WITHDRAW_LIMITS

    print()
    print("=====Account Statement=====")
    if WITHDRAW_LIMITS < 3:
        print(f"\nYou can make {WITHDRAW_LIMITS} withdraw. ")
    else:
        print(f"\nNo withdraw made")

    if limit < 500:
        print(f"\nLimit value available: {limit}")

    print(f"\nTotal balance account: {balance}\n")
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