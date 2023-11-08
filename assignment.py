import requests
import json

#define all the function include in the system
#Menu page showing options for user to choose from
def print_menu():
    print("\nOptions:")
    print("0. Test the connection with Webex server")
    print("1. Display information")
    print("2. Display rooms")
    print("3. Create a room")
    print("4. Send a message to a room")

#Option 0: Test the connection with webex server
def test_connection(accessToken):
    headers = {
        "Authorization": accessToken
    }
    response = requests.get(f"https://webexapis.com/v1/people/me", headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Connection successful!")
    else:
        print("Connection failed. Status code:", response.status_code)


#Option 1: User will display his/her information 
def display_user_info(accessToken):
    url = 'https://webexapis.com/v1/people/me'

    headers = {
        "Authorization": accessToken
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    print("\nName: ", data.get("displayName"))
    print("Nickname: ", data.get("nickName"))
    print("Email: ", data.get("emails")[0])



#Option 2: Displayed list of 5 rooms
def display_rooms(accessToken):
    url = 'https://webexapis.com/v1/rooms'

    headers = {
        "Authorization": accessToken,
        'Content-Type' : 'application/json'
    }
    params={'max':'100'}
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        data = res.json()
        rooms = data.get('items', [])
        i = 1 

        for room in rooms:
            if i > 5:
                break 
            room_id = room.get('id')
            room_title = room.get('title')
            date_created = room.get('created')
            last_activity = room.get('lastActivity')
            
            print("\nRoom ID ", (i),":", room_id)
            print("Room Title:", room_title)
            print("Date Created:", date_created)
            print("Last Activity:", last_activity)
            i += 1
    else:
        print("Failed to retrieve room data. Status code:", res.status_code)

#Option 3: Create a room
def create_room(accessToken):
    roomTitle = input("Enter the room title you want to create: ")
    url = 'https://webexapis.com/v1/rooms'

    headers = {
        "Authorization": accessToken,
        'Content-Type' : 'application/json'
    }
    params={'title': roomTitle}
    res = requests.post(url, headers=headers, json=params)
    if res.status_code == 200:
        data = res.json()
        room_id = data.get('id', None)
        roomTitle = data.get('title', None)

        if room_id and roomTitle:
            print(f"Room' {roomTitle}' has been successfully created.")
        else:
            print("Room creation response does not contain expected data.")
    else:
        print("Failed to create the room, Status code:", res.status_code)


#Option 4: Send message to a room
def send_message(accessToken):
    url = 'https://webexapis.com/v1/rooms'

    headers = {
        "Authorization": accessToken,
        'Content-Type' : 'application/json'
    }
    params={'max': '5'}  # Adjust the max parameter to retrieve the top 5 rooms

    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        data = res.json()
        rooms = data.get('items', [])

        if not rooms:
            print("No rooms found.")
            return

        print("List of 5 Rooms:")
        for i, room in enumerate(rooms, start=1):
            room_title = room.get('title')
            print(f"{i}. {room_title}")

        room_choice = int(input("Enter the number of the room you want to send the message to (1-5): "))

        if 1 <= room_choice <= 5:
            room_id = rooms[room_choice - 1].get('id')
            message = input("Enter the message: ")

            url = 'https://webexapis.com/v1/messages'
            params = {'roomId': room_id, 'markdown': message}
            res = requests.post(url, headers=headers, json=params)

            if res.status_code == 200:
                print("Message has been sent successfully.")
            else:
                print("Failed to send the message. Status code:", res.status_code)
        else:
            print("Invalid room number. Please enter a number between 1 and 5.")
    else:
        print("Failed to fetch room data. Status code:", res.status_code)



accessToken = 'MTYwNWQwNzQtZjM1My00YTY1LWIwZGMtMWQyNTQ4OTYxYWZmNDMyYWQ5NTctYjU4_P0A1_346e751c-7bdb-491d-9858-1355bbf861ac'
#prompt user for the token, or use a hard-corded token
choice = input ("Do you wish to use the hard coded token? (y/n)")

if choice == "N" or choice == "n":
    accessToken = input ("Enter your access token: ")
    accessToken = "Bearer " + accessToken
else: 
    accessToken = "Bearer MTYwNWQwNzQtZjM1My00YTY1LWIwZGMtMWQyNTQ4OTYxYWZmNDMyYWQ5NTctYjU4_P0A1_346e751c-7bdb-491d-9858-1355bbf861ac"

while True:
    print_menu()
    option = input("\nPlease select the option number you would like to proceed: ")

    if option == "0":
        test_connection(accessToken)
        input("Press Enter to return to the menu")
    elif option == "1":
        display_user_info(accessToken)
        input("\nPress Enter to return to the menu")
    elif option == "2":
        display_rooms(accessToken)
        input("\nPress Enter to return to the menu")
    elif option == "3":
        create_room(accessToken)
        input("Press Enter to return to the menu")
    elif option == "4":
        send_message(accessToken)
        input("Press Enter to return to the menu")
    else:
        print("Invalid option. Please select a valid option.")
    