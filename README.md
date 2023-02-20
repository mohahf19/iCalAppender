# iCalAppender

iCalAppender is a simple CLI tool that appends information to an iCal file.

## Motivation

When a new semester starts at school, we can export out classes as an iCal file from the school's website. This file has two main issues:

- Each event is separate. Meaning, one class per week would be 14 events instead of being a single repititve event.
- There are no options to modify the events and add attendees. For example, this is useful in syncing your calendar with your work email, so that your coworkers can see when you are busy.

This tool allows you to fix these issues.

## Installation

To create an environment, run

```
conda env create -f environment.yml
```

or simply install the dependencies listed in `environment.yml` manually.

Afterwards, invoke the script with

```
python append.py --help
```

## Usage

```
append.py [-h] --input INPUT [--email EMAIL]
                 [--emails EMAILS [EMAILS ...]]
                 [--weekly WEEKLY]
```

## Options

```
  -h, --help            show this help message and exit
  --input INPUT         Path to an .ics file to process. The
                        output will be at the same path, but
                        with an _out suffix
  --email EMAIL         Email to append to each event in the
                        calendar
  --emails EMAILS [EMAILS ...]
                        List of space-separated emails to
                        append to each event in the calendar
  --weekly WEEKLY       Date (in iso format) for which all the
                        events will repeat weekly
```

## Motivation Solution

Download your classes as an iCal file from the school's website and delete all the events after the first week. Then run

```
python append.py --input <path-to-ics-file> --weekly <last-day-of-semester> --email <work-email>
```

and then add the new calendar to your school calendar. This will send out exactly one email for each class.
