import socket
import threading


def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((ip, port))
            print(f'TCP PORT: {port} открыт.')
            sock.close()
        except:
            pass


def scan_tcp_ports(ip, left, right):
    threads = []
    for port in range(left, right + 1):
        t = threading.Thread(target=scan_port, args=(ip, port))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


def main():
    host = input('Адрес хоста: ')
    left, right = input('Диапазон: ').split('-')
    print("Сканирование портов началось")
    scan_tcp_ports(host, int(left), int(right))
    print('Сканирование портов завершено')


if __name__ == '__main__':
    main()
