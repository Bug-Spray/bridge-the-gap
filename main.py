"""A starter app to process bridge files."""

# Loads of Python's strength comes from handy "standard" library modules for
# common operations.
import os
import re
import shutil
import time


# Define the source and destination directories
# Use '/' for Windows as well as Linux/Mac - Python will work it out...
SOURCE_FOLDER = '/Users/schatzibaer/Desktop/'
DESTINATION_FOLDER = '/Users/schatzibaer/Downloads/'
# SOURCE_FOLDER = 'C:/Program Files (x86)/some app/source/'
# DESTINATION_FOLDER = 'C:/Program Files (x86)/another app/destination/'
NEW_EXT = '.PBN'  # ...or whatever it was
# Define our "matching" file names:
#  * exactly 5 digits long
#  * .BPN extension (or whatever it was)
FILE_MATCH_REGEX = r'^\d{5}.BPN$'


def transfer(original_path):
    # Extract the file name from the full path
    file_name = os.path.basename(original_path)
    # Get just the name part of the file name - we will "split" the file name,
    # then grab what's at index 0
    # Discard the extension since we're going to change it anyway
    name_only = os.path.splitext(file_name)[0]
    # Build the new path and file name from the pieces
    destination_file_name = name_only + NEW_EXT
    destination_path = os.path.join(DESTINATION_FOLDER, destination_file_name)

    # Quickly confirm the file exists - so far, we haven't actually touched the
    # file system at all; just manipulated some text
    if os.path.exists(original_path):
        shutil.copyfile(original_path, destination_path)

def invalidate_name(original_path):
    # This is a "helper" to change the original file name so that it *doesn't*
    # match our pattern, and thus won't be processed a second time.
    # Naturally, we should run this _after_ the transfer routine, since this
    # modifies the original file.
    file_name = os.path.basename(original_path)
    file_folder = os.path.dirname(original_path)
    # Now we want both the name part and the extension from the file name.
    # We can still "split" the file name, but now we'll keep both parts in two
    # separate variables. Python knows how to "unpack" these two parts.
    name_only, extension = os.path.splitext(file_name)
    destination_file_name = name_only + '#1' + extension
    destination_path = os.path.join(file_folder, destination_file_name)

    os.rename(original_path, destination_path)

def run_loop():
    # Now tie it together
    files_in_folder = os.listdir(SOURCE_FOLDER)
    # Check each file name to match our pattern
    for file in files_in_folder:
        if re.match(FILE_MATCH_REGEX, file):
            print(f'Processing: {file}')
            source_path = os.path.join(SOURCE_FOLDER, file)
            transfer(source_path)
            invalidate_name(source_path)
    
    time.sleep(1)  # 1s sleep; to stop it churning too hard during idle

# Yep, infinite loops are bad, except when they're not
while True:
    run_loop()
