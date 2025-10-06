import socket


class EchoClient:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def send_message(self, message):
        try:
            # Создаем сокет и подключаемся к серверу
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))

            # Отправляем сообщение
            client_socket.send(message.encode('utf-8'))
            print(f"Отправлено серверу: {message}")

            # Получаем ответ
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Получено от сервера: {response}")

        except Exception as e:
            print(f"Ошибка клиента: {e}")
        finally:
            client_socket.close()


if __name__ == "__main__":
    client = EchoClient()

    # Тестируем базовое эхо
    message = input("Введите сообщение для отправки: ")
    client.send_message(message)