import math
import doctest
from typing import Union


class Spillway:
    """
    Документация на класс Spillway
    Класс описывает модель водосбросного сооружения на гидроэлектростанции.
    Размерности единиц - метры, секунды.
    Обозначения некоторых атрибутов и переменных приняты не по PEP8 из-за общепринятых научных обозначений
    Атрибут класса g=9,81 м/с2 - константа - наследуется всеми дочерними классами
    """
    g = 9.81

    def __init__(self, m: Union[float, int], H: Union[float, int], NE: Union[float, int]):
        """
        Инициализация экземпляра класса. Атрибуты экземпляра класса:
        :param m: Коэффициент расхода, безразмерная величина от 0 до 1 не включительно
        :param H: Hydraulic Head - гидравлический напор, м
        :param NE: Normal elevation - нормальный подпорный уровень, м

        Примеры:
        >>> test = Spillway(0.35, 10, 142)  # инициализация экземпляра класса
        """
        if not isinstance(m, Union[float, int]):
            raise TypeError
        if not 0 < m < 1:
            raise ValueError
        self.m = m
        if not isinstance(H, Union[Union[float, int], int]):
            raise TypeError
        if not H > 0:
            raise ValueError
        self.H = H
        if not isinstance(NE, Union[float, int]):
            raise TypeError
        if not 8848 > NE > 0:
            raise ValueError
        self.NE = NE

    def __str__(self) -> str:
        """
        Метод экземляра класса, который возврщает строковое представление описание объекта,
        предназначенное для чтения пользователем.

        return: Водосброс с коэффициентом расхода m=0.35 при напоре H=10 м
        """
        return f"Водосброс с коэффициентом расхода m={self.m} при напоре H={self.H} м"

    def __repr__(self) -> str:
        """
        Метод экземляра класса, который возврщает строковое представление инициализации объекта,
        предназначенное для чтения машинным кодом.

        return: Spillway(m=0.35, H=10)
        """
        return f'{self.__class__.__name__}(m={self.m!r}, H={self.H!r})'

    def get_crest_level(self) -> Union[float, int]:
        """
        Метод экземпляра класса, который возвращает отметку гребня водосливной поверхности по NE и H
        Метод наследуется всеми дочерними классами.
        """
        crest_level = self.NE - self.H
        return crest_level

    @staticmethod
    def is_safe(Q_max: Union[float, int], Q: Union[float, int]) -> str:
        """
        Статический метод, который проверяет условие пропускной способности. Принимает аргументы:
        :arg Q_max: Максимальный расход через водосброс
        :arg Q: пропускная способность водосброса. Для дочерних классов вычисляется
        с помощью метода .get_carrying_capacity()
        Метод наследуется всеми дочерними классами
        """
        if Q_max > Q:
            return "Условие не выполняется"
        return "Условие выполняется"


class CircleSpillway(Spillway):
    """
    Документация на дочерний класс CircleSpillway(Spillway)
    Класс описывает модель кольцевого водослива.
    В данном классе унаследован и дополнен конструктор базового класса, перегружены методы __str__ и __repr__, так как
    изменилась логика инициализации экземпляра класса. Унаследованы метод экземпляра класса .get_crest_level
    и статический метод .is_safe.
    Размерности единиц - метры, секунды.
    Обозначения некоторых атрибутов и переменных приняты не по PEP8 из-за общепринятых научных обозначений
    """

    def __init__(self, m: Union[float, int], H: Union[float, int], NE: Union[float, int],
                 R: Union[float, int], S: Union[float, int], n: int):
        """Инициализация экземпляра класса. Атрибуты экземпляра класса:
        :param m: Коэффициент расхода, безразмерная величина от 0 до 1 не включительно
        :param H: Hydraulic Head - гидравлический напор, м
        :param NE: Normal elevation - нормальный подпорный уровень, м
        :param R: радиус водосливной воронки, м
        :param S: толщина быка - разделительной стенки, м
        :param n: количество быков
        Примеры:
        >>> test = CircleSpillway(0.35, 10, 142, 10, 3, 0)  # инициализация экземпляра класса
        """
        super().__init__(m, H, NE)
        if not isinstance(R, Union[float, int]):
            raise TypeError
        if not R > 0:
            raise ValueError
        self.R = R
        if not isinstance(S, Union[float, int]):
            raise TypeError
        if not S > 0:
            raise ValueError
        self.S = S
        if not isinstance(n, int):
            raise TypeError
        if not n >= 0:
            raise ValueError
        self.n = n

    def __str__(self) -> str:
        """
        Метод экземляра класса, который возврщает строковое представление описание объекта, предназначенное для чтения
        пользователем. Метод перегружен из базового класса.
        return: Кольцевой водосброс радиусом R=10 м при напоре H=10 м. Количество быков n=0, толщина быка S=3
        """
        return f"Кольцевой водосброс радиусом R={self.R} м при напоре H={self.H} м. " \
               f"Количество быков n={self.n}, толщина быка S={self.S}"

    def __repr__(self) -> str:
        """
        Метод экземляра класса, который возврщает строковое представление инициализации объекта, предназначенное для
        чтения машинным кодом. Метод перегружен из базового класса.

        return: CircleSpillway(m=0.49, H=5, NE=142, R=10, S=3, n=0)
        """
        return f'{self.__class__.__name__}(m={self.m!r}, H={self.H!r}, NE={self.NE!r}, R={self.R!r}, ' \
               f'S={self.S!r}, n={self.n!r})'

    def get_carrying_capacity(self) -> Union[float, int]:
        """
        Метод экземпляра класса, который возвращает значение пропускной способности кольцевого водослива в м3/с.
        Для других дочерних классов расчет ведется по аналогичной формуле, но с другими значениями w - площади
        водосливного фронта
        """
        w = (2 * math.pi * self.R - self.n * self.S) * self.H
        Q = self.m * w * math.sqrt(2 * Spillway.g * self.H)
        return Q


class NormalSpillway(Spillway):
    """
    Документация на дочерний класс NormalSpillway(Spillway)
    Класс описывает модель водослива с нормальным подводом воды с прямоугольными отверстиями.
    В данном классе унаследован и дополнен конструктор базового класса, перегружены методы __str__ и __repr__, так как
    изменилась логика инициализации экземпляра класса. Унаследованы метод экземпляра класса .get_crest_level
    и статический метод .is_safe.
    Размерности единиц - метры, секунды.
    Обозначения некоторых атрибутов и переменных приняты не по PEP8 из-за общепринятых научных обозначений
    """

    def __init__(self, m: Union[float, int], H: Union[float, int], NE: Union[float, int], b: Union[float, int], n: int):
        """Инициализация экземпляра класса. Атрибуты экземпляра класса:
        :param m: Коэффициент расхода, безразмерная величина от 0 до 1 не включительно
        :param H: Hydraulic Head - гидравлический напор, м
        :param NE: Normal elevation - нормальный подпорный уровень, м
        :param b: ширина отверсия, м
        :param n: количество быков
        Примеры:
        >>> test = NormalSpillway(0.35, 4, 142, 12, 5)  # инициализация экземпляра класса
        """
        super().__init__(m, H, NE)
        if not isinstance(b, Union[float, int]):
            raise TypeError
        if not b > 0:
            raise ValueError
        self.b = b
        if not isinstance(n, int):
            raise TypeError
        if not n > 0:
            raise ValueError
        self.n = n

    def __str__(self) -> str:
        """
        Метод экземляра класса, который возврщает строковое представление описание объекта, предназначенное для чтения
        пользователем. Метод перегружен из базового класса.
        return: Водосброс с нормальным подводом воды с количеством водопропускных отверстий n=5
        при ширине отверстия b=12 м, при напоре H=4 м
        """
        return f"Водосброс с нормальным подводом воды с количеством водопропускных отверстий n={self.n} " \
               f"при ширине отверстия b={self.b} м, при напоре H={self.H} м"

    def __repr__(self) -> str:
        """
        Метод экземляра класса, который возврщает строковое представление инициализации объекта, предназначенное для
        чтения машинным кодом. Метод перегружен из базового класса.
        return: NormalSpillway(m=0.49, H=5, NE=142, b=12, n=5)
        """
        return f'{self.__class__.__name__}(m={self.m!r}, H={self.H!r}, NE={self.NE!r}, b={self.b!r}, n={self.n!r})'

    def get_carrying_capacity(self) -> Union[float, int]:
        """
        Метод экземпляра класса, который возвращает значение пропускной способности кольцевого водослива в м3/с.
        Для других дочерних классов расчет ведется по аналогичной формуле, но с другими значениями w - площади
        водосливного фронта
        """
        w = self.n * self.b * self.H
        Q = self.m * w * math.sqrt(2 * Spillway.g * self.H)
        return Q


if __name__ == "__main__":
    test3 = Spillway(0.35, 10.0, 142.0)
    test5 = NormalSpillway(0.32, 4.0, 142.0, 12.0, 5)
    test1 = CircleSpillway(0.49, 5.0, 142.0, 10.0, 3, 0)
    doctest.testmod()

    print(test5.__str__())
    print(test1.get_carrying_capacity())
    print(test1.__repr__())
