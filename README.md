
# Test Task

The script iterates through the rows of an input.csv, including both Department and Language values, then counts the amount of job listings for the specified filters. These values are then output into another CSV. Feel free to adjust the values in the input.csv, and see how the output.csv changes!



## Process

* Initially, the script was less modular, so I broke it down into rudimentary functions.
* Used implicit waits and time.sleep() for the ease of testing, obviously replaced by WebDriverWait
* I had some trouble with Departments which had no vacancies and were therefore unclickable (such as Finance and Purchasing) . The workaround was to catch the _ElementClickInterceptedException_ in the try-except.
* In the future, less full xpath expressions are key. I should strive to use more future-proof locators.
