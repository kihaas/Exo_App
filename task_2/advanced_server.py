import socket
import threading
import logging


class AdvancedEchoServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Настройка логирования
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def start(self):
        """Запуск сервера"""
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.logger.info(f"Сервер запущен на {self.host}:{self.port}")
            self.logger.info("Ожидание подключений...")

            while True:
                client_socket, client_address = self.socket.accept()
                self.logger.info(f"Подключен клиент: {client_address}")

                # Обрабатываем каждого клиента в отдельном потоке
                client_thread = threading.Thread(
                    target=self.handle_client_connection,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()

        except KeyboardInterrupt:
            self.logger.info("Получен сигнал прерывания")
        except Exception as e:
            self.logger.error(f"Ошибка сервера: {e}")
        finally:
            self.stop()

    def handle_client_connection(self, client_socket, client_address):
        try:
            with client_socket:
                self.handle_client_messages(client_socket, client_address)

        except ConnectionResetError:
            self.logger.warning(f"Клиент {client_address} разорвал соединение")
        except Exception as e:
            self.logger.error(f"Ошибка при работе с клиентом {client_address}: {e}")
        finally:
            self.logger.info(f"Соединение с {client_address} закрыто")

    def handle_client_messages(self, client_socket, client_address):
        client_socket.settimeout(30.0)  # Таймаут 30 секунд

        while True:
            try:
                # Получаем сообщение от клиента
                data = client_socket.recv(1024).decode('utf-8')

                # Проверяем, не закрыл ли клиент соединение
                if not data:
                    self.logger.info(f"Клиент {client_address} закрыл соединение")
                    break

                self.logger.info(f"Получено от {client_address}: {data}")

                # Проверяем команду выхода
                if data.strip().lower() == 'exit':
                    self.logger.info(f"Клиент {client_address} запросил отключение")
                    client_socket.send("До свидания! Соединение закрыто.".encode('utf-8'))
                    break

                # Отправляем эхо-ответ
                response = f"ECHO: {data}"
                client_socket.send(response.encode('utf-8'))
                self.logger.info(f"Отправлено {client_address}: {response}")

            except socket.timeout:
                self.logger.warning(f"Таймаут для клиента {client_address}")
                client_socket.send("Таймаут: соединение будет закрыто".encode('utf-8'))
                break
            except ConnectionResetError:
                self.logger.warning(f"Клиент {client_address} разорвал соединение")
                break
            except Exception as e:
                self.logger.error(f"Ошибка при обработке сообщения от {client_address}: {e}")
                break

    def stop(self):
        self.socket.close()
        self.logger.info("Сервер остановлен")


if __name__ == "__main__":
    server = AdvancedEchoServer()
    server.start()