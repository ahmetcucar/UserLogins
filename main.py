credentials = {
    "ahmet": "1234",
    "bob": "builder",
    "john": "doe"
}

def isValidCredentials(username, password):
    if username.lower() in credentials:
        if credentials[username] == password:
            return True
    return False

def main():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if isValidCredentials(username, password):
        print("Welcome,", username)
    else:
        print("Wrong username or password!")

main()