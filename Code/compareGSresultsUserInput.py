# Google search query uniqueness identifier program (GSQUIP)
# Program needs Google search urls to search queries of Google or Google Scholar and finds the uniqueness of each search query (which is a percantage of the search results in the search query that is unique with respect to the search terms of the other search queries)
# Program can be especially useful for A) finding the effectiveness of search terms in a literature review (finding the percentage of unique search results) and B) can save a lot of time, because you can see beforehand if there are many duplicates in your search results with respect to your previous results, so you don't have to go through them by hand

# Working version 0.1: program is not optimal (can be improved a lot, especially efficiency/speed) and might result in a Captcha questionnaire by Google if pages are reloaded to much, too fast and too often (but it works). This wil disappear in a couple of hours. Using a VPN connection will help, but doesn't eliminate the problem. No precoutions were taken to avoid Chrome from detecting Selenium and avoiding the Captchas

# Please make sure you don't have any files with the following naming conventions in your current folder: search_query_xx.txt since they will be overwritten or the program wil use the previous results as well

# Tested with python version 3.6
# Windows 10 Home edition
# Check Chrome version, tested succesfully with Chrome 83
# https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have

# Download driver in section 1.3:
# https://selenium-python.readthedocs.io/installation.html (needs to be in same folder)
# Is already included seperately with the .exe file, so you don't have to do that again

# Reference for how to use Selenium in this code:
# https://www.youtube.com/watch?v=xJxD6ltJLlQ

# Made by TdJ 20/07/2020

# Import necessary libraries
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from random import random
from math import ceil
from os import system

system('cls')
print("Welcome to the Google Search Query Uniqueness Identifier Program (GSQUIP)!")
print("\nThis program helps you with A) finding the effectiveness of search terms in a literature review and B) managing your time, because you can see beforehand if there are many duplicates in your search query with respect to your previous results.")

search_queries = []
while True:
    try:
        max_pages = int(input("\nSelect maximum amount (integer) of page refreshes per search query (default: 3): "))
    except ValueError:
        print("Please insert an integer and press <enter>")
    else:
        break
while True:
    try:
        time_between_refresh = float(input("\nSelect approximated time (sec) in between page refreshes, to avoid getting the CAPTCHA questionnaire by Google (default: 1): "))
    except ValueError:
        print("Please insert a float and press <enter>")
    else:
        break
while True:
    try:
        amount_of_search_queries = int(input("\nHow many search queries do you have? "))
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
    # print([int(word) for word in temp_total_pages.split() if word.isdigit()])
    # print(temp_total_pages.split())
    # for word in temp_total_pages.split():
    #     print(word.isdigit())
    # print(len(get_headers_on_page()))
    # print([int(word) for word in temp_total_pages.split() if word.isdigit()][0])

    tempAmountOfPages = temp_total_pages.split()[1].split(".")
    newAmountOfPages = "".join(tempAmountOfPages)
    return ceil(int(newAmountOfPages))
    # return ceil([int(word) for word in temp_total_pages.split() if word.isdigit()][0]/len(get_headers_on_page()))

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

# Write titles to file and remove pdf, html tags etc.
def check_titles_and_write_to_file():
    file = open("search_query_" + str(search_query_number) +".txt", "a", encoding="utf-8")
    for title in titles:
        if title.text.split(' ', 1)[0] == "[PDF]" or title.text.split(' ', 1)[0] == "[HTML]" or title.text.split(' ', 1)[0] == "[CITATION]":
            file.write(title.text.split(' ', 1)[1] + "\n")
        else:
            file.write(title.text + "\n")
    file.close()

# Click on next page
def go_to_next_page():
    browser.find_element_by_tag_name('tbody').find_element_by_link_text(str(current_page+1)).click()

# Return a list of booleans containing information if the lines in the file is unique or not (compares two files)
def get_file_uniqueness(lines1, lines2, file1_length, file2_length):
    list_of_line_uniqueness = []
    item_appended = False
    for line_number1 in range(file1_length):
        for line_number2 in range(file2_length):
            if lines1[line_number1] == lines2[line_number2]:
                list_of_line_uniqueness.append(0)
                item_appended = True
                break
        if not item_appended:
            list_of_line_uniqueness.append(1)
            item_appended = False
        else:
            item_appended = False
    return list_of_line_uniqueness

# Count the number of unique lines in a list of line uniqueness (containing booleans) and return this number
def get_number_of_unique_lines(list_of_line_uniqueness):
    number_of_unique_lines = 0
    for line in list_of_line_uniqueness:
        if line == 1:
            number_of_unique_lines += 1
    return number_of_unique_lines

# Calculate the percentage of unique lines, as a function of the total amount of lines in all files (=total_file_length) and the amount of unique lines (int)
def get_percentage_of_unique_lines(number_of_unique_lines, total_file_length):
    return [number / total_file_length for number in number_of_unique_lines]

# Code
# For every search query open the page in the browser (as a new tab) and receive all the titles. Refreses take place at randomized time intervals
for search_query in search_queries:
    search_query_number = get_new_search_query_number() # increase query number, used for naming files and indexing
    current_page = get_reset_current_page() # set the current page to 0 every time a new tab is opened

    if search_query_number == 1:
        browser.get(search_query) # open url in current window if its the first url, else open in new tab and focus on that tab
    else:
        browser.execute_script("window.open('');") # open new tab
        browser.switch_to.window(browser.window_handles[search_query_number-1]) # change active tab
        browser.get(search_query) # open url in new tab

    total_pages = get_total_pages() # get the amount of pages for this search query and update the total amount of pages accordingly

    # The main loop runs until limitations are reached
    while not_last_page(current_page, total_pages) and not_max_page(current_page):
        current_page = get_next_page(current_page)
        titles = get_headers_on_page()
        check_titles_and_write_to_file()
        sleep(time_between_refresh + random());
        go_to_next_page() # go to next page of same search query

browser.quit() # close the browser

# Interpret data, no browser or online data needed anymore
total_file_length = 0 # amount of lines in all files containing headlines/titles
file_lengths = [] # list containing all file lengths
list_of_line_uniquenesses = [] # list containing amount of unique titles

# open every file and save content as variable and calculate length
for text_file_number in range(len(search_queries)):
    file1 = open("search_query_" + str(text_file_number+1) +".txt", "r")
    lines1 = file1.readlines()
    file1.close()
    file1_length = len(lines1)
    file_lengths.append(file1_length)
    total_file_length += file1_length
    # initialize some variables
    temp_list_of_line_uniqueness = [] # used to temporarily save the line uniqueness booleans
    list_of_line_uniqueness = [] # list of all line uniqueness booleans

    # select the 2nd file which has to be compared to the first one for uniqueness of search terms. This wraps back to the first search query if index is exceeding the amount of search queries
    for i in range(len(search_queries)-1):
        compare_text_file_number = (text_file_number+i+1)%len(search_queries)+1
        file2 = open("search_query_" + str(compare_text_file_number) +".txt", "r")
        lines2 = file2.readlines()
        file2.close()

        file2_length = len(lines2) # amount of search results in file 2

        temp_list_of_line_uniqueness.append(get_file_uniqueness(lines1, lines2, file1_length, file2_length))

    # combine all lists of uniquenesses into one, so if a search term is unique in one file, but not compared to another, the search term is therefore marked as not unique. Only after the search term of the file in question is compared to all other files and the search term passes (= 1) all comparisons, the search term is marked as unique (=1)
    if len(temp_list_of_line_uniqueness) == 1:
        list_of_line_uniqueness = temp_list_of_line_uniqueness[0]
    else:
        temp_list_of_line_uniqueness.append(get_file_uniqueness(lines1, lines2, file1_length, file2_length))
        list_of_line_uniqueness = (list(map(min, zip(temp_list_of_line_uniqueness[0], temp_list_of_line_uniqueness[1]))))

    list_of_line_uniquenesses.append(list_of_line_uniqueness)

# Add the amount of unique titles per search query to a list
number_of_unique_lines = []
for item in list_of_line_uniquenesses:
    number_of_unique_lines.append(get_number_of_unique_lines(item))

percentage_of_unique_lines = get_percentage_of_unique_lines(number_of_unique_lines, total_file_length) # get percentage of unique lines

# Display results
print("\n===== RESULTS =====")
print("Amount of search queries: ", len(search_queries))
print("Amount of search results: ", total_file_length)
print("\nDistribution of search results per search query: ", file_lengths)
print("Amount of unique search results per search query: ", number_of_unique_lines)
print("Percentage of unique search results per search query: ", percentage_of_unique_lines)
print("\nA list containing the uniquenesses of all search terms ordered per file (e.g. search_query_xx.txt) with search results (1 = search term unique, 0 = not unique): ", list_of_line_uniquenesses)

input("\nAll titles scraped from the search queries are listed in files search_query_xx.txt. Please don't forget to copy the results above. Press enter to exit the terminal.")
