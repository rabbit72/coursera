import csv
import os.path
import sys


class CarBase:
    """Базовый класс с атрибутами и методами"""
    #  константы соотвествия колонок и значениям в них
    ix_car_type = 0
    ix_brand = 1
    ix_passenger_seats_count = 2
    ix_photo_file_name = 3
    ix_body_whl = 4
    ix_carrying = 5
    ix_extra = 6

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)

    def __str__(self):
        return f'Car(' \
               f'{self.brand}, ' \
               f'{self.photo_file_name}, ' \
               f'{self.carrying}, ' \
               f'{self.passenger_seats_count})'

    __repr__ = __str__

    @classmethod
    def create(cls, auto):
        return cls(
            auto[cls.ix_brand],
            auto[cls.ix_photo_file_name],
            auto[cls.ix_carrying],
            auto[cls.ix_passenger_seats_count]
        )


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        # обрабатываем поле body_whl
        try:
            width, height, length = (float(c) for c in body_whl.split('x', 2))
        except ValueError:
            width, height, length = .0, .0, .0

        self.body_width = width
        self.body_height = height
        self.body_length = length

    def __str__(self):
        return f'Truck(' \
               f'{self.brand}, ' \
               f'{self.photo_file_name}, ' \
               f'{self.carrying}, ' \
               f'{self.body_width}x{self.body_height}x{self.body_length})'

    __repr__ = __str__

    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width

    @classmethod
    def create(cls, auto):
        return cls(
            auto[cls.ix_brand],
            auto[cls.ix_photo_file_name],
            auto[cls.ix_carrying],
            auto[cls.ix_body_whl]
        )


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    def __str__(self):
        return f'SpecMachine(' \
               f'{self.brand}, ' \
               f'{self.photo_file_name}, ' \
               f'{self.carrying}, ' \
               f'{self.extra})'

    __repr__ = __str__

    @classmethod
    def create(cls, auto):
        return cls(
            auto[cls.ix_brand],
            auto[cls.ix_photo_file_name],
            auto[cls.ix_carrying],
            auto[cls.ix_extra]
        )


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename, 'r', encoding='utf8') as csv_f:
        reader = csv.reader(csv_f, delimiter=';')
        next(reader)  # пропускаем заголовок

        create_class = {car_class.car_type: car_class for car_class in (Car, Truck, SpecMachine)}

        # обрабатываем csv-файл построчно
        for auto in reader:
            try:
                #  определить тип автомобиля
                car_type = auto[CarBase.ix_car_type]
            except IndexError:
                # игнорировать строку, если нехватает колонок
                continue

            try:
                #  узнаем класс объекта, который нужно создать
                car_class = create_class[car_type]
            except KeyError:
                # если класс неизвестен - пропускай строку
                continue

            try:
                car_list.append(car_class.create(auto))
            except (ValueError, IndexError):
                # если данные некорректны, то просто игнорируем
                pass

    return car_list


if __name__ == "__main__":
    print(get_car_list('cars.csv'))
    truck = Truck('toyota', 'f8.png', 40, '2.5x2x1')
    print(truck.get_body_volume())
