# Graduate-Assessment-Good-Match
Calculates the match percentage between two peoples first names.

GitHub repo link: https://github.com/218002566/Graduate-Assessment-Good-Match.git


log.txt contains all previous outputs of the program

output.txt contains output from last run only

Names.csv was created by copying the list of names and genders in the project's instructions and pasting them into a text file
File extension was then changed to csv

To view output of Names.csv: 
Run GoodMatch.py

To view output of custom csv: 
Copy csv file into the project folder. 
Replace Names.csv with your own csv file name in the code on line 7 of GoodMatch.py. 
Use the code excerpt below  for refernce to find it:

    with open('Names.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            teams_list.append(row[0]+'#'+row[1])  # appends name and gender separated by "#" to list
    return teams_list

Thank you
