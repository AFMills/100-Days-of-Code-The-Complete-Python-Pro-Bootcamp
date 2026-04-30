from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

is_on = True

while is_on:
    options = menu.get_items()
    user_choice = str(input(f"What would you like? ({options}): ")).lower()
    if user_choice == "off":
        is_on = False
    elif user_choice == "report":
        coffee_maker.report()
        money_machine.report()
    else:
        drink_choice = menu.find_drink(user_choice)
        if coffee_maker.is_resource_sufficient(drink_choice) and money_machine.make_payment(drink_choice.cost):
                coffee_maker.make_coffee(drink_choice)
