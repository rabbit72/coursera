import os.path
import tempfile


class File:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return str(self.path)

    def __add__(self, other):
        # находим имя файла 1
        _, file_name = os.path.split(self.path)

        # находим путь к временной директории
        folder_path = tempfile.gettempdir()

        # создаем путь для новго файла с именем файла 1 во временной директории
        new_path = os.path.join(folder_path, file_name)

        # создаем объект класса File для результата сложения
        new_file = type(self)(new_path)

        # читаем файл 1 и файл 2 и складываем содержимое
        temp_string = self.read() + other.read()

        # пишем слитые данные в новый файл
        new_file.write(temp_string)

        return new_file

    def __iter__(self):
        return open(self.path)

    def __next__(self):
        return next()

    def write(self, string):
        with open(self.path, 'w') as f:
            f.write(string)

    def read(self):
        with open(self.path) as f:
            return f.read()


if __name__ == '__main__':
    file_1 = File('C:\\Py\\coursera\\File\\test1.txt')
    file_2 = File('C:\\Py\\coursera\\File\\test2.txt')
    file_1.write('555\n555\n555\n')
    file_3 = file_1 + file_2
    r = []
    for n in file_3:
        r.append(n)
    print(r)
