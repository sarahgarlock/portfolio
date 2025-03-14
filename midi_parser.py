import pretty_midi
import psycopg2
import numpy as np
import music21
from collections import defaultdict

# Function to analyze MIDI data and detect chords
def detect_chords(midi_data):
    chord_progressions = []
    # Dictionary to store chords by their start time
    chord_dict = defaultdict(list)
    
    # Iterate through each instrument in the MIDI file
    for i, instrument in enumerate(midi_data.instruments):
        for note in instrument.notes:
            pitch = note.pitch
            start = note.start
            end = note.end
            chord_dict[start].append(pitch)
    
    # Sort chords by start time
    for start_time in sorted(chord_dict.keys()):
        chord_progressions.append(sorted(chord_dict[start_time]))
    
    return chord_progressions

# Function to detect repeated patterns (chord progressions)
def detect_repeated_patterns(chords, threshold=0.8):
    repeated_patterns = []
    for i in range(len(chords) - 1):
        # Look for repeated patterns within a given threshold
        for j in range(i + 1, len(chords)):
            # Compare the current chord progression to the rest
            if np.array_equal(chords[i], chords[j]):
                repeated_patterns.append((chords[i], i, j))
    return repeated_patterns

# Function to parse the MIDI file and analyze it
def parse_and_analyze_midi(file_path):
    midi_data = pretty_midi.PrettyMIDI(file_path)
    
    # Detect chord progressions
    chord_progressions = detect_chords(midi_data)
    print(f"Detected chord progressions: {chord_progressions}")
    
    # Detect repeated chord progressions
    repeated_patterns = detect_repeated_patterns(chord_progressions)
    print(f"Detected repeated patterns: {repeated_patterns}")
    
    # Store detected patterns in the database
    for pattern, start_idx, end_idx in repeated_patterns:
        pattern_name = f"Chord Progression {start_idx + 1}"
        pattern_type = "chord progression"
        pattern_data = str(pattern)  # Store chord pattern as string (or JSON)
        start_time = chord_progressions[start_idx][0]  # Use the start time of the first chord
        end_time = chord_progressions[end_idx][-1]  # Use the end time of the last chord
        song_title = "Song A"  # Replace with actual song title
        
        # Insert detected pattern into the database
        store_pattern(pattern_name, pattern_type, pattern_data, start_time, end_time, song_title)

# Function to store detected patterns into the database
def store_pattern(pattern_name, pattern_type, pattern_data, start_time, end_time, song_title):
    cur.execute(
        "INSERT INTO midi_patterns (pattern_name, pattern_type, pattern_data, start_time, end_time, song_title) VALUES (%s, %s, %s, %s, %s, %s)",
        (pattern_name, pattern_type, pattern_data, start_time, end_time, song_title)
    )
    conn.commit()

# Set up PostgreSQL connection
conn = psycopg2.connect(
    dbname="midi_data", 
    user="sarahgarlock", 
    password="garlock10",  
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

# Example usage
file_path = "/Users/sarahgarlock/Documents/_Socials/MIDI/out_early.mid"
parse_and_analyze_midi(file_path)

# Close connection
cur.close()
conn.close()
