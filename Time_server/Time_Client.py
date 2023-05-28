import socket
from datetime import datetime


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 123)

    # Отправка запроса на получение времени
    udp_socket.sendto(b"TimeRequest", server_address)

    # Получение ответа от сервера
    data, server = udp_socket.recvfrom(1024)
    print("Получен ответ от сервера:")
    time_value = float(data.decode())
    datetime_value = datetime.fromtimestamp(time_value)

    print("Дата и время:", datetime_value)

    udp_socket.close()


if __name__ == '__main__':
    main()