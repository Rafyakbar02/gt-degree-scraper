from bs4 import BeautifulSoup
import requests
import pandas as pd

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

    dict = {}
    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    dict["Program"] = programs
    df = pd.DataFrame(dict)

    return df


def get_concentrations(program, degree):
    """
    Get list of concentrations/threads within the program and degree pair

    :param program: program name
    :param degree: degree name
    :return: list of concentrations
    """
    url = _program_link(program, degree)

    if url is None:
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    if soup.find(id="concentrationstextcontainer"):
        div = soup.find(id="concentrationstextcontainer")
    elif soup.find(id="standardandconcentrationoptiontextcontainer"):
        div = soup.find(id="standardandconcentrationoptiontextcontainer")
    elif soup.find(id="threadstextcontainer"):
        div = soup.find(id="threadstextcontainer")
    else:
        print("Program and degree pair doesn't have concentrations/threads")
        return

    dict = {}
    concentrations = []

    for a in div.find_all("a"):
        if a.text == "":
            continue
        concentrations.append(a.text)

    dict["Concentration"] = concentrations
    df = pd.DataFrame(dict)

    return df


def get_courses(program, degree, concentration=None):
    """
    Get list of possible courses that can be taken to fulfill degree requirement with the specified concentration

    :param program: program name
    :param degree: degree name
    :param concentration: concentration name
    :return: list of courses
    """
    # if concentration is None:
    #     url = _program_link(program, degree)
    # else:
    #     url = _concentration_link(program, degree, concentration)
    #
    # if url is None:
    #     return
    #
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, "html.parser")
    # tbody = soup.find('tbody')
    #
    # curr_category = ""
    # prev_credits = 0
    #
    # dict = {}
    # codes = []
    # categories = []
    # credits = []
    #
    # # Loop all rows in the table
    # for tr in tbody.find_all("tr"):
    #     # Store current category
    #     if 'areaheader' in tr['class']:
    #         curr_category = tr.text
    #         continue
    #
    #     # Check if row contains a course
    #     if tr.find("a", {"class": "bubblelink"}):
    #         curr_code = tr.a.text.replace("\xa0", " ")
    #         codes.append(curr_code)
    #         categories.append(curr_category)
    #
    #         hourscol = tr.find("td", {"class": "hourscol"})
    #
    #         if hourscol is None or hourscol.text == "":
    #             credits.append(prev_credits)
    #         else:
    #             hours = int(hourscol.text)
    #             credits.append(hours)
    #             prev_credits = hours
    #
    #     # Check if it's a flexible choice of courses
    #     elif tr.find("span", {"class": "courselistcomment"}):
    #         if 'Select' in tr.text:
    #             hourscol = tr.find("td", {"class": "hourscol"})
    #             hours = int(hourscol.text)
    #
    #             if hours > 4:
    #                 if hours % 3 == 0:
    #                     prev_credits = 3
    #                 elif hours % 4 == 0:
    #                     prev_credits = 4
    #             else:
    #                 prev_credits = hours
    #
    #             continue
    #
    #         curr_code = tr.span.text.strip()
    #         codes.append(curr_code)
    #         categories.append(curr_category)
    #
    #         hourscol = tr.find("td", {"class": "hourscol"})
    #
    #         if hourscol is None or hourscol.text == "":
    #             credits.append(prev_credits)
    #         else:
    #             hours = int(hourscol.text)
    #             credits.append(hours)
    #             prev_credits = hours
    #
    # dict["Course"] = codes
    # dict["Category"] = categories
    # dict["Credits"] = credits
    # df = pd.DataFrame(dict)
    #
    # return df


def get_degree_overview(program, degree, concentration=None):
    """
        Get an overview of the degree requirements

        :param program: program name
        :param degree: degree name
        :param concentration: concentration name
        :return: list of categories
        """
    if concentration is None:
        url = _program_link(program, degree)
    else:
        url = _concentration_link(program, degree, concentration)

    if url is None:
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    credits_total = 0
    categories = []
    credits = []

    for tr in soup.tbody.find_all("tr"):
        if "areaheader" in tr['class']:
            category = tr.span.text
            categories.append(category)

            if "firstrow" not in tr['class']:
                credits.append(credits_total)
                credits_total = 0

            continue

        if tr.find("td", {"class": "hourscol"}):
            hourscol = tr.find("td", {"class": "hourscol"})

            if hourscol is None or hourscol.text == "":
                continue

            hours = int(hourscol.text)
            credits_total += hours

        if "lastrow" in tr['class']:
            credits.append(credits_total)
            break

    dict = {"Categories": categories, "Credits": credits}
    df = pd.DataFrame(dict)

    return df


def _simple_degree(link):
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

    dict = {}
    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    dict["Program"] = programs
    df = pd.DataFrame(dict)

    return df


def get_masters_programs():
    """
    Get list of all masters programs currently offered in Georgia Institute of Technology

    :return: list of masters programs
    """

    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="masterstextcontainer")

    dict = {}
    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    dict["Program"] = programs
    df = pd.DataFrame(dict)

    return df


def get_doctoral_programs():
    """
    Get list of all doctoral programs currently offered in Georgia Institute of Technology

    :return: list of doctoral programs
    """

    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(id="doctoraltextcontainer")

    dict = {}
    programs = []

    for li in div.find_all("li"):
        curr_link = li.text
        end = curr_link.find('.')
        major = curr_link[:end]
        programs.append(major)

    dict["Program"] = programs
    df = pd.DataFrame(dict)

    return df


def get_total_credit_hours(program, degree, concentration=None):
    """
    Get total credit hours required to complete the program degree requirement

    :param program: program name
    :param degree: degree type
    :param concentration: concentration type
    :return: amount of credit hours
    """
    if concentration is None:
        url = _program_link(program, degree)
    else:
        url = _concentration_link(program, degree, concentration)

    if url is None:
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tbody = soup.find('tbody')

    if tbody is None:
        print("Not valid")

    tr = soup.find_all('tr', {"class": "listsum"})[0]
    hour = tr.find_all('td')[1].text

    return hour


def _program_link(program, degree):
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


def _concentration_link(program, degree, concentration):
    """
    Get link of the program, degree and concentration combination

    :param program: program name
    :param degree: degree type
    :param concentration: concentration type
    :return: URL of the program
    """
    program_url = _program_link(program, degree)

    if program_url is None:
        return

    page = requests.get(program_url)
    soup = BeautifulSoup(page.content, "html.parser")

    if soup.find(id="concentrationstextcontainer"):
        div = soup.find(id="concentrationstextcontainer")
    elif soup.find(id="standardandconcentrationoptiontextcontainer"):
        div = soup.find(id="standardandconcentrationoptiontextcontainer")
    elif soup.find(id="threadstextcontainer"):
        div = soup.find(id="threadstextcontainer")
    else:
        print("Program/Degree doesn't have concentrations/threads")
        return

    url = main_url

    for a in div.find_all("a"):
        if a.text == "":
            continue

        if a.text[-1] == " ":
            curr_concentration = a.text[:-1]
        else:
            curr_concentration = a.text

        if curr_concentration == concentration:
            url += a['href'][10:]
            break

    if url == "https://catalog.gatech.edu/programs/":
        print("Concentration not found")
        return

    return url
