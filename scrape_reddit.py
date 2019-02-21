import time
from datetime import date
import json
import requests
import calendar


session = requests.session()

base_url = 'https://api.pushshift.io/reddit/search/submission/?subreddit=umd&sort=desc&sort_type=created_utc&after={}&before={}&size=1000'
year = 2013
month = 1




def get_urls(year, month):

    print("month: "  + str(month))

    num_days = days_in_month(year, month)

    day_start = 1
    day_end = 2
    day_increment = 1



    urls = []

    while (day_start < num_days):

        after = date(year, month, day_start)
        before = date(year, month, day_end)

        unix_after = int(time.mktime(after.timetuple()))
        unix_before = int(time.mktime(before.timetuple()))

        api_url = base_url.format(unix_after, unix_before)


        r = session.get(api_url, timeout = 5)

        json_data = json.loads(r.text)

        data = json_data['data']

        for post in data:

            parent_comment = post[0]
            num_comments = post['num_comments']
            full_link = post['full_link']

            if '?' in parent_comment and num_comments > 0:
                check = acceptable(parent_comment)
                if check != False:
                    print(parent_comment)
                    print(full_link)


        day_start += day_increment
        day_end += day_increment

    print("\n")


    return urls


def acceptable(parent_comment):
    length = len(parent_comment.split(' '))
    if length > 50 or length < 3:
        return False



def days_in_month(year, month):
    if (month < 1) or (month > 12):
        print ("please enter a valid month")
    elif (year < 1) or (year > 9999):
        print ("please enter a valid year between 1 - 9999")
    else:
        return calendar.monthrange(year, month)[1]



while (month <= 5):

    get_urls(year, month)

    time.sleep(.50)

    month += 1







