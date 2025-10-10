import socket
import time


class AdvancedEchoClient:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def start_session(self):
        try:
            # Создаем сокет и подключаемся к серверу
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)  # Таймаут 5 секунд на приём данных
            client_socket.connect((self.host, self.port))

            print(f"Подключено к серверу {self.host}:{self.port}")
            print("Введите сообщения (для выхода введите 'exit'):")

            with client_socket:
                while True:
                    message = input("> ").strip()

                    # Отправляем сообщение серверу
                    if not message:
                        continue
                    client_socket.send(message.encode('utf-8'))

                    # Проверяем команду выхода
                    if message.lower() == 'exit':
                        print("Завершение сессии...")
                        break

                    # Получаем ответ от сервера
                    try:
                        response = client_socket.recv(1024).decode('utf-8')
                        print(f"Сервер: {response}")
                    except socket.timeout:
                        print("Таймаут при ожидании ответа от сервера (5 секунд)")
                        break

                    time.sleep(0.1)

        except ConnectionRefusedError:
            print(f"Не удалось подключиться к серверу {self.host}:{self.port}")
        except Exception as e:
            print(f"Ошибка клиента: {e}")


if __name__ == "__main__":
    client = AdvancedEchoClient()
    client.start_session()
