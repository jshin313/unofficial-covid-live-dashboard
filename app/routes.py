from flask import render_template
from app import app
from app import scraper
from app import db
from app.models import DailyCase, WeeklyTest

@app.route('/')
@app.route('/index')
def index():
    # See if anything changed since last time
    total_tests = scraper.scrape()

    # Get all the individual vars from the database
    latest_cases = db.session.query(DailyCase).order_by(DailyCase.id.desc()).first()
    last_updated_cases= db.session.query(DailyCase).order_by(DailyCase.id.desc())[2].total
    total_active_cases = latest_cases.total
    new_cases = total_active_cases - last_updated_cases
    on_campus_students = latest_cases.onCampusStudents
    off_campus_students = latest_cases.offCampusStudents
    employees = latest_cases.employees

    dates_list = []
    on_campus_students_list = []
    off_campus_students_list = []
    employees_list = []
    new_cases_on_campus_students_list = []
    new_cases_off_campus_students_list = []
    new_cases_employees_list = []
    new_cases_total_list = []

    # Get the sets from the database
    dates = DailyCase.query.all()
    for i, day in enumerate(dates):
        dates_list.append(day.date)
        on_campus_students_list.append(day.onCampusStudents)
        off_campus_students_list.append(day.offCampusStudents)
        employees_list.append(day.employees)

        # Create the sets for new cases
        if (i > 0):
            new_cases_on_campus_students_list.append(dates[i].onCampusStudents - dates[i - 1].onCampusStudents)
            new_cases_off_campus_students_list.append(dates[i].offCampusStudents - dates[i - 1].offCampusStudents)
            new_cases_employees_list.append(dates[i].employees - dates[i - 1].employees)
            new_cases_total_list.append(new_cases_employees_list[i - 1] + new_cases_off_campus_students_list[i - 1] + new_cases_on_campus_students_list[i - 1])

    new_cases_dates_list = dates_list[1:]
    # print(new_cases_dates_list)

    negative_cases_list = []
    positive_cases_list = []
    time_frame_list = []
    for week in WeeklyTest.query.all():
        positive_cases_list.append(week.positive_cases)
        negative_cases_list.append(week.total_tested - week.positive_cases)
        time_frame_list .append(week.timeframe)

    return render_template('index.html',
                           total_active_cases=total_active_cases,
                           total_tests=total_tests,
                           on_campus_students=on_campus_students,
                           off_campus_students=off_campus_students,
                           employees=employees,
                           new_cases=new_cases,
                           on_campus_students_list=on_campus_students_list,
                           off_campus_students_list=off_campus_students_list,
                           employees_list=employees_list,
                           dates_list=dates_list,
                           positive_cases_list=positive_cases_list,
                           negative_cases_list=negative_cases_list,
                           time_frame_list=time_frame_list,
                           new_cases_dates_list=new_cases_dates_list,
                           new_cases_employees_list=new_cases_employees_list,
                           new_cases_off_campus_students_list=new_cases_off_campus_students_list,
                           new_cases_on_campus_students_list=new_cases_on_campus_students_list,
                           new_cases_total_list=new_cases_total_list)

