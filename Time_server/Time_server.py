import json
import ntplib
import socket


def main():
    with open("config.json", "r") as file_json:
        file = json.load(file_json)
        offset_seconds = file['offset_seconds']

    # Создание UDP-сокета
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 123))

    print("Сервер точного времени запущен.")
    print(f"Отклонение времени: {offset_seconds} секунд.")

    while True:
        # Получение запроса от клиента
        data, addr = udp_socket.recvfrom(1024)
        print(f"Запрос на получение времени от {addr[0]}:{addr[1]}")

        # Получение точного времени от time.windows.com
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('time.windows.com', version=3)
        ntp_time = response.tx_time

        modified_time = ntp_time + offset_seconds
        time_bytes = str(modified_time).encode()
        udp_socket.sendto(time_bytes, addr)


if __name__ == '__main__':
    main()
