# pathplanning.py

""" Calculate the smallest turn direction from current to target orientation.
    Returns the turn command and the amount to turn."""
def calculate_turn_direction(current_orientation, target_orientation):
    # Normalize angles between 0 and 359 degrees
    current_orientation %= 360
    target_orientation %= 360

    # Calculate the angular difference
    angular_difference = (target_orientation - current_orientation + 360) % 360

    # Determine turn direction (right or left)
    if angular_difference == 0:
        return 0  # No turn needed
    elif angular_difference <= 180:
        return 2  # Turn right
    else:
        return 4  # Turn left

def generate_path_commands(marker_positions):
    commands = []
    if all(key in marker_positions for key in [7, 8, 9]):
        # Access the orientation from the dictionary, not a tuple
        turn_to_pallet = calculate_turn_direction(
            marker_positions[7]['orientation'], 
            marker_positions[8]['orientation']
        )
        if turn_to_pallet != 0:
            commands.append(turn_to_pallet * 100)  # Encode the turn as a 3-digit command

        # Assume the bot moves forward after turning
        commands.append(100)  # Move forward

        # Calculate the direction to turn from marker 8 to marker 9
        turn_to_destination = calculate_turn_direction(
            marker_positions[8]['orientation'], 
            marker_positions[9]['orientation']
        )
        if turn_to_destination != 0:
            commands.append(turn_to_destination * 100)  # Encode the turn as a 3-digit command
        
        # Move forward towards the destination
        commands.append(100)  # Move forward
    else:
        # If not all markers are detected, we stop the bot
        commands.append(0)  # Stop command

    return commands
