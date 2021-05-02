import requests
import json


def get_json(district_id, date):
    response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
                            '?district_id={district_id}&date={date}'.format(district_id=district_id, date=date))
    response_json_dict = response.json()
    # print(response_json)
    return response_json_dict


def parse_response_json(response_json):
    list_centers = response_json['centers']
    total_centers = len(list_centers)
    # print(total_centers)
    count = 0
    for center in list_centers:
        center_name = center['name']
        center_sessions = center['sessions']
        # print(center_name + "  " + str(len(center_sessions)))
        # print(center_name)
        for session in center_sessions:
            if session['available_capacity'] > 0:
                print(center_name)
                print(session['date'])
                print(session['available_capacity'])
                print(session['min_age_limit'])
            if session['min_age_limit'] < 45 and session['available_capacity'] > 0:
                print(center_name)
                print('FINALLY!')


if __name__ == '__main__':
    district_id = 725
    date = '02-05-2021'
    # for i in range(1, 737):
    # district_id = i
    response_json = get_json(district_id, date)
    parse_response_json(response_json)