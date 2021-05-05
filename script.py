import datetime
import schedule
import requests
import time
from playsound import playsound


def get_json(district_id, date):
    response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
                            '?district_id={district_id}&date={date}'.format(district_id=district_id, date=date))
    response_json_dict = response.json()
    parse_response_json(response_json_dict)


def parse_response_json(response_json):
    list_centers = response_json['centers']
    # print(len(list_centers))
    for center in list_centers:
        center_name = center['name']
        center_sessions = center['sessions']
        for session in center_sessions:
            if session['min_age_limit'] < 45 and session['available_capacity'] > 0:
                print(center_name)
                print('FINALLY!')
                playsound('notif.mp3')


if __name__ == '__main__':
    district_id = 725
    today = datetime.date.today()
    date = today.strftime("%d-%m-%Y")
    schedule.every(10).seconds.do(get_json, district_id, date)
    playsound('notif.mp3')
    while True:
        schedule.run_pending()
        time.sleep(1)
