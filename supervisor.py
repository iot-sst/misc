import os
import psutil
from collections import namedtuple

import requests
import mysql.connector

# [DATABASE]
SQL_DATABASE = 'ilsdb'
SQL_USER = 'greenlamp'
SQL_PASSWORD = 'greenlamp'
SQL_HOST = 'localhost'

Param = namedtuple('Param', 'default_value description units')

parameters = {
    1: Param('255', 'Address RF', ''),
    2: Param('30', 'Interval between measurements', '(sec.)'),
    3: Param('30', 'Base Presence Time Window', '(sec.)'),
    4: Param('7', 'Day Period - Start Time', '(Hour)'),
    5: Param('19', 'Post-Work Period - Start Time', '(Hour)'),
    6: Param('21', 'Night Period - Start Time', '(Hour)'),
    7: Param('0', 'Minimum time on', '(sec.)'),
    8: Param('100', 'Daylight Period - Maximum brightness level', '%'),
    9: Param('0', 'Daytime Period - Courtesy Level', '%'),
    10: Param('100', 'Post-Work Period - Maximum brightness level', '%'),
    11: Param('0', 'Post-Work Period - Level of courtesy', '%'),
    12: Param('100', 'Night Period - Maximum brightness level', '%'),
    13: Param('0', 'Night Period - Courtesy Level', '%'),
    14: Param('100', 'Daylight Period - Maximum brightness level', '%'),
    15: Param('0', 'Daytime Period - Courtesy Level', '%'),
    16: Param('100', 'Post-Work Period - Maximum brightness level', '%'),
    17: Param('0', 'Post-employment period - level of courtesy', '%'),
    18: Param('100', 'Night Period - Maximum brightness level', '%'),
    19: Param('0', 'Night Period - Courtesy Level', '%'),
    20: Param('40', 'LDR Lower Limit', '%'),
    21: Param('90', 'LDR Upper Limit', '%'),
    22: Param('12345', 'Network Key', ''),
    23: Param('12345', 'Network connection key', ''),
    24: Param('0', 'Access - Reverse direction', ''),
    25: Param('10', 'ON time after PIR time', '(sec.)'),
    26: Param('28800', 'Maximum time in manual mode', '(sec.)'),
    27: Param('0', '[Send] Other sensor: Light - Presence', ''),
    28: Param('0', 'RF Channel', ''),
    29: Param('0', '[Receives] Remote light sensor', ''),
    30: Param('0', 'Daytime - Temporary presence window', '(sec.)'),
    31: Param('0', 'Post-employment period - Temporary presence window', '(sec.)'),
    32: Param('0', 'Night Period - Presence Time Window', '(sec.)'),
    33: Param('0', 'Daytime - Temporary presence window', '(sec.)'),
    34: Param('0', 'Post-employment period - Temporary presence window', '(sec.)'),
    35: Param('0', 'Night Period - Presence Time Window', '(sec.)'),
    36: Param('0', 'Internal temperature sensor offset', '(C)'),
    37: Param('0', 'Hysteresis', '%'),
    38: Param('1', 'Relay Inverter', ''),
    39: Param('15', 'Notice board', '')
}


def set_param(device_id, param_id, value):
    param = parameters.get(param_id)
    if param:
        print('Device {} set param <{}> to value {}'.format(device_id, param.description, value))
        url = 'http://127.0.0.1/end_devices/{}/configuration'.format(device_id)
        values = [{'param_id': str(param_id), 'param_value': str(value)}]
        cfg = {'end_device_id': device_id, 'configuration': values}
        response = requests.post(url, headers={'X-Requested-With': 'XMLHttpRequest'}, json=cfg)
        if response:
            print('Done')
        else:
            print('Error set parameters')
    else:
        print('Parameter not founded.')


def get_version(device_id):
    url = 'http://127.0.0.1/end_devices/{}/version'.format(device_id)
    response = requests.get(url, headers={'X-Requested-With': 'XMLHttpRequest'})
    if response:
        if response.status_code == 200:
            print('{}'.format(response.text))
        else:
            print('Error: Timeout.')
    else:
        print('Error: Fail get version')


def get_all_devices():
    all_ids = []
    db_connection = _connect_to_database()
    if db_connection is None:
        return False
    query = 'SELECT id FROM ilsdb.end_devices'
    cursor = None

    try:
        # Create prepared statement
        cursor = db_connection.cursor(prepared=True)
        cursor.execute(query)
        for id in cursor:
            if id[0] != 254:
                all_ids += id
    except mysql.connector.OperationalError:
        print("Could not register configuration. (Connection lost)")
        return all_ids
    except mysql.connector.Error:
        print("Could not register configuration.")
        return all_ids
    finally:
        if cursor is not None:
            cursor.close()
        db_connection.close()
        return all_ids


def _connect_to_database():
    db_connection = None

    try:
        db_connection = mysql.connector.connect(
            user=SQL_USER,
            password=SQL_PASSWORD,
            host=SQL_HOST,
            database=SQL_DATABASE
        )
    except mysql.connector.Error:
        print('Could not connect to database.')
    return db_connection


def get_free_space():
    disk = psutil.disk_usage('/')
    disk_total = disk.total / 2 ** 30
    disk_used = disk.used / 2 ** 30
    disk_free = disk.free / 2 ** 30
    disk_percent_used = disk.percent
    return 100 - disk.percent


if __name__ == '__main__':
    # all_devices = [1, 2, 3, 4, 5, 6]
    print('Start')
    print('============================')
    print('Disk free: {}%'.format(get_free_space()))
    # stream = os.popen('df -h')
    # output = stream.read().splitlines()
    # for l in output:
    #     if l.endswith('/'):
    #         ll = l.split()
    #         print('Used space:', ll[4])
    print('============================')
    all_devices = get_all_devices()
    print('Devices Id:', all_devices)
    for id in all_devices:
        print('Get version for device', id, end=':')
        get_version(id)
        # print('Set parameter for device ', id)
        # set_param(id, 2, 2*60)
    print('============================')
    print('End')
