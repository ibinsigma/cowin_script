import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/cowin')
def cowin():
    district_id = request.args['district_id']
    date = request.args['date']
    response_json_dict = get_json(district_id, date)
    final_dict_open = parse_response_json(response_json_dict)
    return final_dict_open


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
    open_centers = {}
    for center in list_centers:
        center_name = center['name']
        center_sessions = center['sessions']
        open_sessions = []
        open_18_sessions = []
        for session in center_sessions:
            if session['available_capacity'] > 0:
                # print(center_name)
                # print(session['date'])
                # print(session['available_capacity'])
                # print(session['min_age_limit'])
                open_sessions.append(session)
                # print(session)
                # print(type(session))
            if session['min_age_limit'] < 45 and session['available_capacity'] > 0:
                open_18_sessions.append(session)
                print(center_name)
                print('FINALLY!')
        open_centers[center_name] = open_sessions
    return open_centers


# if __name__ == '__main__':
#
#     district_id = 240
#     date = '02-05-2021'
#     # for i in range(1, 737):
#     # district_id = i
#     response_json = get_json(district_id, date)
#     parse_response_json(response_json)
