from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd 
import matplotlib.pyplot as plt

from tkinter import Tk
from tkinter.filedialog import askopenfilename


# We create a blank df for users who wish to build their data up from scratch using this application

columns = ["Date", "Hours", "Quality", "Exercise", "Caffeine", "Light_Sleep", "Deep_Sleep", "REM_Sleep"]

sleep_df =  pd.DataFrame(columns=columns)

def log_sleep():

    """

    Function to log the users sleep. The function requests that the user enter the data of their sleep, the hours they slept, the quality of their sleep,
    whether or not they exercises and had caffeine and the respective hours spent in each sleep cycle. Using the pandas library we store the data in a df 
    to easily perform our linear regression later. Basic while loops are used to valid the input from the user.

    """
    date_valid = False
    hours_valid = False
    sleep_stages_valid = False
    quality_valid = False 

    # booleans variables that determines whether acceptable user input has been received or not 


    # Check for valid date
    while not date_valid:
        date = input("Enter the date of sleep in DD-MM-YYYY: ")
        try:
            datetime.strptime(date, "%d-%m-%Y")
            date_valid = True
        except ValueError:
            print("Error! Please enter in DD-MM-YYYY")

    while not hours_valid:
        try:
            hours = float(input("Enter total hours slept: "))
            if hours < 0:
                raise ValueError("Error! Invalid hours entered")
            hours_valid = True
        except ValueError:
            print(f"Error! Please enter a valid number of hours.")

    # Check for valid sleep rating
    while not quality_valid:
        try:
            quality = int(input("Rate Sleep Quality from 1–5: "))
            if quality not in range(1, 6):
                raise ValueError("Quality must be between 1 and 5")
            quality_valid = True
        except ValueError:
            print(f"Error! Please enter a valid ratings between 1 and 5 ")

    # Input prompts for exercise rating, will default to false if user does not enter an appropriate value 
    exercise = input("Exercised Today? (Y/N): ").strip().lower() == "y"
    caffeine = input("Caffeine Consumed Today? (Y/N): ").strip().lower() == "y"

    # validation for sleep stages input 
    while not sleep_stages_valid:
        try:
            print("Enter hours spent in each sleep stage:")
            light_sleep = float(input("Light sleep hours: "))
            deep_sleep = float(input("Deep sleep hours: "))
            rem_sleep = float(input("REM sleep hours: "))
            if light_sleep < 0 or deep_sleep < 0 or rem_sleep < 0:
                raise ValueError("Please enter a valid number of hours in each stage")
            total_sleep_stage_hours = light_sleep + deep_sleep + rem_sleep # ensures the hours match for consistency
            if total_sleep_stage_hours != hours:
                raise ValueError(f"Error! {total_sleep_stage_hours} sleep stages hours is not inconsistent {hours} entered.")
            sleep_stages_valid = True
        except ValueError:
            print(f"Error! Please enter a valid number of hours for each stage")

    # entries stored as an entry in the sleep df
    sleep_df.loc[len(sleep_df)] = [date, hours, quality, exercise, caffeine, light_sleep, deep_sleep, rem_sleep]
    
    print("Sleep data logged!")


def view_sleep():

    """
    Function to display the recorded sleep data of a user
    """

    print("Your Sleep Data:\n") #using the df we don't have to do any formatting can simply print it to the terminal 
    print(sleep_df)


def model_sleep():
    """

    Function that uses linear regression to model the collected sleep data. Linear Regression attempts to establish a linear relationship between the data.
    For this, we have selected Sleep Quality to be what we are attempting to predict. We drop Date, Hours (total) since they are irrelevant and Quality for our
    predictors. We use feature scaling as standard good practice for a linear regression model to ensure that no feature dominanates another due to it's large unit of measurement
    and affect our results. To handle our categorical variables, we convert them to 0 and 1 and simplfy include or don't include them. Lastly, we display all our coefficients
    at the end for the user to see.

    """
    if len(sleep_df) < 3: # not enough data to produce meaningful results 
        print("Insufficient data to model")
        return ""

    # Since exercise and caffeine are not quantitative predictors, we can convert them into categorical predictors by including them if true (1) and 
    # excluding if they aren't (0)
    sleep_df["Exercise"] = sleep_df["Exercise"].apply(lambda x: 1 if x else 0)
    sleep_df["Caffeine"] = sleep_df["Caffeine"].apply(lambda x: 1 if x else 0)


    # We define our predictors and what we are trying to predict
    X = sleep_df.drop(columns=['Date', 'Hours', 'Quality'])
    y = sleep_df['Quality']

    # Feature scaling is using to prevent large scale features to dominant other features 
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Create our model
    linear_model = LinearRegression().fit(X_scaled, y)

    coefficients_df = pd.DataFrame({'Feature': X.columns,'Coefficient': linear_model.coef_}) # create a df for the coefficients 

    print(coefficients_df)

    features = X.columns 
    coefficients = linear_model.coef_
    max_idx = coefficients.argmax() 

    # Get the feature with the highest influence
    max_feature = features[max_idx]
    max_coef = coefficients[max_idx]

    print(f"\n{max_feature} has the most positive influence on sleep rating")

def visualise_sleep():

    """

    Function that provides a very simple visual representation of the data collected. It will display the data and the sleep quality and present this
    as a simple line graph.

    """
    # setting up plot
    plt.plot(sleep_df['Date'], sleep_df['Quality'], label='Sleep Quality')
    plt.xlabel('Date')
    plt.ylabel('Quality')
    plt.title('Sleep Quality Over Time')

    # adding a legend, displaying a grid and adjusting the x axis spacing
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    plt.show()



def read_data():
    
    """
    The function is responsible for reading the data into the df. Uses Tkinter to display a pop up to make this process idea. We use the basic .read_csv() method enter the data easily.
    This function overrides any existing data in the df currently.
    """
        
    global sleep_df # required to access the global variable sleep_df, otherwise it will create a local variable
    print("Warning! Read Data will Override any existing data you have entered.")
    Tk().withdraw()
    # UsingTkinter we can open a file dialog to allow user to select their csv file
    file_name = askopenfilename(title="Select a CSV File",filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
    if not file_name:
        print("No file selected.")
        return 
    # Read the selected CSV file into a df
    sleep_df = pd.read_csv(file_name)


def save_data():
    """
    Function for saving data as a csv. Prompts the user to select a file name. Adds ".csv" at the end so that it will be correctly displayed for the read_data() function. 
    
    """

    file_name = input("Enter File Name: ")
    file_name = file_name + ".csv" # adds .csv to end of any file name so it's formatted correctly
    sleep_df.to_csv(file_name,index=False) # index set to false as we don't need indexes 
    print(f"Data successfully saved to {file_name}")

def main():

    """

    Main Menu function. Uses a while True loop to keep the user on the menu until they terminate the application. Presents users with the different functionality.

    """

    while True:
        print("\nSleep Tracker")
        print("1. Log Sleep")
        print("2. View Data")
        print("3. Save Data")
        print("4. Read Data")
        print("5. Model Data")
        print("6. Visualise Data")
        print("7. Exit")
        
        
        option = input("Choose an option: ")
        if option == "1":
            log_sleep()
        elif option == "2":
            view_sleep()
        elif option == "3":
            save_data()
        elif option == "4":
            read_data()
    
        elif option == "5":
            model_sleep()

        elif option == "6":
            visualise_sleep()
     
        elif option == "7":
            print("Closing...")
            break
        else:
            print("Invalid Selection.")

    


if __name__ == "__main__":
    main()
