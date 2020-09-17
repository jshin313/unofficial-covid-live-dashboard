from app import db

class DailyCase(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(64), index=True, unique=True)
    onCampusStudents = db.Column(db.Integer, index=True)
    offCampusStudents = db.Column(db.Integer, index=True)
    nonCampusStudents = db.Column(db.Integer, index=True)
    employees = db.Column(db.Integer, index=True)
    total = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<DailyCase {}>'.format(self.date)

class WeeklyTest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timeframe = db.Column(db.String(64), index=True, unique=True)
    total_tested = db.Column(db.Integer, index=True)
    positive_cases = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<DailyCase {}>'.format(self.timeframe)
