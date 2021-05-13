import datetime
import schedule
import requests
import time
from playsound import playsound

from config import district_id

def get_json(district_id, date):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict'
                            '?district_id={district_id}&date={date}'.format(district_id=district_id, date=date), headers=headers)
    # print(response.status_code)
    while response.status_code == 401:
        print('Retry')
        response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
                                '?district_id={district_id}&date={date}'.format(district_id=district_id, date=date),
                                headers=headers)
    response_json_dict = response.json()
    parse_response_json(response_json_dict)


def parse_response_json(response_json):
    list_centers = response_json['centers']
    # print(len(list_centers))
    for center in list_centers:
        center_name = center['name']
        center_sessions = center['sessions']
        for session in center_sessions:
            if session['min_age_limit'] < 45 and session['available_capacity'] > 3:
                print('*********** SLOT FOUND! ***********')
                print("Center name : ", center_name)
                print("Available capacity : ", session['available_capacity'])
                print("Vaccine : ", session['vaccine'])
                playsound('notif.mp3')
                print("\n\n\n\n")
                # quit()


if __name__ == '__main__':
    print("\n\nCowin_script started!\n\n")
    today = datetime.date.today()
    date = today.strftime("%d-%m-%Y")
    schedule.every(10).seconds.do(get_json, district_id, date)
    # playsound('notif.mp3')
    while True:
        schedule.run_pending()
        time.sleep(1)
