def createReport(jobs):
    """
    Creates report for jobs.
    logs warnings whenever the job duration is greater than 5mins(300 secs)
    and logs errors when durations is greater than 10mins(600 secs)
 
    Args:
        jobs (dict): a dictionary mapping each PID(str) to job data, which includes:
                 - "start": datetime object indicating the job start time
                 - "end": datetime object indicating the job end time
                 - "description": job description string  

    Returns:
        str: A multi-line string report of the job durations and any warnings/errors.
    """
    reports = []

    for jobPid, jobData in jobs.items():
        if not(jobData.get("START") and jobData.get("END")): # skips jobs with missing starttime or endtime
            continue
        # Calculate duration in seconds
        jobDuration = (jobData["END"] - jobData["START"]).seconds
        if jobDuration > 600:
            line = "[ERROR]: exceeded 10 minutes"
        elif jobDuration > 300:
            line = "[WARNING]: exceeded 5 minutes"
        else:
            continue # job is less than 10minutes and less than 5 minutes
        line += f"PID {jobPid}: Duration {jobDuration} seconds "
        reports.append(line)
    return "\n".join(reports)