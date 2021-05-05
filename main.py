# gets url
import requests
# HTML parser
from bs4 import BeautifulSoup

DEGREES = {}


def sub_webpages(url: str):
    """
    :return: collect all sublinks and run get contents
    """
    subpages = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    for a in soup.find_all('a', href=True):
        if 'program_group' in a['href']:
            fix = url[:41]
            subpages.append(''.join((fix, a['href'])))

    for i in subpages:
        get_contents(i)

    for x in list(DEGREES.keys()):
        if DEGREES[x] == {}:
            del DEGREES[x]


def get_contents(url: str):
    """
    :return: contents of course requirements needed to graduates
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        degree_type = soup.find("p", {'class': "titlestyle"}).get_text()
        degree_name = [a['name'] for a in soup.findAll('a') if a.get('name')]
        table = soup.findAll("table", {'class': 'tab_adm'})
        temp = []
        for line in table:
            if line.get_text().find("First Year") > -1:
                paragraph = line.get_text().split("\n")
                paragraph[-1] = "Year"
                temp.append(paragraph)

        course = []
        for x in range(len(temp)):
            sub = []
            for i in range(len(temp[x]) - 1):
                if "Year" in temp[x][i]:
                    sub.append([temp[x][i + 1]])
            course.append(sub)

        DEGREES.setdefault(degree_type, dict(zip(degree_name, course)))
    except AttributeError:
        print("AttributeError: invalid webpage entry")


if __name__ == '__main__':
    sub_webpages("https://student.utm.utoronto.ca/calendar/program_list.pl")
    print(DEGREES)
