import socket
import time
import pickle

from dnslib import DNSRecord, RCODE

TRUST_SERVER = "8.8.8.8"


class DNSServer:
    def __init__(self):
        self.cache = {}
        self.cache_path = "cache.pickle"

    def load_cache(self):
        try:
            with open(self.cache_path, "rb") as f:
                print('Подгрузили кэш')
                data = pickle.load(f)
                for key, (records, expiry) in data.items():
                    if time.time() < expiry:
                        self.cache[key] = (records, expiry)
        except FileNotFoundError:
            print("Кэш пустой")

    def save_cache(self):
        with open(self.cache_path, "wb") as f:
            pickle.dump(self.cache, f)

    def update_cache(self, key, records, ttl):
        expiry = time.time() + ttl
        self.cache[key] = (records, expiry)

    def get_cached_records(self, key):
        records_data = self.cache.get(key)
        if records_data:
            records, expiry = records_data
            if time.time() < expiry:
                return records
            del self.cache[key]
        return None

    def search_cached_records(self, query_key, query):
        cached_records = self.get_cached_records(query_key)
        if cached_records:
            response_record = DNSRecord(header=query.header)
            response_record.add_question(query.q)
            response_record.rr.extend(cached_records)
            for rr_section in (response_record.rr, response_record.auth, response_record.ar):
                for rr in rr_section:
                    print(f"Найденные записи в кэше:\n{rr}", end="\n\n")
            return response_record.pack()
        return None

    def send_request_update_cache(self, query_data):
        try:
            query = DNSRecord.parse(query_data)
            response = query.send(TRUST_SERVER, 53, timeout=5)
            response_record = DNSRecord.parse(response)

            if response_record.header.rcode == RCODE.NOERROR:
                records_by_type = {}
                for rr_section in (response_record.rr, response_record.auth, response_record.ar):
                    for rr in rr_section:
                        if (rr.rtype, rr.rname) not in records_by_type:
                            records_by_type[(rr.rtype, rr.rname)] = []
                        records_by_type[(rr.rtype, rr.rname)].append(rr)
                        print(f"Кэшированные записи:\n{rr}", end="\n\n")
                        self.update_cache((rr.rtype, rr.rname), records_by_type[(rr.rtype, rr.rname)], rr.ttl)

                return response
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def resolve_query(self, query_data):
        try:
            query = DNSRecord.parse(query_data)
            query_key = (query.q.qtype, query.q.qname)
            cached_response = self.search_cached_records(query_key, query)
            if cached_response:
                return cached_response
            response = self.send_request_update_cache(query_data)
            if response:
                return response

            return None
        except Exception as e:
            print(f"Error: {e}")
            return None


if __name__ == "__main__":
    dns_server = DNSServer()
    dns_server.load_cache()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 53))
    print("DNS-сервер запущен...")

    while True:
        query_data, addr = server_socket.recvfrom(512)
        if 'exit' in query_data.decode().strip():
            print('Кэш сохранён')
            print("Выключение сервера...")
            dns_server.save_cache()
            server_socket.close()
            break
        response_data = dns_server.resolve_query(query_data)
        if response_data:
            server_socket.sendto(response_data, addr)
