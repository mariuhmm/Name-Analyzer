#!/usr/bin/env python3
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import difflib


def main(argv):
    which_state = int(input("Would you like to view Hawaii (1) or Maine (2)? " ))

    # if you gave an invalid input
    while which_state not in [1, 2]:
        print("\nInvalid choice.")
        which_state = int(input("Would you like to view Hawaii (1) or Maine (2)? " ))
    
    # if you pick Hawaii
    if which_state == 1:
        inputFileName = "STATE/HI.TXT"
        gender = input("Enter gender (M/F): ")
        while gender not in ['M', 'F']:
            print("Invalid choice.")
            gender = input("Enter gender (M/F): ")
        
    #if you pick Maine
    elif which_state == 2:
        inputFileName = "STATE/ME.TXT"
        gender = input("Enter gender (M/F): ")
        while gender not in ['M', 'F']:
            print("Invalid choice.")
            gender = input("Enter gender (M/F): ")
    else: 
        print("\nInvalid choice.")
        which_state = int(input("Would you like to view Hawaii (1) or Maine (2)? " ))

    # MENU
    while True:
        menu_choice = int(input("""\nHere is the menu:
        1. View popularity of a name over X years (ie 1970-2000 popularity of name x)
        2. View most popular names for all years
        3. View most popular names for one year
        4. View top 5 longest names
        5. Search name origin
        6. Exit
        Enter your choice: """))

        # reading the file
        with open(inputFileName, 'r') as input_file:
            # removing whitespaces
            lines = []
            for line in input_file:
                line = line.strip()
                if line:
                    lines.append(line)

        # View popularity of a name over X years
        if (menu_choice == 1):
            name = input("Enter a name: ")
            year_low = int(input("Enter the starting year: "))
            if year_low < 1910:
                print("Invalid year.")
                year_low = int(input("Enter the starting year: "))
            year_high = int(input("Enter the ending year: "))
            if year_high>2021:
                print("Invalid year.")
                year_high = int(input("Enter the ending year: "))

            if year_high<=year_low:
                print("Ending year must be higher than starting year.")
                year_low = int(input("Enter the starting year: "))
                year_high = int(input("Enter the ending year: "))

            ranks = []
            years = []

            # populating df
            for line in lines:
                row = line.split(',')
                if int(int(row[2]) >= year_low and int(row[2]) <= year_high) and row[3].strip() == name:
                    if (gender and gender != row[1]):
                        continue
                    gender = row[1]
                    years.append(int(row[2].strip()))
                    ranks.append(int(row[4]))

            if True:
                people = {'Year': years, 'Rank': ranks}
                people_df = pd.DataFrame(people)

                # sorting names
                people_df.sort_values(["Year", "Rank"], axis=0, ascending=[
                    True, True], inplace=True)

                ranked_people_df = people_df
                if(len(ranked_people_df)>0):
                    print("Here are the years", name ,"appeared in")
                    print(ranked_people_df.to_string(index=False))

                    # printing the graph
                    show_graph = input("Would you like to see the graph for this data? (y/n): ")
                    if show_graph == 'y':
                        plt.plot(ranked_people_df['Year'], ranked_people_df['Rank'])
                        plt.title(f"Popularity of {name} from {year_low} to {year_high}")
                        plt.xlabel('Year')
                        plt.ylabel('Number')
                        plt.show()

                    # writing to text file
                    save_file = input("Would you like to save this data? (y/n): ")
                    if save_file == 'y':
                        outputFileNameBase = input("Enter output file name: ")
                        outputFolder = "totalBased/"
                        if not os.path.exists(outputFolder):
                            os.makedirs(outputFolder)
                        outputFileName = outputFolder + outputFileNameBase + ".txt"
                        with open(outputFileName, 'w') as output_file:
                            output_file.write(name+'\n')
                            output_file.write('Year,Rank\n\n')
                            for row in ranked_people_df.itertuples(index=False):
                                output_file.write(','.join(map(str, row)) + '\n')
                else:
                    print("There is no data for this name in this timeframe.")

        # View most popular names for all years          
        elif (menu_choice == 2):
            most_popular_for_year = {}  # year: ('name',score) .. tuple
            for line in lines:
                row = line.split(',')
                name = row[3]
                year = int(row[2])
                rank = int(row[4])
                if (row[1] != gender):
                    continue
                if (row[2] in most_popular_for_year):
                    if (rank >= most_popular_for_year[row[2]][1]):
                        if (rank > most_popular_for_year[row[2]][1]):
                            most_popular_for_year[row[2]] = (row[3], rank)
                        elif (name < most_popular_for_year[row[2]][0]):
                            most_popular_for_year[row[2]] = (row[3], rank)
                else:
                    most_popular_for_year[row[2]] = (row[3], rank)
            
            #populating df
            years = most_popular_for_year.keys()
            names = [i[0] for i in most_popular_for_year.values()]
            people = {'Year': years, 'Name': names}
            people_df = pd.DataFrame(people)
            ranked_people_df = people_df

            # sorting names
            people_df.sort_values(["Year", "Name"], axis=0, ascending=[
                True, True], inplace=True)
            print(ranked_people_df.to_string(index=False))
            
            # writing to text file
            save_file = input("Would you like to save this data? (y/n): ")
            if save_file == 'y':
                outputFileNameBase = input("Enter output file name: ")
                outputFolder = "totalBased/"
                if not os.path.exists(outputFolder):
                    os.makedirs(outputFolder)
                outputFileName = outputFolder + outputFileNameBase + ".txt"
                with open(outputFileName, 'w') as output_file:
                    output_file.write('Year,Name\n\n')
                    for row in ranked_people_df.itertuples(index=False):
                        output_file.write(','.join(map(str, row)) + '\n')

        # View most popular names for one year
        elif (menu_choice == 3):
            year = int(input("Enter a year: "))
            # initializing lists
            names = []
            numbers = []
            ranks = []
            total = 0

            for line in lines:
                row = line.split(',')
                if int(row[2]) == year:
                    if gender and gender != row[1]:
                        continue
                    if row[1] not in ['M', 'F']:
                        continue
                    gender = row[1]
                    temp_name = row[3].strip()
                    names.append(temp_name)
                    numbers.append(int(row[4]))
                    total += 1
                    ranks.append(total)

            if total > 0:
                people = {'Name': names, 'Number': numbers}
                people_df = pd.DataFrame(people)

                # sorting names
                people_df.sort_values(["Number", "Name"], axis=0, ascending=[
                    False, True], inplace=True)

                ranked_people_df = people_df.assign(Rank=ranks).head(100)
                print(ranked_people_df.to_string(index=False))

            # visualizing data
            show_graph = input("Would you like to see the graph for this data (top 10 names)? (y/n): ")
            if show_graph == 'y':
                top10_df = ranked_people_df[:10]

                plt.bar(top10_df['Name'], top10_df['Number'], color = 'tomato')
                plt.xlabel('Name')
                plt.ylabel('Number')
                plt.title('Top 10 most popular names in ' + str(year))

                plt.show()

            # writing to text file
            save_file = input("Would you like to save this data? (y/n): ")
            if save_file == 'y':
                outputFileNameBase = input("Enter output file name: ")
                outputFolder = "yearBased/"
                if not os.path.exists(outputFolder):
                    os.makedirs(outputFolder)
                outputFileName = outputFolder + outputFileNameBase + ".txt"
                with open(outputFileName, 'w') as output_file:
                    output_file.write('Year,Name\n\n')
                    for row in ranked_people_df.itertuples(index=False):
                        output_file.write(','.join(map(str, row)) + '\n')

        # View top 5 longest names
        elif(menu_choice == 4):
            names = []
            with open(inputFileName, 'r') as input_file:
                # extracting names from file
                for line in input_file:
                    row = line.split(',')
                    if gender and gender != row[1]:
                        continue
                    if row[1] not in ['M', 'F']:
                        continue
                    temp_name = (row[3].strip())
                    if temp_name not in names:
                        names.append(temp_name)

            longest_names = sorted(names, key=len, reverse=True)[:5]
            print("\nHere are the top 5 longest names for this state from 1910-2021:")
            for i, name in enumerate(longest_names, start=1):
                print(f"{i}. {name}")

            # writing to text file
            save_file = input("Would you like to save this data? (y/n): ")
            if save_file == 'y':
                outputFileNameBase = input("Enter output file name: ")
                outputFolder = "nameBased/"
                if not os.path.exists(outputFolder):
                    os.makedirs(outputFolder)
                outputFileName = outputFolder + outputFileNameBase + ".txt"
                with open(outputFileName, 'w') as output_file:
                    output_file.write('Top 5 Longest Names\n\n')
                    for i, row in enumerate(longest_names):
                        output_file.write(f"{i+1}. {row}\n")

        # Search name origin
        elif(menu_choice == 5):
             # populate names list
            with open(inputFileName, 'r') as input_file:
                # removing whitespaces
                lines = []
                for line in input_file:
                    line = line.strip()
                    if line:
                        lines.append(line)

            # initializing lists
            names = []
            # extracting names from file
            for line in lines:
                row = line.split(',')
                if gender and gender != row[1]:
                    continue
                if row[1] not in ['M', 'F']:
                    continue
                temp_name = (row[3].strip()).lower()
                names.append(temp_name)

            name_found = False
            name = input("Enter a name to search: ").lower()

            # use sequencematcher to find similar names
            match_ratio = 0.6
            similar_names = []
            for temp_name in names:
                # compare names using sequencematcher, if match ratio is greater than or equal to 0.6 add to similar_names
                if difflib.SequenceMatcher(None, temp_name, name).ratio() >= match_ratio:
                    similar_names.append(temp_name)

            if len(similar_names) == 0:
                print("Name not found.")
            else:
                for temp_name in similar_names:
                    with open('ORIGIN.txt', 'r') as origin_file:
                        for line in origin_file:
                            if temp_name == line.strip().split(',')[0].lower():
                                row_origin = line.strip().split(',')
                                print("Origin found for name:", temp_name.capitalize())
                                print("Origin:", row_origin[1],",",row_origin[2])
                                name_found = True
                                break
                        if name_found:
                            break
                if not name_found:
                    print("Origin not found for any similar names.")

        # Exit
        elif (menu_choice == 6):
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main(sys.argv[1:])
