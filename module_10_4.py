import threading
import time
import random
import queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(random.randint(1, 2))  #Сделал меньше задержку


class Cafe:
    def __init__(self, *tables):
        self.queue = queue.Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for i in guests:
            for j in self.tables:
                if j.guest is None:
                    j.guest = i
                    i.start()
                    print(f'{i.name} сел(-а) за стол номер {j.number}')
                    break
            else:
                self.queue.put(i)
                print(f'{i.name} в очереди')

    def discuss_guests(self):
        while any(table.guest is not None for table in self.tables) or not self.queue.empty():
            for i in self.tables:
                if i.guest is not None and not i.guest.is_alive():
                    print(f'{i.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {i.number} свободен')
                    i.guest = None
                if not self.queue.empty() and i.guest is None:
                    i.guest = self.queue.get()
                    print(f'{i.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {i.number}')
                    i.guest.start()


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman', 'Vitoria', 'Nikita', 'Galina',
                'Pavel', 'Ilya', 'Alexandra']
# Создание гостей
guests = [Guest(name) for name in guests_names]
# print(guests))
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()

print("Все столы свободны, посетителей нет!")
