from robotcom import send_command_to_node_mcu

NODEMCU_BASE_URL = 'http://192.168.50.102'  # Use your NodeMCU's actual IP address
test_command = [200, 100, 200]  # Example command sequence

for command in test_command:
    send_command_to_node_mcu(NODEMCU_BASE_URL, command)
