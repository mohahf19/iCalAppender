import argparse
import pathlib
from datetime import date

from icalendar import Calendar, Event, vCalAddress

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

parser.add_argument(
    "--weekly",
    required=False,
    help="Date (in iso format) for which all the events will repeat weekly",
)

parser.add_argument(
    "--private",
    required=False,
    default=False,
    help="Whether the event is private or not",
    action=argparse.BooleanOptionalAction,
)


def add_emails_to_event(emails: list[str], event: Event) -> Event:
    for email in emails:
        attendee = vCalAddress(f"MAILTO:{email}")
        event.add("attendee", attendee, encode=0)
    return event


def add_weekly_repetition(until: str, event: Event) -> Event:
    date_dt = date.fromisoformat(until)
    event.add("RRULE", {"UNTIL": date_dt, "FREQ": "WEEKLY", "WKST": "MO"})
    return event


def mark_as_private(event: Event) -> Event:
    event.add("CLASS", "PRIVATE")
    return event


args = parser.parse_args()
input_path = pathlib.Path(args.input)
email = args.email
emails = args.emails
weekly_date = args.weekly
private = args.private


if emails is None:
    emails = []

if email is not None:
    emails.append(email)

with open(input_path, encoding="UTF-8") as file:
    cal = Calendar.from_ical(file.read())
    events = [item for item in cal.walk() if item.name == "VEVENT"]
    print(f"There are {len(events)} events in this calendar")
    new_events = [add_emails_to_event(emails, event) for event in events]
    if weekly_date is not None:
        new_events = [add_weekly_repetition(weekly_date, event) for event in new_events]

    if private:
        new_events = [mark_as_private(event) for event in new_events]

output_path = pathlib.Path.joinpath(
    input_path.with_suffix(""), "_out", input_path.suffix
)
output_path = input_path.parent / (input_path.stem + "_out" + input_path.suffix)

with open(output_path, "wb") as file:
    file.write(cal.to_ical())
