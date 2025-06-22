import sys
import logging
from logParser import parseLogFile
from reportCreator import createReport


def main():
    """
    using sys.argv to determine the log file path.
    uses the argument provided, otherwise defaults to logs.log
    """
    if len(sys.argv) > 1:
        logFile = sys.argv[1]
    else:
        logFile =  "logs[14].log"

    try:
        jobs = parseLogFile(logFile)
    except FileNotFoundError:
        logging.error(f"{logFile} file not found")
        sys.exit(1)

    report = createReport(jobs)
    print(report)

    #saves the report to output.txt
    with open("job_output.txt", "w") as f:
        f.write(report)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    main()