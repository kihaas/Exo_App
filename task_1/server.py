import socket
import threading


class EchoServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print(f"Сервер запущен на {self.host}:{self.port}")
            print("Ожидание подключений...")

            while True:
                client_socket, client_address = self.socket.accept()
                print(f"Подключен клиент: {client_address}")

                # Обрабатываем каждого клиента в отдельном потоке
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()

        except Exception as e:
            print(f"Ошибка сервера: {e}")
        finally:
            self.stop()

    def handle_client(self, client_socket, client_address):
        try:
            # Получаем сообщение от клиента
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Получено от {client_address}: {data}")

            # Отправляем эхо-ответ
            response = f"ECHO: {data}"
            client_socket.send(response.encode('utf-8'))
            print(f"Отправлено {client_address}: {response}")

        except Exception as e:
            print(f"Ошибка при работе с клиентом {client_address}: {e}")
        finally:
            client_socket.close()
            print(f"Соединение с {client_address} закрыто")

    def stop(self):
        """Остановка сервера"""
        self.socket.close()
        print("Сервер остановлен")


if __name__ == "__main__":
    server = EchoServer()
    server.start()