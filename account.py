ADD_TO_ACCOUNT = 1
WITH_DRAW_MONEY = 2
ACCOUNT_STATEMENT = 3
EXIT_APP = 4

balance = 0
limit = 500
account_statement = ""
TRANSITION_LIMITS = 3


def options():
    print()
    print("=====Banck System=====")
    print(f"{[ADD_TO_ACCOUNT]} Make a deposit")
    print(f"{[WITH_DRAW_MONEY]} Cash out")
    print(f"{[ACCOUNT_STATEMENT]} Account Statement")
    print(f"{[EXIT_APP]} Exit")
    return int(input('Choose a option: '))


def add_to_account():
    global balance
    value = float(input("Type the value to add in the account: "))
    if value >= 0:
        balance += value
    else:
        print('The value must be at least 1 dolar')


def with_draw_money():
    return print('Cash Out')

def account_statement():
    print('Account Statement')

def exit():
    return print('Thanks for using our system!!!')

def main():
    choose = options()
    while True:
        if choose == ADD_TO_ACCOUNT:
            add_to_account()
        elif choose == WITH_DRAW_MONEY:
            with_draw_money()
        elif choose == ACCOUNT_STATEMENT:
            account_statement()
        elif choose == EXIT_APP:
            exit()
            break
        else:
            print('Invalid choise')

        choose = options()
    
main()