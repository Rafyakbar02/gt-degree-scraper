from bs4 import BeautifulSoup
import requests


masters = ["MS", "PMASE", "M.Arch", "MBID", "MBA", "MCRP", "M.ID", "PMML", "MS (undesignated)", "PMOSH", "MRED",
           "PMSEE", "MSEEM"]


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

        college_degrees = []

        for a in li.find_all("a"):
            course_level = a.text
            # link = a.get('href')[10:]
            # college_level[course_level] = url + link
            college_degrees.append(course_level)

        programs[major] = college_degrees

    return programs


def get_courses(program, degree):
    programs = get_all_programs()

    if program not in programs.keys():
        print("Program not found")
        return

    if degree not in programs[program]:
        print("Degree of program not found")
        return

    url = "https://catalog.gatech.edu/programs/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    if degree == "BS":
        div = soup.find(id="bachelorstextcontainer")
    elif degree in masters:
        div = soup.find(id="masterstextcontainer")
    elif degree == "PhD":
        div = soup.find(id="doctoraltextcontainer")
    else:
        print("Not supported yet")
        return

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        if curr_link[:end] == program:
            url += li.a['href'][10:]
            break

    if not simple_degree(url):
        print("Not implemented")
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tbody = soup.find('tbody')

    courses = []

    for tr in tbody.find_all('tr'):
        if 'areaheader' in tr['class']:
            continue

        course_code = tr.find('a')

        if course_code is None:
            continue

        courses.append(course_code.text.replace("\xa0", " "))

    return courses


def simple_degree(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    if soup.find(id="requirementstextcontainer") is None:
        return False
    else:
        return True
    
    
def get_bachelors_programs():
    url = "https://catalog.gatech.edu/programs/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="bachelorstextcontainer")

    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    print(programs)


def get_masters_programs():
    url = "https://catalog.gatech.edu/programs/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="masterstextcontainer")

    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    print(programs)

    
def get_doctoral_programs():
    url = "https://catalog.gatech.edu/programs/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="doctoraltextcontainer")

    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    print(programs)


def get_minors_programs():
    url = "https://catalog.gatech.edu/programs/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="minorstextcontainer")

    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    print(programs)


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


print(get_courses("Architecture", "BS"))