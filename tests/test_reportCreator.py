import unittest
import datetime
from reportCreator import createReport

class TestReportGenerator(unittest.TestCase):
    def test_createReport(self):
        jobs = {
            "76512": {
                "START": datetime.datetime.strptime("15:00:00", "%H:%M:%S"),
                "END": datetime.datetime.strptime("15:06:00", "%H:%M:%S"),
                "description": "Scheduled task A"
            },
            "46213": {
                "START": datetime.datetime.strptime("15:10:00", "%H:%M:%S"),
                "END": datetime.datetime.strptime("15:25:00", "%H:%M:%S"),
                "description": "Scheduled task B"
            }
        }
        report = createReport(jobs)
        #print(report)
        self.assertIn("[WARNING]: exceeded 5 minutesPID 76512: Duration 360 seconds", report)
        self.assertIn("[ERROR]: exceeded 10 minutesPID 46213: Duration 900 seconds", report)

    def test_incomplete_job(self):
        jobs = {
            "46213": {
                "START": datetime.datetime.strptime("15:00:00", "%H:%M:%S"),
                "END": None,
                "description": "incomplete job"
            }
        }
        report = createReport(jobs)
        self.assertEqual(report, "")

    def test_empty_jobs(self):
        jobs = {}
        report = createReport(jobs)
        self.assertEqual(report, "")

    def test_job_under_5_minutes(self):
        jobs = {
            "76512": {
                "START": datetime.datetime.strptime("15:00:00", "%H:%M:%S"),
                "END": datetime.datetime.strptime("15:03:00", "%H:%M:%S"),
                "description": "Scheduled task A"
            },
            "46213": {
                "START": datetime.datetime.strptime("15:10:00", "%H:%M:%S"),
                "END": datetime.datetime.strptime("15:12:00", "%H:%M:%S"),
                "description": "Scheduled task B"
            }
        }
        report = createReport(jobs)
        self.assertEqual(report, "")

if __name__ == '__main__':
    unittest.main()
