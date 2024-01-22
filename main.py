from bs4 import BeautifulSoup
import requests
from degreescraper import get_courses, get_all_programs, \
    get_concentrations, get_total_credit_hours, \
    get_bachelors_programs, get_masters_programs, \
    get_minors_programs, get_doctoral_programs

get_courses("Computer Engineering", "BS", "Cybersecurity and Devices")