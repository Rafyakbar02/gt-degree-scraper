from bs4 import BeautifulSoup
import requests


main_url = "https://catalog.gatech.edu/programs/"
masters = ["MS", "PMASE", "M.Arch", "MBID", "MBA", "MCRP", "M.ID", "PMML", "MS (undesignated)", "PMOSH", "MRED",
           "PMSEE", "MSEEM"]


def get_all_programs():
    """
    Get list of all programs currently offered in Georgia Institute of Technology

    :returns: dictionary of program with the value of a list of available degrees
    """

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
            college_degrees.append(course_level)

        programs[major] = college_degrees

    return programs


def get_concentrations(program, degree):
    """
    Get list of concentrations/threads within the program and degree pair

    :param program: program name
    :param degree: degree name
    :return: list of concentrations
    """
    url = program_link(program, degree)

    if url is None:
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    div = None

    if soup.find(id="concentrationstextcontainer"):
        div = soup.find(id="concentrationstextcontainer")
    elif soup.find(id="standardandconcentrationoptiontextcontainer"):
        div = soup.find(id="standardandconcentrationoptiontextcontainer")
    elif soup.find(id="threadstextcontainer"):
        div = soup.find(id="threadstextcontainer")
    else:
        print("Program and degree pair doesn't have concentrations/threads")
        return

    concentrations = []

    for a in div.find_all("a"):
        if a.text == "":
            continue
        concentrations.append(a.text)

    return concentrations


def get_courses(program, degree):
    """
    Get list of possible courses that can be taken to fulfill degree requirement

    :param program: program name
    :param degree: degree name
    :return: list of courses
    """

    url = program_link(program, degree)

    if url is None:
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tbody = soup.find('tbody')

    if tbody is None:
        print("Not implemented")
        return

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
    """
    Check if degree contains concentrations or threads

    :param link: URL link of the program
    :return: true if degree is simple, false if not
    """

    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    if soup.find(id="requirementstextcontainer") is None:
        return False
    else:
        return True


def get_bachelors_programs():
    """
    Get list of all bachelors programs currently offered in Georgia Institute of Technology

    :return: list of bachelors programs
    """

    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="bachelorstextcontainer")

    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    return programs


def get_masters_programs():
    """
    Get list of all masters programs currently offered in Georgia Institute of Technology

    :return: list of masters programs
    """

    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="masterstextcontainer")

    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    return programs


def get_doctoral_programs():
    """
    Get list of all doctoral programs currently offered in Georgia Institute of Technology

    :return: list of doctoral programs
    """

    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="doctoraltextcontainer")

    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    return programs


def get_minors_programs():
    """
    Get list of all minors programs currently offered in Georgia Institute of Technology

    :return: list of minors programs
    """

    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="minorstextcontainer")

    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    return programs


def get_total_credit_hours(program, degree):
    """
    Get total credit hours required to complete the program degree requirement

    :param program: program name
    :param degree: degree type
    :return: amount of credit hours
    """

    url = program_link(program, degree)

    if url is None:
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tr = soup.find_all('tr', {"class": "listsum"})[0]
    hour = tr.find_all('td')[1].text

    return hour


def program_link(program, degree):
    """
    Get link of the program and degree pair

    :param program: program name
    :param degree: degree type
    :return: URL of the program
    """

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

    return url