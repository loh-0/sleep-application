from datetime import datetime

data = []

def log_sleep():

    """

    Function to log the users sleep. The function requests that the user enter the data of their sleep, the hours they slept, the quality of their sleep,
    whether or not they exercises and had caffeine and the respective hours spent in each sleep cycle.

    """

    date = input("Enter the date (DD-MM-YYYY): ")
    datetime.strptime(date, "%d-%m-%Y")
    hours = float(input("Enter total hours slept: "))
    quality = int(input("Rate Sleep Quality (1-5): "))
    exercise = input("Exercised Today? (Y/N): ").strip().lower() == "y"
    caffeine = input("Caffeine Consumed Today? (Y/N): ").strip().lower() == "y"

    print("Enter hours spent in each sleep stage:")

    light_sleep = float(input("Light sleep hours: "))
    deep_sleep = float(input("Deep sleep hours: "))
    rem_sleep = float(input("REM sleep hours: "))

    entry = {
    "date": date,
    "hours": hours,
    "quality": quality,
    "exercise": exercise,
    "caffeine": caffeine,
    "stages": {
        "light": light_sleep,
        "deep": deep_sleep,
        "rem": rem_sleep
        }
    }
    data.append(entry)
    
    print("Sleep data logged!")


def view_sleep():

    """
    Function to display the recorded sleep data of a user
    
    """

    if len(data) == 0: 
        print("There is no sleep data to view.")
        return

    print("Your Sleep Data:\n")

    for i, entry in enumerate(data): # accessses the stored sleep information and displays 
        print(f"{i+1}. Date: {entry['date']}, Hours: {entry['hours']}, Quality: {entry['quality']}")
        print(f"Exercise: {entry['exercise']}, Caffeine: {entry['caffeine']}")
        print(f"Sleep Stages - Light: {entry['stages']['light']}, Deep: {entry['stages']['deep']}, REM: {entry['stages']['rem']}")


def main():

    """

    Main Menu function. Uses a while True loop to keep the user on the menu until they terminate the application. Presents users with the different functionality.

    """

    while True:
        print("\nSleep Tracker")
        print("1. Log Sleep")
        print("2. View Data")
        print("3. Exit")
        
        
        option = input("Choose an option: ")
        if option == "1":
            log_sleep()
        elif option == "2":
            view_sleep()
        elif option == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid Selection.")


if __name__ == "__main__":
    main()
