import src.sql_pm as sql_pm
import src.json_pm as json_pm


# TODO: hide user password while typing
def main():
    def printInstructions():
        print("\nHere are the following commands you can use:")
        print("-> add <username> <password>")
        print("-> delete <username>")
        print("-> verify <username> <password>")
        print("-> change <username> <old_password> <new_password>")
        print("-> reset")
        print("-> help")
        print("-> exit")

    print("Hi! Welcome to the SQLite Password Manager!\n")
    pm = sql_pm.SqlitePasswordManager()

    printInstructions()

    comm = input("\nEnter a command: ").split(" ")
    while True:
        match comm[0]:
            case "add":
                if len(comm) == 3:
                    if pm.add_credentials(comm[1], comm[2]):
                        print(f"Added {comm[1]}!")
                    else:
                        print("Failed to add credentials!")
                else:
                    print("Invalid command length!")

            case "delete":
                if len(comm) == 2:
                    if pm.delete_credentials(comm[1]):
                        print(f"Deleted {comm[1]}!")
                    else:
                        print("Failed to delete credentials!")
                else:
                    print("Invalid command length!")

            case "verify":
                if len(comm) == 3:
                    if pm.verify_credentials(comm[1], comm[2]):
                        print(f"Valid credentials!")
                    else:
                        print("Invalid credentials!")
                else:
                    print("Invalid command length!")

            case "change":
                if len(comm) == 4:
                    if pm.change_password(comm[1], comm[2], comm[3]):
                        print(f"Changed {comm[1]}'s password!")
                    else:
                        print("Failed to change password!")
                else:
                    print("Invalid command length!")

            case "reset":
                if len(comm) == 1:
                    if pm.wipe_credentials():
                        print("Cleared out all credentials!")
                    else:
                        print("Failed to clear out all credentials!")
                else:
                    print("Invalid command length!")

            case "help":
                if len(comm) == 1:
                    printInstructions()
                else:
                    print("Invalid command length!")

            case "exit":
                if len(comm) == 1:
                    print("Exiting...")
                    return
                else:
                    print("Invalid command length!")

            case _:
                print("Invalid command!")

        comm = input("\nEnter a command: ").split(" ")


if __name__ == "__main__":
    main()