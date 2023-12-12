import json
import requests

def send_command_to_node_mcu(NODEMCU_BASE_URL, command):
    # Create a dictionary 
    command_dict = {'command': command}
    # dictionary to a JSON string
    command_json = json.dumps(command_dict)
    # content type as JSON
    headers = {'Content-Type': 'application/json'}

    print(f"Sending JSON: {command_json}")

    try:
        # Send a POST request 
        response = requests.post(f"{NODEMCU_BASE_URL}/command", data=command_json, headers=headers)
        response.raise_for_status()  # Raise an error if the request failed

        if response.json().get('status') == 'success':
            print(f"Command {command} sent successfully.")
        else:
            print(f"NodeMCU responded with an error: {response.json().get('error')}")

    except requests.RequestException as e:
        print(f"Failed to send command to NodeMCU: {e}")


def main():
#This is for testing purposes 
    NODEMCU_BASE_URL = 'http://192.168.183.102'
    test_command = [200, 100, 200]
    for command in test_command:
        send_command_to_node_mcu(NODEMCU_BASE_URL, command)

if __name__ == '__main__':
    main()
