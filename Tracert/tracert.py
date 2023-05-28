import json
import re
import subprocess
from urllib import request

from prettytable import PrettyTable


def is_completed(data):
    return 'Trace complete' in data \
           or 'Трассировка завершена' in data


def is_timed_out(data):
    return 'Request timed out' in data \
           or 'Превышен интервал ожидания' in data


def is_beginning(data):
    return 'Tracing route' in data \
           or 'Трассировка маршрута' in data


def is_invalid_input(data):
    return 'Unable to resolve' in data \
           or 'Не удается разрешить' in data


def generate_table():
    empty_table = PrettyTable()
    empty_table.field_names = ["number", "ip", "country", "AS Number", "provider"]
    return empty_table


def get_args(count, info):
    try:
        as_number = info['org'].split()[0][2::]
        provider = " ".join(info['org'].split()[1::])
    except KeyError:
        as_number, provider = '*', '*'
    return [f"{count}.", info['ip'], info['country'], as_number, provider]


def trace(addr, table):
    trac_proc = subprocess.Popen(["tracert", addr], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    counter = 0

    for raw_line in iter(trac_proc.stdout.readline, ''):
        line = raw_line.decode('cp866')
        ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)

        if is_completed(line):
            return table
        if is_invalid_input(line):
            print('Invalid input')
            return
        if is_beginning(line):
            continue
        if is_timed_out(line):
            print('timed out')
            continue
        if ip:
            counter += 1
            info = json.loads(request.urlopen('https://ipinfo.io/' + ip[0] + '/json').read())
            if 'bogon' in info:
                table.add_row([f"{counter}.", info['ip'], '*', '*', '*'])
            else:
                table.add_row(get_args(counter, info))
    return table


if __name__ == '__main__':
    address = input("Enter Address: ")
    table = generate_table()
    print(trace(address, table))
