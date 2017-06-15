from bs4 import BeautifulSoup

def test1():
    html = open("test_HTML.html")

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", attrs={"class":"details"})

    # The first tr contains the field names.
    headings = [th.get_text() for th in table.find("tr").find_all("th")]

    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        datasets.append(dataset)

    return datasets

print test1()