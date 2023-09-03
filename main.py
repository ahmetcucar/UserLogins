correct_username = "Ahmet"
correct_password = "1234"

def isValidCredentials(username, password):
    return (username.lower() == correct_username.lower()
            and password == correct_password)

def main():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if isValidCredentials(username, password):
        print("Welcome,", username)
    else:
        print("Wrong username or password!")

main()