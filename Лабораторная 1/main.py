import doctest
import string
from typing import Union
MATERIALS = ['Железобетон', 'Сталь', 'Дерево']
STRENGTH_LIMIT = {"Железобетон": 140000,
                  "Сталь": 220000,
                  "Дерево": 10000,
}

class Beam():
    """
    Документация на класс Beam.
    Класс описывает модель балки прямоугольного сплошного сечения, работающей на изгиб.
    Все размеры приняты в метрах и килоньютонах.
    В идеале необходимо доработать и добавить прокатные сечения (двутавр, швеллер и т.д.),
    но возникают проблемы с инициализацией атрибутов, которые не понадобятся для разных типов сечений.
    Как я понял, это поможет решить инкапсуляция в будущем.
    """
    def __init__(self, material: str, width: Union[int, float],
                 height: Union[int, float], length: Union[int, float]):
        """
        Инициализация экземпляра класса
        :param material: Материал балки
        :param width: Ширина сечения
        :param height: Высота сечения
        :param length: Длина балки

        Примеры:
        >>> beam1 = Beam('железобетон', 0.4, 0.4, 6)  # инициализация экземпляра класса
        """
        if not material.capitalize() in MATERIALS:  #проверка входит ли запрошенная у пользователя строка в дефолтный
            # список. Альтернативный вариант - запрашивать у пользователя индекс в списке"""
            raise ValueError('Неверное имя!')
        self.material = material.capitalize()
        if not isinstance(width, (int, float)):
            raise TypeError("Ширина должна быть типа int или float")
        if width <= 0:
            raise ValueError("Ширина должна быть больше нуля")
        self.width = width
        if not isinstance(height, (int, float)):
            raise TypeError("Высота должна быть типа int или float")
        if height <= 0:
            raise ValueError("Высота должна быть больше нуля")
        self.height = height
        if not isinstance(length, (int, float)):
            raise TypeError("Длина должна быть типа int или float")
        if length <= 0:
            raise ValueError("Длина должна быть больше нуля")
        self.length = length

    def get_moment_of_resistance(self) -> (int, float):
        """
        Метод, который вычисляет момент сопротивления сечения W в м^3.

        :return: Момент сопротивления сечения в м^3
        """
        moment_of_resistance = self.width * self.height ** 2 / 6
        return moment_of_resistance

    def get_area(self) -> (int, float):
        """
        Метод, который вычисляет площадь сечения A в м^2.

        :return: Площадь сечения в м^2
        """
        area = self.width * self.height
        return area

    def get_volume(self) -> (int, float):
        """
        Метод, который вычисляет расход материала на балку.

        :return: Расход материала
        """
        volume = self.get_area() * self.length
        return volume

    def is_safe(self, moment: Union[int, float]) -> bool:
        """
        Метод, который проверяет выполняется ли условие прочности и возвращает значение True или False.
        :param moment: Изгибающий момент в кН*м

        :return: Выполняется ли условие прочности
        """
        if not isinstance(moment, (int, float)):
            raise TypeError("Момент должен быть типа int или float")
        if moment < 0: #значение изгибающего момента может передаваться отрицательным числом, что говорит лишь о
            # направлении по правилу знаков, но расчет ведется на положительное число. Также момент может быть равен нулю
            moment = abs(moment)
        return moment / self.get_moment_of_resistance() >= STRENGTH_LIMIT[self.material] #сравниваем M/W с возвращаемым
        # значением из дефолтного словаря
BORDERS_LIST = ["Нижняя", "Верхняя", "Левая", "Правая", "Все границы", "Нет границ"]
class Cell:
    """
    Документация на класс Cell.
    Класс, описывающая элемент "ячейка" в электронных таблицах.
    По умолчанию путь на ячейку указывается как "A1", где А - номер столбца (str),
    а 1 - номер строки (int)
    В первом приближении принято, что количество столбцов ограничено тремя буквами (ZZZ- последний столбец)
    Количество строк - 1048576
    Цвет ячейки определяется по индексу от 0 до 16777215
    Ширина и высота ячейки определяется в так называемых "пунктах". В дальнейшем надо разобраться с переводом в пиксели и мм.
    """
    def __init__(self, row: int, column: str, colour: int, width=8.43, height=15.00):
        """
        Инициализация экземпляра класса
        :param row: Номер строки
        :param column: Номер столбца
        :param colour: Цвет заливки ячейки
        :param width: Ширина столбца ячейки. Значение по умолчанию - 8.43 пункта
        :param height: Высота строки ячейки. Значение по умолчанию - 15.00 пунктов

        Примеры:
        >>> cell = Cell(5, 'AB', 45)  # инициализация экземпляра класса
        """
        if not isinstance(row, int):
            raise TypeError('Номер строки - целое число')
        if not 1 <= row <= 1048576:
            raise ValueError('Номер строки должен находить в диапазоне от 1 до 1048576 включительно')
        self.row = row
        for symbol in column.upper():
            if symbol not in string.ascii_uppercase:
                raise TypeError('Номер столбца - сочетание букв латинского алфавита')
        self.column = column.upper()
        if not isinstance(colour, int):
            raise TypeError("Индекс цвета - целое число")
        if not 0 <= colour <= 16777215:
            raise ValueError('Индекс цвета находится в диапазоне от 0 до 16777215 включительно')
        self.colour = colour
        if not isinstance(width, (int, float)):
            raise TypeError("Ширина должна быть типа int или float")
        if not 0 <= width <= 255:
            raise ValueError("Ширина находится в диапазоне от 0 до 255 включительно")
        self.width = round(width, 2)
        if not isinstance(height, (int, float)):
            raise TypeError("Высота должна быть типа int или float")
        if not 0 <= height <= 409:
            raise ValueError("Высота находится в диапазоне от 0 до 409 включительно")
        self.height = round(height, 2)

    def pick_cell(self) -> None:
        """
        Метод обводит выбранную ячейку прямоугольников размерами width x height
        """
        ...
    def change_width(self, width_increment: Union[int, float]) -> Union[int, float]:
        """
        Метод позволяется изменить величину ширины ячейки.
        Пользователь передает любое действительное число, программа подстраивает значение под рамки разрешенного
        диапазона
        """
        self.width = self.width + round(width_increment, 2)
        if self.width > 255:
            self.width = 255
        elif self.width < 0:
            self.width = 0
        return self.width
    def change_height(self, height_increment: Union[int, float]) -> Union[int, float]:
        """
        Метод позволяется изменить величину высоты ячейки.
        Пользователь передает любое действительное число, программа подстраивает значение под рамки разрешенного
        диапазона
        """
        self.height = self.height + round(height_increment, 2)
        if self.height > 409:
            self.height = 409
        elif self.height < 0:
            self.height = 0
        return self.height

class Lamp:
    """
    Документация на класс Lamp
    Класс, описывающий модель лампы
    """
    def __init__(self, position: bool, light_brightness: int):
        """
        Инициализация экземпляра класса
        :param position: True включена, False выключена
        :param light_brightness: Яркость света, изменяемая с помощью диммера в диапазоне от 1 до 10
        Примеры:
        >>> lamp = Lamp(True, 5)  # инициализация экземпляра класса
        """
        if not isinstance(position, bool):
            raise TypeError('Значение должно быть bool')
        self.position = position
        if not  isinstance(light_brightness, int):
            raise TypeError("Значение должно быть int")
        if not 1 <= light_brightness <= 10:
            raise ValueError('Значение не в диапазоне')
        self.light_brightness = light_brightness

    def inverse_light(self) -> bool:
        """
        Метод позволяет поменять положение выключателя на противоположное.
        Если лампа включается, автоматически устанавливается значение 1 яркости света
        """
        self.position = not self.position
        if self.position == True:
            self.light_brightness = 1
        return self.position
    def set_light_brightness(self, new_light_brightness: int) -> int:
        """
        Метод позваоляет выбрать новое значение яркости света
        """
        if not  isinstance(new_light_brightness, int):
            raise TypeError("Значение должно быть int")
        if not 1 <= new_light_brightnesslight_brightness <= 10:
            raise ValueError('Значение не в диапазоне')
        self.light_brightness = new_light_brightness
        return self.light_brightness

if __name__ == "__main__":
    doctest.testmod()
    help(Lamp)