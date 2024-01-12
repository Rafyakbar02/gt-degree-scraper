from bs4 import BeautifulSoup
import requests


main_url = "https://catalog.gatech.edu/programs/"
masters = ["MS", "PMASE", "M.Arch", "MBID", "MBA", "MCRP", "M.ID", "PMML", "MS (undesignated)", "PMOSH", "MRED",
           "PMSEE", "MSEEM"]


def get_all_programs():
    page = requests.get(main_url)
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
    url = program_link(program, degree)

    if url is None:
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
    page = requests.get(main_url)
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
    page = requests.get(main_url)
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
    page = requests.get(main_url)
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
    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="minorstextcontainer")

    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    print(programs)


def get_total_credit_hours(program, degree):
    url = program_link(program, degree)

    if url is None:
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tr = soup.find_all('tr', {"class": "listsum"})[0]
    hour = tr.find_all('td')[1].text

    return hour


def program_link(program, degree):
    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, "html.parser")

    if degree == "BS":
        div = soup.find(id="bachelorstextcontainer")
    elif degree in masters:
        div = soup.find(id="masterstextcontainer")
    elif degree == "PhD":
        div = soup.find(id="doctoraltextcontainer")
    else:
        print("Not yet implemented")
        return

    url = main_url

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        if curr_link[:end] == program:
            for a in li.find_all("a"):
                curr_degree = a.text
                if curr_degree == degree:
                    url += a['href'][10:]
                    break

    if url == "https://catalog.gatech.edu/programs/":
        print("Program or degree not found")
        return

    if not simple_degree(url):
        print("Not yet implemented")
        return

    return url