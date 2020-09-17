import requests
from bs4 import BeautifulSoup
import re
from app import db
from app.models import DailyCase, WeeklyTest

# Returns total number of tests
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
        print("Error: Error retreiving date")
        return -1

    print("Date: " + date)
    print("On Campus Students: " + str(on_campus_students))
    print("Off Campus Students: " + str(off_campus_students))
    print("Non Campus Students: " + str(non_campus_students))
    print("Employees: " + str(employees))
    print("Total Cases: " + str(total_cases))

    last_entry_date = db.session.query(DailyCase).order_by(DailyCase.id.desc()).first()
    primary_key = 1
    try:
        primary_key = last_entry_date.id + 1
        last_entry_date = last_entry_date.date
        print("Last Entry Date: " + last_entry_date)
    except:
        print("Empty Cases Table")

    if (last_entry_date is None):
        new_case = DailyCase(id=primary_key, date=date, onCampusStudents=on_campus_students, offCampusStudents=off_campus_students, nonCampusStudents=non_campus_students, employees=employees, total=total_cases)
        db.session.add(new_case)
        db.session.commit()
        print("Added New Case to database!")
        
    elif (date != last_entry_date):
        new_case = DailyCase(id=primary_key, date=date, onCampusStudents=on_campus_students, offCampusStudents=off_campus_students, nonCampusStudents=non_campus_students, employees=employees, total=total_cases)
        db.session.add(new_case)
        db.session.commit()
        print("Added New Case to database!")
    else:
        print("No new cases :(")
    print()

    # See if there's new test data from the dashboard
    table = page.find_all("table")[1]
    last_row = table("tr")[-2]

    time_frame = last_row("td")[0]("p")[0].text.split('\n')[0].replace("*", "")
    tested = int(last_row("td")[1]("p")[0].text.split('\n')[0].replace("*", ""))
    positive = int(last_row("td")[2]("p")[0].text.split('\n')[0].replace("*", ""))

    print("Time Frame: " + time_frame)
    print("Total Tested: " + str(tested))
    print("Positive: " + str(positive))

    primary_key = 1
    last_time_frame = db.session.query(WeeklyTest).order_by(WeeklyTest.id.desc()).first()
    try:
        primary_key = last_time_frame.id + 1
        last_time_frame = last_time_frame.timeframe
        print("Last time frame: " + last_time_frame)
    except:
        print("Empty Weekly Test table")

    if (time_frame != last_time_frame or last_time_frame is None):
        new_week = WeeklyTest(id=primary_key, timeframe=time_frame, total_tested=tested, positive_cases=positive)
        db.session.add(new_week)
        db.session.commit()
        print("Added New Week of Testing to database!")
    else:
        print("No test data added to database :(")

    print("\n\n")

    total_tested = int(page.find_all('td', class_='row_7 col_1')[0].text.split('\n')[0])
    return total_tested

