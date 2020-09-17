import requests
from bs4 import BeautifulSoup
import re
from app import db
from app.models import DailyCase, WeeklyTest

def scrape():
    url = 'https://www.temple.edu/life-temple/health-wellness/covid-19-keeping-our-community-safe-healthy/university-communication/active-covid-19-cases-temple-university'

    page = BeautifulSoup(requests.get(url).content, 'html.parser')

    # See if there are new cases from the live dashboard
    on_campus_students = int(page.find_all('td', class_='row_1 col_1')[0].text.split('\n')[0])
    off_campus_students = int(page.find_all('td', class_='row_1 col_2')[0].text.split('\n')[0])
    non_campus_students = int(page.find_all('td', class_='row_1 col_3')[0].text.split('\n')[0])
    employees = int(page.find_all('td', class_='row_2 col_4')[0].text.split('\n')[0])
    total_cases = int(page.find_all('td', class_='row_3 col_4')[0].text.split('\n')[0])

    date = ""
    for p in page.find_all('p'):
        if "updated" in p.text.lower():
            date = p.text.split(" ")[1].split(" ")[0].strip()
            break;
    if (date == ""):
        print("Error retreiving date")
        return -1

    print("Date: " + date)
    print("On Campus Students: " + str(on_campus_students))
    print("Off Campus Students: " + str(off_campus_students))
    print("Non Campus Students: " + str(non_campus_students))
    print("Employees: " + str(employees))
    print("Total Cases: " + str(total_cases))
    print()

    last_entry_date = db.session.query(DailyCase).order_by(DailyCase.id.desc()).first().date
    try:
        print("Last Entry Date: " + last_entry_date)
    except:
        print("Empty Database")

    if (date != last_entry_date or last_entry_date is None):
        new_case = DailyCase(date=date, onCampusStudents=on_campus_students, offCampusStudents=off_campus_students, nonCampusStudents=non_campus_students, employees=employees, total=total_cases)
        db.session.add(new_case)
        db.session.commit()
        print("Added New Case to database!")
    else:
        print("No new cases")

    # See if there's new test data from the dashboard
    time_frame = page.find_all('td', class_='row_1 col_0')[1].text.split('\n')[0]
    total_tested = int(page.find_all('td', class_='row_1 col_1')[1].text.split('\n')[0])
    positive = int(page.find_all('td', class_='row_1 col_2')[1].text.split('\n')[0])
    print("Time Frame: " + time_frame)
    print("Total Tested: " + str(total_tested))
    print("Positive: " + str(positive))

    return 0
