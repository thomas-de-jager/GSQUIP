# Google search query uniqueness identifier program (GSQUIP)
# Program needs Google search urls to search queries of Google or Google Scholar and finds the uniqueness of each search query (which is a percantage of the search results in the search query that is unique with respect to the search terms of the other search queries)
# Program can be especially useful for A) finding the effectiveness of search terms in a literature review (finding the percentage of unique search results) and B) can save a lot of time, because you can see beforehand if there are many duplicates in your search results with respect to your previous results, so you don't have to go through them by hand

# Working version 0.1: program is not optimal (can be improved a lot, especially efficiency/speed) and might result in a Captcha questionnaire by Google if pages are reloaded to much, too fast and too often (but it works). This wil disappear in a couple of hours. Using a VPN connection will help, but doesn't eliminate the problem. No precoutions were taken to avoid Chrome from detecting Selenium and avoiding the Captchas

# Please make sure you don't have any files with the following naming conventions in your current folder: search_query_xx.txt since they will be overwritten or the program wil use the previous results as well

# Program only works properly if Google language setting is set to English or Dutch.

# Tested with python version 3.6
# Windows 10 Home edition
# Check Chrome version, tested succesfully with Chrome 83
# https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have

# Download driver in section 1.3:
# https://selenium-python.readthedocs.io/installation.html (needs to be in same folder)
# Is already included seperately with the .exe file, so you don't have to do that again

# Reference for how to use Selenium in this code:
# https://www.youtube.com/watch?v=xJxD6ltJLlQ

# Made by TdJ 09/08/2020

# TODO: add "Page 17 of about 241 results (0,04 sec)" functionality so that you can start your webscraping at a specific page. --> add 'page .. of about' functionality in get_total_pages() and update max pages every page refresh, so that you never get the error that the next page button doesn't exist

# TODO: als minder pagina's dan specified, stop programma. --> adjust try except, set boolean correctly using global statement, just like done with previous local variable
# TODO: include: are you already experiencing the captcha questionnaire question

# Import necessary libraries
from selenium import webdriver  # used to automate webscraping via browser
from time import sleep  # used to keep track of time between page refreshes
from selenium.webdriver.common.keys import Keys  # used to open and close new tabs by sending ctrl-t and ctrl-w commands
from random import random  # used to randomize the time in between page refreshes
from math import ceil
from os import system  # used for file/folder handling
from os import path
from os import makedirs
from os import listdir

# Introduction
system('cls')
print("Welcome to the Google Search Query Uniqueness Identifier Program (GSQUIP)!")
print("\nThis program helps you with A) finding the effectiveness of search terms in a literature review and B) managing your time, because you can see beforehand if there are many duplicates in your search query with respect to your previous results.")

search_queries = []  # list with all Google search urls
program_type = 0  # which program should be run (1=webscraping, 2=data crunching, 3=both)
max_pages = -1  # max amount of pages to analyze
time_between_refresh = -1  # time in between page refreshes, set to negative to initialise and use in if>=0 statement
amount_of_search_queries = 0  # number of search queries that is being iterated over
new_file_boolean = True  # used to indicate if a new file should be made or not
# global file_number_extra  # ==============>>> klopt niet.. error dat het een local variabele is. overschrijft telkens de eerste search query file..
file_number_extra = 0
list_of_doubles = []

# Get user input
while True:
    try:
        while (program_type <= 0 or program_type > 3):
            program_type = int(input("\nWould you like to: 1) extract data from Google search query and write to file, 2) files already exist and only compute uniqueness or 3) do both and run full program? (NOTE: don't add any files other than .txt to search queries folder): "))
            if (program_type <= 0 or program_type > 3):
                print("Please insert 1, 2 or 3.")

    except ValueError:
        print("Please insert an integer and press <enter>")
    else:
        break
if program_type == 1 or program_type == 3:
    while True:
        try:
            while not (max_pages >= 0):
                max_pages = int(input("\nSelect maximum amount (integer) of page refreshes per search query (default: 3): "))
                if not (max_pages >= 0):
                    print("Please insert number bigger than or equal to 0.")
        except ValueError:
            print("Please insert an integer and press <enter>")
        else:
            break
    while True:
        try:
            while not (time_between_refresh >= 0):
                time_between_refresh = float(input("\nSelect approximated time (sec) in between page refreshes, to avoid getting the CAPTCHA questionnaire by Google (default: 1): "))
                if not (time_between_refresh >= 0):
                    print("Please insert number bigger or equal to 0.")
        except ValueError:
            print("Please insert a float and press <enter>")
        else:
            break
    while True:
        try:
            while not amount_of_search_queries >= 1:
                amount_of_search_queries = int(input("\nHow many search queries do you have? "))
                if not (amount_of_search_queries >= 1):
                    print("Please insert number bigger or equal to 1.")
        except ValueError:
            print("Please insert an integer and press <enter>")
        else:
            break
    for i in range(amount_of_search_queries):
        while True:
            try:
                search_queries.append(str(input("\nPlease insert Google search url {}: ".format(i+1))))
            except ValueError:
                print("Please insert a url and press <enter>")
            else:
                break

# Initialise constants and variables by default
if program_type == 1 or program_type == 3:
    chrome_options = webdriver.ChromeOptions() # initialize the web driver
    chrome_options.add_argument("start-maximized") # start screen maximazed
    chrome_options.add_argument('disable-infobars') # hide automated software message from Chromium (not working atm)
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")  # relative path of Selenium webdriver (initialise browser object)
    search_query_number = 0 # current search query being analyzed (also used for naming)


def get_new_search_query_number():
    return search_query_number + 1 # increase search query number

# Function to get total amount of search results and devide it by the amount of headers on the page to get total amount of pages
def get_total_pages():
    temp_total_pages = browser.find_element_by_id('gs_ab_md').find_element_by_class_name('gs_ab_mdw').text

    if (temp_total_pages.split()[0] == "About" or temp_total_pages.split()[0] == "Ongeveer"):
        tempAmountOfPages = temp_total_pages.split()[1].split(".")
    else:
        tempAmountOfPages = temp_total_pages.split()[0].split(".")

    newAmountOfPages = "".join(tempAmountOfPages)
    newIntAmountOfPages = int(newAmountOfPages)
    # print("Amount of pages analysed: ", ceil(int((newIntAmountOfPages-(newIntAmountOfPages%10))/10+1)))
    return ceil(int((newIntAmountOfPages-(newIntAmountOfPages%10))/10+1))


# Check if current page is not exceeding the total amount of pages
def not_last_page(current_page, total_pages):
    return current_page <= total_pages

# Check if current page is nog exceeding maximum amount of pages specified by the user
def not_max_page(current_page):
    return current_page <= max_pages - 1

# Get the number of the next page
def get_next_page(current_page):
    return current_page + 1

# Reset the current page (after a new tab is opened for example)
def get_reset_current_page():
    return 0

# Obtain all titles/headlines on the page
def get_headers_on_page():
    return browser.find_elements_by_tag_name('h3')

# Write titles to file and remove [pdf], [html] tags etc.
def check_titles_and_write_to_file(titles, new_file_boolean):
    global file_number_extra
    # print("file number extra = ", file_number_extra)

    if not path.exists('search_queries'):
        makedirs('search_queries')

    # file_number_extra = 0  # used to keep track of how many .txt files are already existant
    if new_file_boolean == True:
        # print("new page")
        temp_file_number_extra = 0
        while (path.isfile("search_queries\\search_query_" + str(search_query_number + temp_file_number_extra) +".txt")):
            temp_file_number_extra = temp_file_number_extra + 1
            # print(" ", temp_file_number_extra)
        file_number_extra = temp_file_number_extra
        # print("Dit moet 3 zijn: ", file_number_extra)

    # print("search_queries\\search_query_" + str(search_query_number + file_number_extra) +".txt")
    # print(search_query_number, temp_file_number_extra)
    # print("\n")
    file = open("search_queries\\search_query_" + str(search_query_number + file_number_extra) +".txt", "a", encoding="utf-8")

    for title in titles:
        title_first_word = title.text.split(' ', 1)[0]
        if title_first_word == "[PDF]" or title_first_word == "[HTML]" or title_first_word == "[CITATION]" or title_first_word == "[BOOK]":
            file.write(title.text.split(' ', 1)[1] + "\n")
        else:
            file.write(title.text + "\n")
        # print(title.text)
    file.close()

# Click on next page
def go_to_next_page():
    try:
        browser.find_element_by_tag_name('tbody').find_element_by_link_text(str(current_page+1)).click()
        return False
    except:
        return True

# Return a list of booleans containing information if the lines in the file is unique or not (compares two files)
def get_file_uniqueness(lines1, lines2, file1_length, file2_length):
    def_temp_list_of_line_uniqueness = []
    item_appended = False

    for line_number1 in range(file1_length):
        for line_number2 in range(file2_length):
            if lines1[line_number1] == lines2[line_number2]:
                def_temp_list_of_line_uniqueness.append(0)
                item_appended = True
                break
        if not item_appended:
            def_temp_list_of_line_uniqueness.append(1)
            item_appended = False
        else:
            item_appended = False

    return def_temp_list_of_line_uniqueness

# Count the number of unique lines in a list of line uniqueness (containing booleans) and return this number
def get_number_of_unique_lines(def_temp_list_of_line_uniqueness):
    number_of_unique_lines = 0
    for line in def_temp_list_of_line_uniqueness:
        if line == 1:
            number_of_unique_lines += 1
    return number_of_unique_lines

# Calculate the percentage of unique lines, as a function of the total amount of lines in all files (=total_file_length) and the amount of unique lines (int)
def get_fraction_of_unique_lines(number_of_unique_lines, total_file_length):
    return [number / total_file_length for number in number_of_unique_lines]

# get fraction of unique lines with respect to total amount of search results
def get_percentage_of_unique_lines(number_of_unique_lines, file_lengths):
    # return [number / total_search_results for number in number_of_unique_lines]
    return [number / length for (number,length) in zip(number_of_unique_lines, file_lengths)]

def get_list_percentages_of_doubles(list_of_doubles, file_lengths):
    # return [number / total_search_results for number in number_of_unique_lines]
    return [number / length for (number,length) in zip(list_of_doubles, file_lengths)]

def get_reset_new_file_boolean():
    return False

# Code
# For every search query open the page in the browser (as a new tab) and receive all the titles. Refreses take place at randomized time intervals
if program_type == 1 or program_type == 3:
    for search_query in search_queries:
        search_query_number = get_new_search_query_number() # increase query number, used for naming files and indexing
        current_page = get_reset_current_page() # set the current page to 0 every time a new tab is opened

        if search_query_number == 1:
            browser.get(search_query) # open url in current window if its the first url, else open in new tab and focus on that tab

            # Only use this if you have captcha
            input("\nPress enter to continue.")

            # new_file_boolean = False
        else:
            browser.execute_script("window.open('');") # open new tab
            new_file_boolean = True  # indicate that a new file should be made
            # print("new_file_boolean set to true")
            browser.switch_to.window(browser.window_handles[search_query_number-1]) # change active tab
            browser.get(search_query) # open url in new tab

        total_pages = get_total_pages() # get the amount of pages for this search query and update the total amount of pages accordingly

        # The main loop runs until limitations are reached
        not_started_at_first_page = False
        while not_last_page(current_page, total_pages) and not_max_page(current_page) and not not_started_at_first_page:
            current_page = get_next_page(current_page)
            titles = get_headers_on_page()
            check_titles_and_write_to_file(titles, new_file_boolean)
            # print("Dit moet 3 zijn: ", file_number_extra)
            new_file_boolean = get_reset_new_file_boolean()  # next time don't make new file
            sleep(time_between_refresh + ((time_between_refresh*random())*pow((-1),(round(random()))))/2);
            not_started_at_first_page = go_to_next_page() # go to next page of same search query

    browser.quit() # close the browser

# Interpret data, no browser or online data needed anymore
if program_type == 2 or program_type == 3:
    total_file_length = 0 # amount of lines in all files containing headlines/titles
    file_lengths = [] # list containing all file lengths
    list_of_line_uniquenesses = [] # list containing amount of unique titles

    # open every file and save content as variable and calculate length for text_file_number in range(len(search_queries)):
    DIR = "search_queries"
    amount_of_text_files = len([name for name in listdir(DIR) if path.isfile(path.join(DIR, name))])
    for text_file_number in range(amount_of_text_files):
        file1 = open(DIR + "\\search_query_" + str(text_file_number+1) +".txt", "r", encoding="utf-8")
        lines1 = file1.readlines()

        file1.close()
        file1_length = len(lines1)
        file_lengths.append(file1_length)
        total_file_length += file1_length

        # Check for the amount of double search results in each article
        boolean_list_of_all_doubles = []
        list_of_doubles.append(0)
        current_line_number = 0
        appended = False
        for current_line in lines1:
            current_line_number += 1
            comparison_line_number = 0
            for comparison_line in lines1:
                comparison_line_number += 1
                # print(current_line_number, comparison_line_number)
                # print(current_line, comparison_line)
                # print("\n")
                if current_line_number != comparison_line_number and current_line == comparison_line:
                    list_of_doubles[text_file_number] += 1
                    appended = True
                    break
                else:
                    appended = False

            if appended:
                boolean_list_of_all_doubles.append(1)
            else:
                boolean_list_of_all_doubles.append(0)

        # print("this is a test", boolean_list_of_all_doubles)  # prints listst for each file, with the locations of the double search terms

        # initialize some variables
        temp_list_of_line_uniqueness = [] # used to temporarily save the line uniqueness booleans
        list_of_line_uniqueness = [] # list of all line uniqueness booleans

        # select the 2nd file which has to be compared to the first one for uniqueness of search terms. This wraps back to the first search query if index is exceeding the amount of search queries
        for i in range(amount_of_text_files-1):
            # compare_text_file_number = (text_file_number+i+1)%len(search_queries)+1
            compare_text_file_number = (text_file_number+i+1)%amount_of_text_files+1
            file2 = open("search_queries\\search_query_" + str(compare_text_file_number) +".txt", "r", encoding="utf-8")
            lines2 = file2.readlines()

            file2.close()

            file2_length = len(lines2) # amount of search results in file 2

            temp_list_of_line_uniqueness.append(get_file_uniqueness(lines1, lines2, file1_length, file2_length))  # keeps expanding. is a list of lists with line uniquenesses of current file with respect to the other files

        #     print(text_file_number+1, compare_text_file_number)  # handy print statements
        #     print(temp_list_of_line_uniqueness)
        # print("\n")

        # combine all lists of uniquenesses into one, so if a search term is unique in one file, but not compared to another, the search term is therefore marked as not unique. Only after the search term of the file in question is compared to all other files and the search term passes (= 1) all comparisons, the search term is marked as unique (=1)
        if len(temp_list_of_line_uniqueness) == 1:
            list_of_line_uniqueness = temp_list_of_line_uniqueness[0]  # 'final' list with uniqueness of each line in the current file
        else:
            temp_list_of_line_uniqueness.append(get_file_uniqueness(lines1, lines2, file1_length, file2_length))
            list_of_line_uniqueness = list(map(min, zip(*temp_list_of_line_uniqueness)))  # using lambda function map to obtain the element wise minimum of the lists of lists

        # print(list_of_line_uniqueness)  # handy print statements
        # print("\n")

        list_of_line_uniquenesses.append(list_of_line_uniqueness)

    # Add the amount of unique titles per search query to a list
    number_of_unique_lines = []
    for item in list_of_line_uniquenesses:
        number_of_unique_lines.append(get_number_of_unique_lines(item))

    list_percentages_of_doubles = get_list_percentages_of_doubles(list_of_doubles, file_lengths)
    percentage_of_unique_lines = get_percentage_of_unique_lines(number_of_unique_lines, file_lengths)
    fraction_of_unique_lines = get_fraction_of_unique_lines(number_of_unique_lines, total_file_length) # get fraction of unique lines with respect to total amount of search results


    # Display results
    print("\n===== RESULTS =====")
    print("Amount of search queries: ", len(search_queries))
    print("Amount of search results: ", total_file_length)
    print("\nDistribution of search results per search query: ", file_lengths)
    print("Amount of unique search results per search query: ", number_of_unique_lines)
    print("Fraction of unique search results per search query: ", [round(num, 2) for num in percentage_of_unique_lines])
    print("Amount of double search results per search query: ", list_of_doubles)
    print("Fraction of double search results per search query: ", [round(num, 2) for num in list_percentages_of_doubles])
    print("Average fraction of unique search results per search query: ", round(sum(percentage_of_unique_lines)/len(percentage_of_unique_lines), 2))
    print("Fraction of unique search results with respect to the total amount search results: ", [round(num, 2) for num in fraction_of_unique_lines])
    # print("\nA list containing the uniquenesses of all search terms ordered per file (e.g. search_query_xx.txt) with search results (1 = search term unique, 0 = not unique): ", list_of_line_uniquenesses)

    input("\nAll titles scraped from the search queries are listed in files search_query_xx.txt. Please don't forget to copy the results above. Press enter to exit the terminal.")
else:
    input("\nPress enter to exit the terminal.")
