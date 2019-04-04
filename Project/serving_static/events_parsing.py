import time
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup

def loadhtmlfrombrowser():
    date = datetime.datetime.now()
    date = str(date.month) + "/" + str(date.day) + "/" + str(date.year)
    url = "https://insidecbu.calbaptist.edu/ICS/Welcome_to_InsideCBU!.jnz?portlet=University_Calendar_" \
          "%e2%80%93_Public&screen=MainView&screenType=change&calendarView=list&date=" + date
    browser = webdriver.Chrome()
    browser.get(url)
    # wait five seconds for javascript to load
    time.sleep(5)
    html = browser.execute_script("return document.body.innerHTML")
    browser.close()
    return html


# Finds the tag where the 'calendar-list-view' is (the ember id changes and must be found this way)
def find_calendar_tag(soup):
    for tag in soup.find_all(True):
        if tag.name == "div" and tag.has_attr('class'):
            if 'calendar-list-view' in tag['class']:
                return tag
    return None


# Removes empty divs from the list
def remove_empty(tags):
    not_empty = list()
    for tag in tags:
        if tag.name is not None:
            not_empty.append(tag)
    return not_empty


def find_tag_in_tag(name, class_tag, tag):
    for subtag in tag.children:
        if subtag.name == name and subtag.has_attr('class'):
            if class_tag in subtag['class']:
                return subtag
    raise NotImplementedError


def get_date(soup_event):
    date_tag = find_tag_in_tag('span', 'date', soup_event)
    for subtag in date_tag.children:
        if subtag.name == 'button':
            return subtag.string

    # Get the date for the above one (keeps going up until it finds a date)
    return get_date(soup_event.find_previous_sibling('div'))


def get_hours(soup_event):
    hours_tag = find_tag_in_tag('span', 'hours', soup_event)
    return hours_tag.string.strip()


def get_info(soup_event):
    info_tag = find_tag_in_tag('span', 'info', soup_event)
    info_str = ""
    for string in info_tag.strings:
        if "- at" in string:
            info_str += " - " + string.replace("- at", "").strip()
        elif "More details" not in string:
            info_str += string.strip()
    return info_str.replace("'","")

def parse_events(soup_events):
    events = list()
    for soup_event in soup_events:
        date = get_date(soup_event)
        hours = get_hours(soup_event)
        info = get_info(soup_event)
        event = {
            "date": date,
            "hours": hours,
            "description": info
        }
        events.append(event)
    return events

def loadeventsfromhtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    calendar = find_calendar_tag(soup)
    if calendar is None:
        raise NotImplementedError

    soup_events = remove_empty(calendar.children)
    events = parse_events(soup_events)
    return events


def load_CBU_events():
    html = loadhtmlfrombrowser()
    events = loadeventsfromhtml(html)
    return events
