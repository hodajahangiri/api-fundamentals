import requests
import json
from rich.console import Console

console = Console()

# Get random activity
def get_random_activity():
    """
    Get a completely random activity suggestion
    API: https://bored-api.appbrewery.com/random
    """
    # YOUR CODE HERE
    # 1. Make a GET request to the API
    url = "https://bored-api.appbrewery.com/random"
    try:
        response = requests.get(url)
        # 4. Handle any errors
        if response.status_code == 200:
            # 2. Parse the JSON response
            response_data = response.json()
            # 3. Print the activity and type nicely
            title = "\nRandom Activity Suggestion:"
            show_activity(response_data,title)
            save_favorite_activity(response_data)
        elif response.status_code >= 400:
            console.print(f"[red]API Error: Status Code {response.status_code}, Response: Client Error!!")
        elif response.status_code >= 500:
            console.print(f"[red]API Error: Status Code {response.status_code}, Response: Server Error!!")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]An error occurred during the request: {e}")
        
# Get activity by type
def get_activity_by_type():
    """
    Let user choose an activity type and get a suggestion
    API: https://bored-api.appbrewery.com/filter?type={type}
    Types: education, recreational, social, diy, charity, cooking, relaxation, music, busywork
    """
    # YOUR CODE HERE
    url = "https://bored-api.appbrewery.com/filter"
    while True:
        # 1. Show the user available types
        show_available_types()
        try:
            # 2. Get their choice
            choice_type = input("\nChoose an option (1-7): ")
            if choice_type == '1':
                params = {"type" : "education"}
                break
            elif choice_type == '2':
                params = {"type" : "recreational"}
                break
            elif choice_type == '3':
                params = {"type" : "social"}
                break
            elif choice_type == '4':
                params = {"type" : "charity"}
                break
            elif choice_type == '5':
                params = {"type" : "cooking"}
                break
            elif choice_type == '6':
                params = {"type" : "relaxation"}
                break
            elif choice_type == '7':
                params = {"type" : "busywork"}
                break
            else:
                console.print("[red]Invalid choice! Please choose 1-7.")
        except KeyboardInterrupt:
            console.print("[red]\n\nSomething wrong happens.....")
            break
    # 3. Make API request with type parameter
    try:
        if params:
            response = requests.get(url, params = params)
        else:
            console.print("[red]Params can not be None...")
        # Handle any errors
        if response.status_code == 200:
            #  Parse the JSON response
            response_data = response.json()
            # 4. Display the result
            counter = 1
            title = f"\nActivity Suggestion By Type({params["type"]}):"
            for response_data_item in response_data:
                show_activity(response_data_item,title,counter)
                save_favorite_activity(response_data_item)
                counter += 1
        elif response.status_code >= 400:
            console.print(f"[red]API Error: Status Code {response.status_code}, Response: Client Error!!")
        elif response.status_code >= 500:
            console.print(f"[red]API Error: Status Code {response.status_code}, Response: Server Error!!")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]An error occurred during the request: {e}")
    
# Get activity by participants
def get_activity_by_participants():
    """
    Get activity suggestions based on number of participants
    API: https://bored-api.appbrewery.com/filter?participants={number}
    """
    # YOUR CODE HERE
    url = "https://bored-api.appbrewery.com/filter"
    # 1. Ask user how many participants
    while True:
        try:
            participants = int(input("How many participants(1,2,3,4,5,6,or 8)? "))
            if participants in [1,2,3,4,5,6,8]:
                params = {"participants": participants}
                break
            else:
                console.print("\n[red]you have to choose number from [1,2,3,4,5,6,8]")
        except ValueError:
            console.print("\n[red]you have to choose number from [1,2,3,4,5,6,8]")
        except KeyboardInterrupt:
            console.print("\n\n[red]Something wrong happens.....")
            break
    # 2. Make API request with participants parameter
    try:
        if params:
            response = requests.get(url, params = params)
        else:
            console.print("[red]Params can not be None...")
        # Handle any errors
        if response.status_code == 200:
            #  Parse the JSON response
            response_data = response.json()
            # 3. Display the activity suggestion
            counter = 1
            title = f"\nActivity Suggestion By Participants({params["participants"]}):"
            for response_data_item in response_data:
                show_activity(response_data_item,title,counter)
                save_favorite_activity(response_data_item)
                counter += 1

        elif response.status_code >= 400:
            console.print(f"[red]API Error: Status Code {response.status_code}, Response: Client Error!!")
        elif response.status_code >= 500:
            console.print(f"[red]API Error: Status Code {response.status_code}, Response: Server Error!!")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]An error occurred during the request: {e}")

def save_favorite_activity(new_data):
    """
    Get an activity and save it to a text file
    """
    # YOUR CODE HERE
    # 1. after getting an activity from one of the other functions
    # 2. Ask user if they want to save it
    # Specify the filename
    filename = 'favorite_activities.json'
    while True:
        choice = input("Do you want to save this activity to your favorite? yes/no ")
        if choice.lower() == "yes":
            # 3. If yes, append to 'favorite_activities' list
            # Read existing data
            try:
                with open(filename, 'r') as file:
                    existing_data = json.load(file)
                    print("===========existing_data:   ", existing_data)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_data = [] # Initialize as an empty list if the file doesn't exist

            # Append the new dictionary
            print("new data: ", new_data)
            existing_data.append(new_data)
            print("===========existing_data_after_appending:   ", existing_data)
            with open(filename, 'w') as file:
                json.dump(existing_data, file, indent=4) # indent for pretty-printing
            # with open("favorite_activities.txt", "a") as file:
            #     file.write(str(response_data))
                # 4. Print "Activity Saved"
                console.print("[green]Activity is Saved to your favorite.")
                break
        elif choice.lower() == "no":
            break
        else:
            console.print("[red]You have to write yes or no.")

def view_saved_activities():
    """
    Read and display saved activities from file
    """
    # YOUR CODE HERE
    filename = 'favorite_activities.json'
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            # Loop through the list of saved activities and display each one
            counter = 1
            title = f"\nFavorite Activities:"
            if data:
                for item in data:
                    show_activity(item,title,counter)
                    counter += 1
            else:
                console.print("[purple]There is no favorite activity....")
    except (FileNotFoundError, json.JSONDecodeError):
        console.print("[red]File is not found.....")

# Show available types to the user
def show_available_types():
    """Show available types"""
    console.print("\n[blue]Available types to choose: ")
    console.print("[blue]=" * 21)
    console.print("[blue]1.[/blue] education")
    console.print("[blue]2.[/blue] recreational")
    console.print("[blue]3.[/blue] social")
    console.print("[blue]4.[/blue] charity")
    console.print("[blue]5.[/blue] cooking")
    console.print("[blue]6.[/blue] relaxation")
    console.print("[blue]7.[/blue] busywork")

def show_menu():
    """Display the main menu"""
    console.print("\n[blue]Bored Activity Finder")
    console.print("[blue]=" * 21)
    console.print("[blue]1.[/blue] Get a random activity")
    console.print("[blue]2.[/blue] Get activity by type")
    console.print("[blue]3.[/blue] Get activity by participants")
    # console.print("[blue]4.[/blue] Save my favorite activities")
    console.print("[blue]4.[/blue] View my saved activities")
    console.print("[blue]5.[/blue] Exit")


# show the result
def show_activity(data,title,counter=0):
    console.print(f"\n[blue]{title}")
    console.print("[blue]=" * 30)
    if counter != 0 :
        console.print(f"[yellow]Activity Number:[/yellow] {counter}")
    console.print(f'''[yellow]Activity:[/yellow] {data["activity"]}
[yellow]Type:[/yellow] {data["type"]}
[yellow]Participants:[/yellow] {data["participants"]}\n''')



def main():
    """Main function with menu loop"""
    console.print("[purple]Welcome to the Bored Activity Finder!")
    while True:
        show_menu()
        try:
            choice = input("\nChoose an option (1-5): ")
            if choice == '1':
                get_random_activity()
            elif choice == '2':
                get_activity_by_type()
            elif choice == '3':
                get_activity_by_participants()
            # elif choice == '4':
            #     save_favorite_activity()
            elif choice == '4':
                view_saved_activities()
            elif choice == '5':
                console.print("[blue]Thanks for using Bored Activity Finder!")
                break     
            else:
                console.print("[red]Invalid choice! Please choose 1-5.")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

if __name__ == "__main__":
    main()
