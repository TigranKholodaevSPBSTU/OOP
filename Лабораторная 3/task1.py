import doctest


class Book:
    """ Базовый класс книги.
    Примеры:
    >>> book = Book('Пикник на обочине', "Братья Стругацкие")  # инициализация экземпляра класса
     """
    def __init__(self, name: str, author: str):
        self.name = name
        self.author = author

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author

    def __str__(self):
        return f"Книга '{self.name}'. Автор {self.author}"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, author={self.author!r})"


class PaperBook(Book):
    """ Дочерний класс аудиокниги
       Примеры:
    >>> paper_book = PaperBook('Пикник на обочине', "Братья Стругацкие", 250)  # инициализация экземпляра класса
    """
    def __init__(self, name: str, author: str, pages: int):
        super().__init__(name, author)
        self.pages = pages

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, pages: int):
        if not isinstance(pages, int):
            raise TypeError
        if pages <= 0:
            raise ValueError
        self._pages = pages

    def __str__(self):
        return f"Книга '{self.name}'. Автор {self.author}. Количество страниц - {self.pages} стр."

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, author={self.author!r}, pages={self.pages!r})"


class AudioBook(Book):
    """ Дочерний класс аудиокниги
        Примеры:
        >>> audio_book = AudioBook('Пикник на обочине', "Братья Стругацкие", 123.4)  # инициализация экземпляра класса
    """

    def __init__(self, name: str, author: str, duration: float):
        super().__init__(name, author)
        self.duration = duration

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration: float):
        if not isinstance(duration, float):
            raise TypeError
        if duration <= 0:
            raise ValueError
        self._duration = duration

    def __str__(self):
        return f"Аудиокнига '{self.name}'. Автор {self.author}. Длительность {self.duration} мин."

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, author={self.author!r}, duration={self.duration!r})"


if __name__ == "__main__":
    doctest.testmod()
    print(Book('Пикник на обочине', "Братья Стругацкие").__str__())
    print(PaperBook('Пикник на обочине', "Братья Стругацкие", 250).__str__())
    print(AudioBook('Пикник на обочине', "Братья Стругацкие", 191.6).__str__())

    print(Book('Пикник на обочине', "Братья Стругацкие").__repr__())
    print(PaperBook('Пикник на обочине', "Братья Стругацкие", 250).__repr__())
    print(AudioBook('Пикник на обочине', "Братья Стругацкие", 191.6).__repr__())
