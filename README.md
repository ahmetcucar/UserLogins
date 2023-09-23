# UserLogins

The UserLogins project is a secure user login system that incorporates salting and hashing techniques to ensure the safety of user credentials. It provides a flexible storage solution, allowing you to store user data either in JSON files or SQLite databases.

## Motivation

The motivation behind this project is threefold:

1. Understanding User Authentication: The project aims to emulate how websites and companies securely store user account information, including usernames and password hashes. By implementing my own secure user login system, I gained valuable insights into industry-standard practices.

2. Enhancing Skills in JSON and SQL: UserLogins served as a great platform to learn how to use JSON and SQL effectively in Python.

3. Building for the Future: By creating a robust user login system, I have a reusable package that can be integrated into larger full-stack projects. It will be useful to be able to handle different account logins/user-authentication.

## How it works

The UserLogins project revolves around an abstract base class named "PasswordManager." This base class defines a set of self-explanatory methods that must be implemented by its child classes to ensure consistency and security:

- `add_credentials`
- `delete_credentials`
- `verify_credentials`
- `change_password`
- `wipe_credentials`
  
Two concrete classes, each implementing the PasswordManager interface, are provided:
1. `json_pm.py`: This class stores user data in JSON files. While functional, it is not the recommended approach for large-scale applications due to potential efficiency concerns.
2. `sql_pm.py`: The preferred choice for storing user data. This class utilizes SQLite3 databases, offering improved efficiency and scalability, especially when dealing with a large number of user accounts.

Finally, if you run `main.py` we have the main terminal program that the user can interact with to manage their passwords. This runs on an instance of `sql_pm`. Here is a glimpse of what it looks like:

<img width="837" alt="image" src="https://github.com/ahmetcucar/user-logins/assets/103691809/34c16afb-bcf4-4a87-92bd-ad98cbb17013">

https://github.com/ahmetcucar/user-logins/assets/103691809/d2824f70-1c6f-4947-ba60-cdf26dcdc73e

## How to use

This project primarily relies on Python's built-in libraries, however I believe you will need Python version 3.10 and above to run.
For the database, we are using SQLite3 but that should come with every OS.  
  
To run the program, first clone the repo, then run main.py:
```
git clone https://github.com/ahmetcucar/user-logins.git
cd user-logins
python3 main.py
```

Or to use in your app, you can import `sql_pm.py` and use your own instance of the class.

Enjoy!!!
