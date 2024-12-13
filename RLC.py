import csv
import re
from RLClibrary import Speaker
import numpy as np

#this section takes the speakers form the csv file and adds them to list
def get_speakers_from_csv(file_path):
    #creates the dictionary for speakers
    speakers = []
    try:
        #opens the csv file and jumps to the first record
        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip header row
            #this section iterates through each row and appends the data to the approriate list at longs at the data is valid
            for row in reader:
                if validate_speaker_data(row):
                    speaker_data = {
                        "name": row[0],
                        "resistance": float(row[1]),
                        "inductance": float(row[2]),
                        "Resonant_frequency": float(row[3]),
                        "QES": float(row[4]),
                        "QMS": float(row[5]),
                    }
                    speakers.append(speaker_data)
                else:
                    print(f"Invalid data row skipped: {row}")
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

#this section makes sure to validate the data in the CSV file
def validate_speaker_data(row):
    #makes sure the values arent any special characters
    name_pattern = r"^[A-Za-z0-9 _-]+$"
    # makes sure the values are positive integers and floats
    number_pattern = r"^\d+(\.\d+)?$"  

    if not re.match(name_pattern, row[0]):
        return False
    for value in row[1:]:
        if not re.match(number_pattern, value):
            return False
    return True



    return speakers

# this section calculates and ouptutes the impedance file into a txt
def write_impedance_to_file(speaker_name, frequencies, impedances, output_file):
    try:
        with open(output_file, "w") as file:
            file.write(f"Impedance Data for {speaker_name}\n")
            file.write("Frequency (Hz), Impedance (Ohms)\n")
            for freq, imp in zip(frequencies, impedances):
                file.write(f"{freq}, {imp:.2f}\n")
        print(f"Impedance data saved to {output_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    # Load speakers from the CSV file
    csv_file_path = "speakers.csv" 
    speakers = get_speakers_from_csv(csv_file_path)
    #senario if there is no file
    if not speakers:
        print("No valid speakers found in the CSV file.")
        exit()

    # Step 2: displays the speakers in the csv (could have done it with cowsay)
    print("Available Speakers:")
    for idx, speaker in enumerate(speakers):
        print(f"{idx + 1}: {speaker['name']}")
    #gives the user the option to choose the speaker wanted if it exists
    try:
        choice = int(input("Select a speaker by number: ")) - 1
        if choice < 0 or choice >= len(speakers):
            raise ValueError("Invalid choice.")
    except ValueError as e:
        print("Invalid input. Exiting.")
        exit()

    selected_speaker_data = speakers[choice]

    # this section takes the selected data and turns it into an object and sends it to the library
    selected_speaker = Speaker(
        name=selected_speaker_data["name"],
        resistance=selected_speaker_data["resistance"],
        inductance=selected_speaker_data["inductance"],
        Resonant_frequency=selected_speaker_data["Resonant_frequency"],
        QES=selected_speaker_data["QES"],
        QMS=selected_speaker_data["QMS"],
    )

    #this section defiens the resolution of the graph on pyplot and calculates it
    freq_range = (20, 20000, 1)  # 20 Hz to 20 kHz in steps of 100 Hz
    frequencies = np.arange(*freq_range)
    impedances = [selected_speaker.calculate_impedance(f) for f in frequencies]

    # this section just gets the data to be sent to the txt file maker
    output_file_path = "impedance_output.txt"
    write_impedance_to_file(selected_speaker.name, frequencies, impedances, output_file_path)


    # this last section will plot the impedance graph
    selected_speaker.plot_impedance(freq_range)
