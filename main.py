from bs4 import BeautifulSoup
import requests

def get_all_programs():
    url = "https://catalog.gatech.edu/programs/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="alltextcontainer")

    programs = {}

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]

        college_level = {}

        for a in li.find_all("a"):
            course_level = a.text
            link = a.get('href')[10:]
            college_level[course_level] = url + link

        programs[major] = college_level

    return programs


def get_courses(program, degree):
    if get_offering(program) is None or degree not in get_offering(program):
        print("Not Found")
        return
    
    url = get_offering(program)[degree]

    if not simple_degree(url):
        print("Not implemented")
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tbody = soup.find('tbody')

    for tr in tbody.find_all('tr'):
        if 'areaheader' in tr['class']:
            continue

        course_code = tr.find('a')

        if course_code is None:
            continue

        print(course_code.text)


def simple_degree(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    if soup.find(id="requirementstextcontainer") is None:
        return False
    else:
        return True
    
    
def get_bachelor_programs():
    programs = get_all_programs()

    for major, val in programs.items():
        for college_level in val:
            if college_level == 'BS':
                print(major)


def get_master_programs():
    programs = get_all_programs()

    for major, val in programs.items():
        for college_level in val:
            if college_level in get_masters_degree_type():
                print(major)


def get_masters_degree_type():
    url = "https://catalog.gatech.edu/programs/#masterstext"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    degree_type = []

    for li in soup.find(id="masterstextcontainer").find_all("li"):
        degree_type.append(li.find('a').text)

    return set(degree_type)

    
def get_doctor_programs():
    programs = get_all_programs()

    for major, val in programs.items():
        for college_level in val:
            if college_level == 'PhD':
                print(major)


def get_offering(program):
    programs_dict = get_all_programs()
    
    if program not in programs_dict:
        return None

    return programs_dict[program]


def get_total_credit_hours(program, degree):
    if get_offering(program) is None or degree not in get_offering(program):
        print("Not Found")
        return
    
    url = get_offering(program)[degree]

    if not simple_degree(url):
        print("Not implemented")
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tr = soup.find_all('tr', {"class": "listsum"})[0]
    hour = tr.find_all('td')[1].text
    print(hour, "credit hours")
