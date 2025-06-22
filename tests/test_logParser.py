import io
import unittest
from logParser import parseLogFileHelper

class TestLogParser(unittest.TestCase):
    def test_parse_valid_log(self):
        # CSV format: timestamp, description, status, PID
        sampleCsv = (
            "15:00:00,Scheduled task A, START,76512\n"
            "15:06:00,Scheduled task A, END,76512"
        )
        fileObj = io.StringIO(sampleCsv)
        jobs = parseLogFileHelper(fileObj)
        self.assertIn("76512", jobs)
        self.assertEqual(jobs["76512"]["START"].strftime("%H:%M:%S"), "15:00:00")
        self.assertEqual(jobs["76512"]["END"].strftime("%H:%M:%S"), "15:06:00")
        self.assertEqual(jobs["76512"]["description"], "Scheduled task A")

    def test_invalid_timestamp(self):
        sampleCsv = "invalid_time,Scheduled task A, START,76512\n"
        fileObj = io.StringIO(sampleCsv)
        jobs = parseLogFileHelper(fileObj)
        # no valid row due to invalid timestamp
        self.assertEqual(jobs, {})

    def test_unexpected_row_format(self):
        # Rows with less or more than 4 columns should be skipped
        sampleCsv = (
            "15:00:00,Scheduled task A, START\n"                        # 3 columns
            "15:06:00,Scheduled task A, END,76512,another column\n"     # 5 columns
            "12:10:00,Scheduled task B,START,44213\n"         # Valid
        )
        fileObj = io.StringIO(sampleCsv)
        jobs = parseLogFileHelper(fileObj)
        # Only the valid row should be parsed.
        self.assertEqual(set(jobs.keys()), {"44213"})

    def test_incomplete_log(self):
        # entry with only START should result in an incomplete job.
        sampleCsv = "15:00:00,Scheduled task A,START,76512\n"
        fileObj = io.StringIO(sampleCsv)
        jobs = parseLogFileHelper(fileObj)
        self.assertIn("76512", jobs)
        self.assertIsNotNone(jobs["76512"]["START"])
        self.assertIsNone(jobs["76512"]["END"])

    def test_mixed_valid_and_invalid_entries(self):
        # Mixture of valid and invalid rows.
        sampleCsv = (
            "15:00:00,Scheduled task A,START,76512\n"          # Valid.
            "invalid,Scheduled task A,START,76512\n"            # Invalid timestamp.
            "15:06:00,Scheduled task A,END,76512\n"             # Valid.
            "16:10:00,Scheduled task B,START,88912\n"           # Valid.
            "16:15:00,Scheduled task B,END,88912\n"             # Valid.
            "16:20:00,Scheduled task C,START\n"                 # Invalid row format.
        )
        fileObj = io.StringIO(sampleCsv)
        jobs = parseLogFileHelper(fileObj)
        # Only valid entries should be processed: PIDs 76512 and 88912.
        self.assertEqual(set(jobs.keys()), {"76512", "88912"})
        self.assertIsNotNone(jobs["76512"]["START"])
        self.assertIsNotNone(jobs["76512"]["END"])
        self.assertIsNotNone(jobs["88912"]["START"])
        self.assertIsNotNone(jobs["88912"]["END"])

    def test_duplicate_start_entries(self):
        # duplicate START entries overwrites earlier entry
        sampleCsv = (
            "15:00:00,Scheduled task A,START,76512\n"
            "16:02:00,Scheduled task A,START,76512\n"
            "17:06:00,Scheduled task A,END,76512\n"
        )
        fileObj = io.StringIO(sampleCsv)
        jobs = parseLogFileHelper(fileObj)
        # second entry is used as start time
        self.assertEqual(jobs["76512"]["START"].strftime("%H:%M:%S"), "16:02:00")

    def test_duplicate_end_entries(self):
        # duplicate END entries overwrites earlier entry
        sampleCsv = (
            "15:00:00,Scheduled task A,START,76512\n"
            "16:02:00,Scheduled task A,END,76512\n"
            "17:06:00,Scheduled task A,END,76512\n"
        )
        fileObj = io.StringIO(sampleCsv)
        jobs = parseLogFileHelper(fileObj)
        # second entry is used as end time
        self.assertEqual(jobs["76512"]["END"].strftime("%H:%M:%S"), "17:06:00")
