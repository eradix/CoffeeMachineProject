from data import MENU, resources, MONEY


def print_resources():
    """generate a latest report about resources"""
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")


def check_stock_resources(stock_resources, choice_menu):
    """check if stock resources is sufficient"""
    water_need = choice_menu['ingredients'].get('water', 0)
    milk_need = choice_menu['ingredients'].get('milk', 0)
    coffee_need = choice_menu['ingredients'].get('coffee', 0)

    if water_need != 0 and water_need > stock_resources['water']:
        return {
            'is_sufficient': False,
            'resources': 'water'
        }
    elif milk_need != 0 and milk_need > stock_resources['milk']:
        return {
            'is_sufficient': False,
            'resources': 'milk'
        }
    elif coffee_need != 0 and coffee_need > stock_resources['coffee']:
        return {
            'is_sufficient': False,
            'resources': 'coffee'
        }
    return {
        'is_sufficient': True
    }


def calculate_customer_money(quarter, dime, nickle, penny):
    """calculate customer provided money"""
    total_quarter = quarter * MONEY['quarter']
    total_dime = dime * MONEY['dime']
    total_nickle = nickle * MONEY['nickle']
    total_penny = penny * MONEY['penny']
    total_amount = total_quarter + total_dime + total_nickle + total_penny

    return total_amount


def is_sufficient_amount(customer_money, customer_order):
    """check if customer money is sufficient to buy order"""
    if MENU[customer_order]['cost'] > customer_money:
        return False
    return True


def has_change(customer_money, customer_order):
    """check if customer must be given a change"""
    if customer_money > MENU[customer_order]['cost']:
        return True
    return False


def calculate_change(customer_money, customer_order):
    """returns customer change"""
    return customer_money - MENU[customer_order]['cost']


def update_resources(customer_order):
    """update the resources"""
    resources['water'] -= MENU[customer_order]['ingredients'].get('water', 0)
    resources['milk'] -= MENU[customer_order]['ingredients'].get('milk', 0)
    resources['coffee'] -= MENU[customer_order]['ingredients'].get('coffee', 0)


def is_valid_amount(variable):
    """validates if variable is a valid amount"""
    try:
        int_value = float(variable)
        return True
    except ValueError:
        return False


# get valid number inputs
def get_user_amount(prompt):
    """get user amount, prompts if user provide invalid input"""
    is_valid = False
    while not is_valid:
        num = input(prompt)

        if is_valid_amount(num):
            is_valid = True
            return float(num)
        else:
            print("Invalid input. Please provide a valid amount.")


if __name__ == '__main__':
    money = 0
    should_continue = True
    while should_continue:
        # ensures user types the valid input
        while True:
            user_choice = input("What would you like? (espresso/latte/cappuccino): ").lower()
            valid_inputs = ['espresso', 'latte', 'cappuccino', 'report', 'off']
            if user_choice not in valid_inputs:
                print('Invalid input!')
            else:
                break

        # process user choice
        if user_choice == 'off':
            print('Program terminated...')
            break
        elif user_choice == 'report':
            print_resources()
            print(f"Money: ${money}")
        else:
            result_resources = check_stock_resources(resources, MENU[user_choice])
            # check if enough resources to process user choice
            if result_resources['is_sufficient']:
                print("Please insert coins.")
                quarters = get_user_amount("How many quarters?: ")
                dimes = get_user_amount("How many dimes?: ")
                nickles = get_user_amount("How many nickels?: ")
                pennies = get_user_amount("How many pennies?: ")
                total_money = calculate_customer_money(quarter=quarters, dime=dimes, nickle=nickles, penny=pennies)
                # check if user money is sufficient
                if is_sufficient_amount(customer_money=total_money, customer_order=user_choice):
                    money += MENU[user_choice]['cost']
                    # check if user has changed
                    if has_change(customer_money=total_money, customer_order=user_choice):
                        customer_change = calculate_change(customer_money=total_money, customer_order=user_choice)
                        print(f"Here is ${customer_change:.2f} in change.")
                    print(f"Here is your {user_choice} ☕. Enjoy!")
                    update_resources(user_choice)
                else:
                    print("Sorry that's not enough money. Money refunded.")

            else:
                print(f"Sorry there is not enough {result_resources['resources']}.")
