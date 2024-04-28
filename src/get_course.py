from datetime import datetime
from selenium.webdriver.chrome.options import Options
import os
import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml

import config


def extract_days_and_times(days_time):
    days_end_index = days_time.index(" from ")
    days = days_time[:days_end_index].strip()

    times_start_index = days_time.index(" from ") + len(" from ")
    times = days_time[times_start_index:].strip()

    return days[0:-7], times.replace("-", "").replace(" to ", "-")


def format_time(time):
    time = time.replace("am", " AM").replace("pm", " PM")
    if ":" not in time:
        time = f"{time[:-3]}:00:00 {time[-2:]}"
    else:
        time = f"{time[:-3]}:00 {time[-2:]}"

    time = datetime.strptime(time, "%I:%M:%S %p")

    return time.strftime("%H:%M:%S")


def format_days(days):
    days = days.replace(" and ", ",")
    days = days.split(",")
    days = [day[0:2].upper() for day in days]

    return ",".join(days)


def format_dates(dates):
    dates = dates.replace("From ", "").strip()
    _, dates = dates.split(" – ")
    dates = dates.strip().replace("through", "-")
    start_date, end_date = dates.split("-")

    year = end_date[-4:]
    start_date = f"{start_date[0:-1]}, {year}"
    end_date = end_date[6:]

    if end_date[0].isnumeric():
        end_date = end_date[1:]

    return [start_date, end_date], year


def get_faculty_info(doc):
    table = doc.find_all("table", class_="directory-search-results")
    if not table:
        return "", "", "", "", ""

    rows = table[0].tbody.find_all("tr")
    for row in rows:
        # Name
        full_name = row.find("strong").text.strip().replace(",", "").split(" ")
        first_name = full_name[1]
        last_name = full_name[0]
        name = f"{first_name} {last_name}"

        # Faculty and Location
        all_faculty_info = row.find_all("td")[1].text.strip().strip("\t")
        all_faculty_info = " ".join(all_faculty_info.split())

        all_faculty_info = all_faculty_info.split(" ")
        faculty = all_faculty_info[0]
        location = " ".join(all_faculty_info[1:])
        location = (
            location.replace("RC", "Rock Creek Campus,")
            .replace("SY", "Sylvania Campus,")
            .replace("CA", "Cascade Campus,")
        )

        # Phone Number and Email
        phone_number = row.find_all("td")[2].text.strip()

        input_box = doc.find_all("input")[0]
        email = input_box.get("value")

        return name, faculty, location, phone_number, email


def get_course_info_from_html(url):
    response = requests.get(url)
    doc = BeautifulSoup(response.content, "html.parser")

    breadcrumps = doc.find_all("nav", id="breadcrumbs")[0]

    course_title = doc.find_all("h3")[0].text.strip()
    short = course_title.split(" ")[0]
    course_title = course_title.replace(short, "").strip()

    pos = ""
    for pos, string in enumerate(short):
        if string.isnumeric():
            break

    short = f"{short[0:pos]}-{short[pos:]}"

    term = breadcrumps.find_all("a")[2].text.strip()
    term = term.replace(": Credit", "")

    class_schedule = doc.find_all("table", class_="jxScheduleSortable")[0]
    if not class_schedule:
        return

    rows = class_schedule.tbody.find_all("tr")
    for row in rows:
        # Class Type
        class_type = row.find("td").text.strip()

        # Location
        location = ""
        if class_type == "In_person":
            location = row.find_all("td")[1].text.strip()
            location = location.split(" ")
            location = f"{location[0]} Campus, {' '.join(location[1:])}"

        # Start and End Dates
        dates = row.find_all("td")[3].text.strip()
        dates, year = format_dates(dates)
        start_date, end_date = dates

        date_obj = datetime.strptime(start_date, "%B %d, %Y")
        start_date = date_obj.strftime("%b %d %Y %a (12:00:00)")

        date_obj = datetime.strptime(end_date, "%B %d, %Y")
        end_date = date_obj.strftime("%b %d %Y %a (12:00:00)")

        # Days and Start and End Times
        days_time = row.find_all("td")[2].text.strip()
        if days_time == "Available 24/7":
            start_time = ""
            end_time = ""
            days = ""
        else:
            days, times = extract_days_and_times(days_time)

            days = format_days(days)
            start_time, end_time = times.split("-")

            if "am" not in start_time and "pm" not in start_time:
                if "am" in end_time:
                    start_time += "am"
                elif "pm" in end_time:
                    start_time += "pm"

            if "am" not in end_time and "pm" not in end_time:
                if "am" in start_time:
                    end_time += "am"
                elif "pm" in start_time:
                    end_time += "pm"

            if class_type != "Online":
                start_time = format_time(start_time)
                end_time = format_time(end_time)

        # Faculty and Professor Info
        faculty_link = row.find_all("td")[5].a.get("href")
        faculty_response = requests.get(faculty_link)
        faculty_doc = BeautifulSoup(faculty_response.content, "html.parser")
        name, faculty, office, phone_number, email = get_faculty_info(
            faculty_doc,
        )

        info = {
            "title": course_title,
            "topic": breadcrumps.find_all("a")[-1].text.strip(),
            "class_number": url[-5:],
            "short": short,
            "author": "Hashem A. Damrah",
            "term": term,
            "faculty": faculty,
            "college": "Portland Community College",
            "location": location,
            "year": year,
            "start_date": start_date,
            "end_date": end_date,
            "start_time": start_time,
            "end_time": end_time,
            "days": days,
            "url": "",
            "type": class_type,
            "notes_type": "lectures" if class_type != "Online" else "chapters",
            "professor": {
                "name": name,
                "email": email,
                "phone_number": phone_number,
                "office": office,
            },
        }

        return info


def main(crns):
    crn_list = crns.split(",")

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    for crn in crn_list:
        driver.get("https://www.pcc.edu/schedule/")
        search_input = driver.find_element(By.NAME, "queryText")

        search_input.clear()
        search_input.send_keys(crn)
        search_input.submit()

        time.sleep(1)

        url = driver.current_url
        info = get_course_info_from_html(url)
        if not info:
            continue

        path = f"{config.root}/{info['short'].lower()}/"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/info.yaml", "w") as file:
            yaml.dump(
                info,
                file,
                default_flow_style=False,
                sort_keys=False,
                default_style='"',
            )

    driver.quit()
