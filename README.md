# CIS2250Project
Authors: Mariam Ahmed, Devnash Devnash, Dana Kleber, Tim Sheremet

# Description
This program allows the user to analyze the popularity of names in Maine and Hawaii based on gender.
Once the user has chosen a state and gender, the program presents the user with a menu with the following options:

1. View popularity of a name over X years (ie 1970-2000 popularity of name x)
2. View most popular names for all years
3. View most popular names for one year
4. View top 5 longest names
5. Search name origin
6. Exit

# Dependencies
Ensure pandas, difflib numpy & matplotlib are installed.
If they are not installed, use the following command:
```bash
pip install pandas matplotlib numpy difflib
```

# pip command not found
If pip install command does not work ensure that you have pip installed. 
To check this run this command: 

pip3 install --upgrade pip

The command above installs the pip command on your computer and 
will allow you to install the dependencies using the command listed above

# Executing the program
To execute the program, use the following command:
```bash
python teamProject.py
```

# Known Issues
- The search name option only accounts for a small amount of names, not every name will have an origin
- If a character is entered as a menu option, there is a value error
- Option 1 is case sensitive, the first letter of the name should be capitalized
