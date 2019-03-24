import time

# region: Variables
# user1 info
user1_name = "Ahmet"
user1_password = "1234"
user1_currency = 0
# user2 info
user2_name = "Zeynep"
user2_password = "4321"
user2_currency = 0
# login check parameters
login, login_user1, login_user2 = False, False, False


# endregion: Variables

def login_user():
    while True:
        global user1_name, user1_password
        global user2_name, user2_password
        global login, login_user1, login_user2  # login check parameters
        username = raw_input("\nUser Name:")
        password = raw_input("Password:")
        if username == user1_name and password == user1_password:
            login = True
            login_user1 = True
            print("\nWelcome " + username + "!")
            return username
        elif username == user2_name and password == user2_password:
            login = True
            login_user2 = True
            print("\nWelcome " + username + "!")
            return username
        else:
            print("!!!login info error!!!")


def withdraw_money(user_currency):
    input_money = int(raw_input("\nPlease enter the amount you want to withdraw:"))
    if input_money <= user_currency:
        user_currency = user_currency - input_money
        print(str(input_money) + " TL withdrawn from your account\n\nGoing back to main menu...")
        return user_currency
    print("You don't have " + str(input_money) + " TL in your account\n\nGoing back to main menu...")
    return user_currency


def deposit_money(user_currency):
    input_money = int(raw_input("\nPlease enter the amount you want to drop:"))
    user_currency = user_currency + input_money
    print(str(input_money) + " TL added to your account\n\nGoing back to main menu...")
    return user_currency


def transfer_money(from_user_currency, to_user_currency):
    input_money = int(raw_input("\nPlease enter the amount you want to transfer:"))
    # region: transfer impossible
    if input_money > from_user_currency:
        print("Sorry! You don't have enough money to complete this transaction\n")
        print("1. Go back to main menu\n2. Transfer again")
        selected_service = raw_input(">>>")
        if selected_service == "1":  # return to menu
            return from_user_currency, to_user_currency
        elif selected_service == "2":  # transfer again
            return transfer_money(from_user_currency, to_user_currency)
        else:  # invalid input/service_number
            print("service error")
    # endregion: transfer impossible
    # region: transfer possible from the currency from_user_currency to the currency to_user_currency
    else:
        from_user_currency = from_user_currency - input_money
        to_user_currency = to_user_currency + input_money
        print("Money transferred successfully!\n\nGoing back to main menu...")
        return from_user_currency, to_user_currency
    # endregion: transfer possible from the currency from_user_currency


def show_account_info(username, password, currency):
    # localtime at 'Year-Mounth-Day Hour:Minute.Second' format
    current_daytime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("------- SEHIR Bank -------\n----" + current_daytime + "----\n----------------------------")
    print("Your Name: " + str(username) + "\nYour Password: " + str(password) + "\nYour Amount (TL): " + str(currency))
    return current_daytime, username, password, currency


def logout_user():
    global login, login_user1, login_user2  # login check parameters
    global user1_name, user2_name  # user names
    if login_user1:
        login_user1 = False
        print("\nGood Bye " + user1_name + ":)")
        login = False
    elif login_user2:
        login_user2 = False
        print("\nGood Bye " + user2_name + ":)")
        login = False
    else:
        print("!!!logout error!!!")


def bank_app():
    # user1 info
    global user1_name, user1_password, user1_currency
    # user2 info
    global user2_name, user2_password, user2_currency
    # login check parameters
    global login, login_user1, login_user2

    while True:
        # region: with login
        if login:  # check for login
            print("\nPlease enter the number of the service:")
            print("1. Withdraw Money\n2. Deposit Money\n3. Transfer Money\n4. My Account Information\n5. Logout")
            selected_service = raw_input(">>>")
            # region: Withdraw Money
            if selected_service == "1":
                if login_user1:  # check for login of user1 (Ahmet)
                    user1_currency = withdraw_money(user1_currency)
                elif login_user2:  # check for login of user2 (Zeynep)
                    user2_currency = withdraw_money(user2_currency)
                else:  # check for any login error...
                    print("!!!login error!!!")
            # endregion: Withdraw Money
            # region: Deposit Money
            elif selected_service == "2":
                if login_user1:  # check for login of user1 (Ahmet)
                    user1_currency = deposit_money(user1_currency)
                elif login_user2:  # check for login of user2 (Zeynep)
                    user2_currency = deposit_money(user2_currency)
                else:  # check for any login error...
                    print("!!!login error!!!")
            # endregion: Deposit Money
            # region: Transfer Money
            elif selected_service == "3":
                if login_user1:  # check for login of user1 (Ahmet)
                    user1_currency, user2_currency = transfer_money(user1_currency, user2_currency)
                elif login_user2:  # check for login of user2 (Zeynep)
                    user2_currency, user1_currency = transfer_money(user2_currency, user1_currency)
                else:  # check for any login error...
                    print("!!!login error!!!")
            # endregion: Transfer Money
            # region: Show Account Information
            elif selected_service == "4":
                if login_user1:  # check for login of user1 (Ahmet)
                    show_account_info(user1_name, user1_password, user1_currency)
                elif login_user2:  # check for login of user2 (Zeynep)
                    show_account_info(user2_name, user2_password, user2_currency)
                else:  # check for any login error...
                    print("!!!login error!!!")
            # endregion: Show Account Information
            # region: Logout
            elif selected_service == "5":
                logout_user()
            # endregion: Logout
            # region: invalid input/service_number
            else:
                print("!!!service error!!!")
            # endregion: invalid input/service_number
        # endregion: with login
        # region: without login
        else:  # Welcome page
            print("\n---Welcome to SEHIRBank V.0.1 ---\n\n1. Login\n2. Exit")
            selected_service = raw_input(">>>")
            # region: Login
            if selected_service == "1":
                login_user()
            # endregion: Login
            # region: Exit
            elif selected_service == "2":
                return
            # endregion: Exit
            # region: invalid input/service_number
            else:
                print("!!!service error!!!")
            # endregion: invalid input/service_number
        # endregion: without login


bank_app()
