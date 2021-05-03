import datetime
import logging
import requests
from flask import Flask, request, render_template, redirect, url_for, session
from datetime import date

app = Flask(__name__)
app.secret_key = "super secret key"

log = logging.getLogger('cowin_script')
logging.basicConfig(level=logging.INFO)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def get_values():
    email = request.form['inputEmail']
    phone = request.form['inputPhone']
    age = request.form['inputAge']
    district = request.form['inputDistrict']
    data = {'email': email, 'phone': phone, 'age': age, 'district': district}
    session['data'] = data
    log.info(session['data'])
    return redirect(url_for('cowin'))


@app.route('/cowin', methods=['GET', 'POST'])
def cowin():
    # district_id = request.args['district_id']
    # date = request.args['date']
    today = datetime.date.today()
    date_today = today.strftime("%d-%m-%Y")
    log.info('  DATE  ' + str(date_today))
    data = session['data']
    log.info('  SESSION DATA  ' + str(data))
    response_json_dict = get_json(data['district'], date_today)
    final_dict_open = parse_response_json(response_json_dict)
    return final_dict_open


def get_json(district_id, date):
    response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
                            '?district_id={district_id}&date={date}'.format(district_id=district_id, date=date))
    response_json_dict = response.json()
    log.info('  STATUS_CODE  ' + str(response.status_code))
    return response_json_dict


def parse_response_json(response_json):
    list_centers = response_json['centers']
    total_centers = len(list_centers)
    log.info('  TOTAL CENTERS IN DISTRICT  ' + str(total_centers))
    open_centers = {}
    data = session['data']
    for center in list_centers:
        center_name = center['name']
        center_sessions = center['sessions']
        open_sessions = []
        flag = False
        for session_of_center in center_sessions:
            if session_of_center['available_capacity'] > 0 and int(session_of_center['min_age_limit']) == int(data['age']):
                flag = True
                open_sessions.append(session_of_center)
        if flag:
            open_centers[center_name] = open_sessions
    if len(open_centers) == 0:
        return "Sorry! No centers available right now"
    return open_centers


if __name__ == '__main__':
    app.debug = True
    app.run()
