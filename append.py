import argparse
import pathlib

from icalendar import Calendar, Event

parser = argparse.ArgumentParser(description="Appends details to iCal (ics) files")

# Parser arguments (details to add to all the events)
parser.add_argument(
    "--input",
    required=True,
    help="Path to an .ics file to process. The output will be at the same path, but with an _out suffix",
)

parser.add_argument(
    "--email",
    required=False,
    help="Email to append to each event in the calendar",
)
parser.add_argument(
    "--emails",
    required=False,
    help="List of space-separated emails to append to each event in the calendar",
    nargs="+",
)

args = parser.parse_args()
input_path = pathlib.Path(args.input)
email = args.email
emails = args.emails

if emails is None:
    emails = []

if email is not None:
    emails.append(email)

with open(input_path) as file:
    cal = Calendar.from_ical(file.read())
    print(cal)
