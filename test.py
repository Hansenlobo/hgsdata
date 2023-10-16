# import datetime

# # Get the current date and time
# current_datetime = datetime.datetime.now()

# # Calculate the start date and time of the last year (January 1st) at midnight
# last_year_start = datetime.datetime(current_datetime.year - 1, 1, 1)

# # Calculate the end date and time of the last year (December 31st) at 23:59:59
# last_year_end = datetime.datetime(current_datetime.year - 1, 12, 31, 23, 59, 59)

# # Format the dates in ISO format
# last_year_start_iso = last_year_start.isoformat()
# last_year_end_iso = last_year_end.isoformat()

# print("Start date and time of the last year (ISO format):", last_year_start_iso)
# print("End date and time of the last year (ISO format):", last_year_end_iso)

import datetime

# Get the current date and time
current_datetime = datetime.datetime.now()

# Calculate the start date and time of the current year
current_year_start = current_datetime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

# Calculate the end date and time of the current year
next_year_start = datetime.datetime(current_datetime.year + 1, 1, 1, 0, 0, 0, 0)
current_year_end = next_year_start - datetime.timedelta(seconds=1)

# Format the dates in ISO format
current_year_start_iso = current_year_start.isoformat()
current_year_end_iso = current_year_end.isoformat()

print("Start date and time of the current year (ISO format):", current_year_start_iso)
print("End date and time of the current year (ISO format):", current_year_end_iso)
