import threading
import time
import random
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None  # Гость, сидящий за столом (по умолчанию None)

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        # Имитация времени, проведенного за столом от 3 до 10 секунд
        time.sleep(random.randint(3, 10))

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()  # Очередь гостей
        self.tables = list(tables)  # Список столов

    def guest_arrival(self, *guests):
        """
        Метод принимает неограниченное количество гостей.
        Сажает их за свободные столы или ставит в очередь, если все столы заняты.
        """
        for guest in guests:
            table_found = False
            for table in self.tables:
                if table.guest is None:
                    # Нашли свободный стол, садим гостя и запускаем его поток
                    table.guest = guest
                    guest.start()
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    table_found = True
                    break
            if not table_found:
                # Все столы заняты, добавляем гостя в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        """
        Метод обслуживания гостей.
        Проверяет завершение приема пищи и освобождает столы.
        Если есть гости в очереди, они занимают освободившиеся столы.
        """
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None:
                    if not table.guest.is_alive():
                        # Гость завершил прием пищи
                        print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                        print(f"Стол номер {table.number} свободен")
                        table.guest = None  # Освобождаем стол

                        # Проверяем, есть ли гости в очереди, чтобы занять освободившийся стол
                        if not self.queue.empty():
                            next_guest = self.queue.get()
                            table.guest = next_guest
                            next_guest.start()  # Запускаем поток нового гостя
                            print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
            time.sleep(1)  # Небольшая пауза для имитации процесса обслуживания

# Пример выполнения программы:
# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Прием гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
