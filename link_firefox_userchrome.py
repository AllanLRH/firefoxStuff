#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import pathlib
import yaml


def promot_user_for_folder(profile_folders):
    # Print all possible folders
    for i, fld in enumerate(profile_folders, start=1):
        print(f"{i}:  {fld}")
    print("Please select which profile folder to use (enter number and press enter):")
    while True:  # keep prompting until we recieve a valid input
        try:
            userinput = input("> ").strip()
            idx = int(userinput) - 1
            if idx < 0:
                print(f"The value must be between 1 and {len(profile_folders)}")
                continue  # next iteration
            userinput = pathlib.Path(profile_folders[idx])
            break  # break out of while loop
        except ValueError as err:  # Invalid value specified
            if userinput.isnumeric():
                print("Unknown error:\n", err, "\n")
            else:
                print("Input mus be an integer.")
        except IndexError as err:  # Index probably out of bounds
            print(f"Value must be between 1 and {len(profile_folders)}, but you specified {idx}")
    return userinput
    

# Load preferences
with open("filepaths.yaml") as fid:
    filepath_dct = yaml.load(fid)
file_to_link                = pathlib.Path(filepath_dct["file_to_link"])
folder_with_firefox_profile = pathlib.Path(filepath_dct["folder_with_firefox_profile"])

# If there is more than one profile folder, prompt the user to chose which one to use
profile_folders             = [el for el in folder_with_firefox_profile.iterdir() if el.is_dir()]
if len(profile_folders) > 1:
    fld_chosen = promot_user_for_folder(profile_folders)
else:  # there is only one profile folder
    fld_chosen = pathlib.Path(profile_folders[0])

# Check that there is a "chrome" directory, and if there is, remove the userchrome.css file or symlink
# If there is a chrome, but it is a file, prompt the user and exit with exit code 1
chrome = fld_chosen / "chrome"
if chrome in fld_chosen.iterdir():
    if chrome.is_dir():
        userchrome = chrome/"UserChrome.css"
        if userchrome in chrome.iterdir() and (userchrome.is_file() and userchrome.is_symlink()):
            userchrome.unlink()
    else:
        print("Cannot make the chrome dir, since a file exists with the same path", file=sys.stderr)
        sys.exit(1)

userchrome_link_destination = pathlib.Path(fld_chosen, "chrome/UserChrome.css")
userchrome_link_destination.symlink_to(file_to_link)
