from bs4 import BeautifulSoup
import requests
import pandas as pd
from degreescraper import get_courses, get_all_programs, \
    get_concentrations, get_total_credit_hours, \
    get_bachelors_programs, get_masters_programs, get_doctoral_programs, get_degree_overview

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# print(get_all_programs())
# print(get_concentrations("Computer Engineering", "BS"))
# print(get_courses("Industrial Engineering", "BS", "Bachelor of Science in Industrial Engineering - Economic and Financial Systems"))
# print(get_total_credit_hours("Computer Science", "BS", "Intelligence & Devices"))
# print(get_doctoral_programs())
print(get_degree_overview("Civil Engineering", "BS", "Bachelor of Science in Civil Engineering - Construction and Infrastructure Systems Engineering"))