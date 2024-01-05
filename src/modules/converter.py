def vtt_to_txt(transcript, output_path):
    """
    Convert a webvtt meeting transcript .vtt file to a .txt file and remove redundant information

    Parameters:
    - transcript (str): Path to the .vtt file in the Docs folder

    Returns:
    - raw_txt (str): Path to the raw .txt file of the meeting transcript
    """
    # if not transcript.startswith("Docs/"):
    #     transcript = f"Docs/{transcript}"
    
    vtt_path = transcript
    
    print(f"Reading from {vtt_path}")  # Debugging line
    
    with open(vtt_path, "r", encoding="utf-8") as file:
        vtt_content = file.readlines()

    # Process and refine the content, omitting the "WEBVTT" redundant speaker information
    file_txt = []
    current_speaker = None
    current_start_timestamp = None
    current_end_timestamp = None
    speaker_dialogues = []

    for line in vtt_content:
        line = line.strip()
        print(f"Processing line: {line}")
        # Skip "WEBVTT" and empty lines
        if not line or line == "WEBVTT":
            continue

        # If line contains a speaker's name
        if '-->' in line:
            new_speaker1 = line.split(None,2)[0] # Get the speaker's first name
            new_speaker2 = line.split(None,2)[1] # Get the speaker's last name
            new_speaker = new_speaker1 + ' ' + new_speaker2
            # If we have a previous speaker's dialogues, append them to the output
            if current_speaker and new_speaker != current_speaker:
                file_txt.append("\n")
                # Add the previous speaker's name and timestamps to the output
                file_txt.append(f'### "{current_speaker}" [{current_start_timestamp}-{current_end_timestamp}]')
                file_txt.extend(speaker_dialogues) # Add the speaker's dialogues to the output
                speaker_dialogues = [] # Reset the speaker's dialogues
            
            current_speaker = new_speaker # Update the current speaker
            current_start_timestamp = None # Reset the start timestamp

            # If line contains a timestamped dialogue
            timestamp_start = line.split(None,4)[2] # Get the start timestamp
            timestamp_end = line.split(None,4)[4] # Get the end timestamp
            
            # Setting the start timestamp if it's the first dialogue of the current speaker
            if not current_start_timestamp:
                current_start_timestamp = timestamp_start # Setting the start timestamp
            
            # Updating the end timestamp for every dialogue of the current speaker
            current_end_timestamp = timestamp_end
       
        # If it's a dialogue
        else:
            speaker_dialogues.append(line) # Add the dialogue to the speaker's dialogues

    # Add the last speaker's dialogues to the output
    if current_speaker:
        file_txt.append("\n")
        # file_txt.append(f'### "{current_speaker}" [{current_start_timestamp}-{current_end_timestamp}]')
        file_txt.append(f'### "{current_speaker}"')
        file_txt.extend(speaker_dialogues)

    # Write to a .txt file
    # raw_md = vtt_path.replace(".vtt", ".txt")

    print(f"Writing...")  # Debugging line
    with open(output_path, "w", encoding="utf-8") as file:

        file.write("\n".join(file_txt))
    print(f"Successfully converted {vtt_path} to {output_path}")
    return output_path
