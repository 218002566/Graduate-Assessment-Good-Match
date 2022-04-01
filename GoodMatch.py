import csv
import re


def read_csv():  # function reads csv data and returns it via list
    teams_list = []
    with open('Names.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            teams_list.append(row[0]+'#'+row[1])  # appends name and gender separated by "#" to list
    return teams_list


def split_csv(teams_list):  # function splits above list into two lists by gender,cleans text & returns both lists
    m_list = []  # male list
    f_list = []  # female list
    for item in teams_list:  # loops through every name+gender in list
        if re.search('# m', item):  # searches if name is male
            m_list.append(re.sub('# m$', '', item))  # uses regex to replace gender with blank space and adds to m_list
        elif re.search('# f', item):
            f_list.append(re.sub('# f$', '', item))
        else:  # error handles gender if not input as m or f
            while True:  # infinite loop unless valid input is entered
                gender_edit = input("Incorrect Input detected for " + re.sub('#.*$', '', item)
                                    + " Please enter either m or f for gender: ")  # requests correct input for gender
                if gender_edit.lower() == 'f':
                    f_list.append(re.sub('#.*$', '', item))  # replace # and incorrect input with blank space & +list
                    break
                elif gender_edit.lower() == 'm':
                    m_list.append(re.sub('#.*$', '', item))
                    break
                else:  # if correct input is entered, enters m or f list & exits while, else repeats while
                    continue
    return m_list, f_list


def clean_csv(m, f):  # removes remaining non alphabetic text from lists & removes duplicates & returns lists
    if len(m) > len(f):
        longest = m  # finds which list is longer
    else:
        longest = f
    for i in range(len(longest)):  # loops for length of longer list to complete all operations in 1 loop
        if i < len(m):  # affects list that still has index in bounds
            m[i] = re.sub('^[0-9]*.\s*', '', m[i])  # removes the numbering from the names
            while True:   # infinite loop unless valid input is entered
                if is_valid(m[i]) == "false":  # calls a validity check function for correct input
                    name_edit = input(m[i] + " is an invalid input! Only alphabet characters allowed, re-enter name: ")
                    # above requests correct input for name
                    m[i] = name_edit  # list item now equals new input
                    continue  # while starts again to test the new input
                else:
                    break  # exits while when name only contains letters
        if i < len(f):
            f[i] = re.sub('^[0-9]*.\s*', '', f[i])
            while True:
                if is_valid(f[i]) == "false":
                    name_edit = input(f[i] + " is an invalid input! Only alphabet characters allowed, re-enter name: ")
                    f[i] = name_edit
                    continue
                else:
                    break  # validity check for female list
    m = list(dict.fromkeys(m))
    f = list(dict.fromkeys(f))  # removes duplicates via dictionary

    return m, f


def is_valid(names):  # checks if names only have letters and returns true or false

    if re.match('^[a-zA-Z]*$', names):  # checks if name only has alphabetic characters from beginning to end
        valid = "true"
    else:
        valid = "false"

    return valid


def match_sets(m, f):  # pairs all entries in the female list with all entries in the male list separated by 'matches'
    names = []
    for i in f:  # i is name in female list f
        for j in m:  # j is name in male list m
            pair = i + "matches" + j
            names.append(pair)
    return names  # returns list of matched pairs from the two lists


def letter_count(names):  # counts the number of times a letter appears for each matched pair and returns this as a list
    num_group = []
    for item in names:  # loops through matched names in list
        temp_str = ''
        num_letters = []
        for char in item:  # loops through each character in each match within the list
            if char.lower() not in temp_str.lower():  # if the letter not in new temporary string
                num_letters.append(item.lower().count(char.lower()))  # adds num of times its in matched names to num_letters list
                temp_str = temp_str + char.lower()  # adds letter to temp string
        num_group.append(num_letters)  # adds list of numbers of letters to another empty list
    return num_group  # returns list of lists of numbers


def num_reduction(num, match):  # reduces the length of numbers in the lists above and writes results to text file
    file_text = open("output.txt", "a+")  # opens/creates and opens text file for appending
    temp = []
    while len(num) > 0:  # initial cleanup of long number lists
        if len(num) == 1:
            temp.append(num[0])  # if only one number remains add to list and exit while
            break
        add = num[0]+num[-1]  # sums first and last numbers
        if add > 9:  # if summation over 9
            str_temp = str(add)  # sets temp string to sum
            temp.append(int(str_temp[0]))  # adds each digit separately
            temp.append(int(str_temp[1]))
        else:
            temp.append(add)  # adds summation to temp
        num.pop(0)  # removes first digit from num
        num.pop(-1)  # removes last digit from num
    if len(temp) > 2:  # if temp is greater than two then temp needs to be reduced further
        num_reduction(temp, match)  # calls same function within function now with temp as new parameter
    else:
        file_text.write(string_result(match) + " " + percentage_result(temp) + "\n")
        # above calls string_result to clean up match and percentage_result to convert temp list to string
        # and writes the two appended strings to a text file
    file_text.close()


def txt_write(num_c, match):  # calls the num_reduction function for each pair of matched names and num of letters
    for i in range(len(num_c)):
        num_reduction(num_c[i], match[i])


def string_result(string):  # changes name+matches+name  to name +matches+ name and returns it
    pattern = re.compile(r"matches")
    new_str = pattern.sub(" matches ", string)
    return new_str


def percentage_result(string):  # converts final two temp list digits to string and concatenates them + % and returns it
    percentage = ""
    for item in string:
        percentage += str(item)  # concatenates final two ints after converting them to string
    percentage_int = int(percentage)  # converts new combined string to int
    if percentage_int > 79:  # adds good match to returned string if combined num is 80 or higher
        percentage += "%, good match"
    else:
        percentage += "%"
    return percentage


def txt_display():  # orders data in text file & displays it in console & logs all outputs
    name_sort = []
    file_text = open("output.txt", "r")
    log_text = open("log.txt", "a+")
    lines = file_text.readlines()  # reads each line in text file
    print("\n")  # provides space on console after potential inputs due to input errors & final output
    for item in lines:  # loops through each line from text file
        name_sort.append(item) # adds lines to new list
    name_sort.sort(key=lambda x: (-int(x.split()[3][0:1]), x.split()[0], x.split()[2]))
    # above sorts list of lines by reverse order of int(number) percentage, followed by 1st name & then 2nd name
    # eg Jack matches Jill 60% -> (x.split()[0]) matches (x.split()[2]) (-int(x.split()[3][0:1])%
    file_text.close()
    file_text = open("output.txt", "w")  # opens text file to clear unsorted data
    file_text.close()
    file_text = open("output.txt", "a")  # opens text file to append sorted data
    for item in name_sort:  # where item is matched names and percentage
        file_text.write(item)  # writes sorted data to output text file
        log_text.write(item)  # writes sorted data to log text file
        print(item)  # prints sorted data to console
    log_text.write("________________________________________________________________________________________________\n")
    # above separates each execution on the log
    log_text.close()
    file_text.close()


def main():
    file_text = open("output.txt", "w+")  # opens output text file when executed and clears it for operation
    file_text.close()
    m_list, f_list = split_csv(read_csv())  # assigns lists returned lists from split_csv to variables
    m_list, f_list = clean_csv(m_list, f_list)  # assigns edited lists returned from clean_csv to same variables above
    match = match_sets(m_list, f_list)  # uses cleaned lists as parameters for match_sets
    num_c = letter_count(match)  # assigns list of lists of numbers of letters of matched pairs to a variable
    txt_write(num_c, match)  # uses the above variable and match as parameters for txt_write
    txt_display()  # calls the display function


if __name__ == "__main__":
    main()
