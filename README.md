# Google search query uniqueness identifier program (GSQUIP)
Program needs Google search urls of search queries of Google or Google Scholar and finds the uniqueness of each search query (which is a percantage of the search results in the search query that is unique with respect to the search terms of the other search queries).
Program can be especially useful for A) finding the effectiveness of search terms in a literature review (finding the percentage of unique search results) and B) can save a lot of time, because you can see beforehand if there are many duplicates in your search results with respect to your previous results, so you don't have to go through them by hand. You can directly see if any search term can be eliminated.

Working version 0.1: program is not optimal (can be improved a lot, especially efficiency/speed) and might result in a Captcha questionnaire by Google if pages are reloaded to much, too fast and too often (but it works). This wil disappear in a couple of hours. Using a VPN connection will help, but doesn't eliminate the problem. No precoutions were taken to avoid Chrome from detecting Selenium and avoiding the Captchas

Please make sure you don't have any files with the following naming conventions in your current folder: search_query_xx.txt since they will be overwritten or the program wil use these previous results as well

Tested with python version 3.6
Windows 10 Home edition
Check Chrome version, tested succesfully with Chrome 83
https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have

Download driver in section 1.3:
https://selenium-python.readthedocs.io/installation.html (needs to be in same folder as .py or .exe)
Is already included seperately, so you don't have to do that again

Made by TdJ 20/07/2020


# How to use the program:
Clone/download the repository as a zip file. Extract and run compareGSresultsUserInput.exe in the Executable folder.
Program might not work the first time (due to permissions you have to allow for Windows).
Program should open a terminal, ask a few questions for efficiency and then you can insert your Google Search queries by copy-pasting the url to the terminal, when requested.
