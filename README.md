## README.md

# Log Monitoring Application

This is a log monitoring application written in Python that reads log file, measures how long each job takes from start to finish and generates warnings or errors if the processing time exceeds 5minutes or 10minutes.

---

## Project Structure

logMonitor/

├── main.py               # Main entry point

├── logParser.py          # Parses the CSV log file

├── reportCreator.py      # Generates report from parsed data

├── tests/                # Unit tests

│   ├── test_logParser.py

│   └── test_reportCreator.py

├── logs[13].log          # Input log file (sample)

└── job_output.txt        # Auto-generated output report

## Log File Format

The log file (`logs[13].log`) must be a CSV with **4 columns**, in this exact order:

1. **Timestamp** – format: `HH:MM:SS`
2. **Description** – short job description
3. **Status** – either `START` or `END`
4. **PID** – a unique process ID

### Example Log Entry
```
11:56:15,scheduled task 294, START,46125
12:02:01,scheduled task 294, END,46125
```

---

## How It Works

### main.py
- Reads the log file (`logs[13].log` by default or from CLI).
- Parses it using `logParser.py`.
- Generates a report with `reportCreator.py`.
- Prints the report to the console.
- **Also saves the report to `job_output.txt`.**

---

## Running the App

### Default (uses `logs[13].log`):

```bash
python main.py
```

### With a different log file:

```bash
python main.py your_log_file.log
```

After execution, a file `job_output.txt` will be created or overwritten with the generated report.

---

## Running Tests

Make sure you're in the root of the project.

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

This runs all unit tests inside the `tests/` directory.

---

## What the Report Logs

- Logs a **WARNING** if job duration > 5 minutes (300 seconds).
- Logs an **ERROR** if job duration > 10 minutes (600 seconds).
- Ignores jobs shorter than or equal to 5 minutes.
- Ignores jobs that don’t have both START and END entries.

---

## Example Output (`output.txt`)

```
[WARNING]: exceeded 5 minutes]PID 10123: Duration 395 seconds 
[ERROR]: exceeded 10 minutes]PID 22001: Duration 721 seconds 
```

---

## Logging and Edge Cases

- Handles missing or incorrect rows gracefully.
- Strips extra whitespace in columns.
- Logs issues like:
  - unexpected row length
  - bad timestamp format
  - missing START or END
  - duplicate START/END

---
