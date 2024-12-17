from typing import Self


class ObjList:
    def __init__(self, data: str) -> None:
        self.__data = data
        self.__next = None
        self.__prev = None

    def set_next(self, obj: Self) -> None:
        """Изменение следующего узла"""
        self.__next = obj

    def set_prev(self, obj: Self) -> None:
        """Изменение предыдущего узла"""
        self.__prev = obj

    def get_next(self) -> Self:
        """Получение следующего узла"""
        return self.__next

    def get_prev(self) -> Self:
        """Получение предыдущего узла"""
        return self.__prev

    def set_data(self, data: str) -> None:
        """Добавление данных узла"""
        self.__data = data

    def get_data(self) -> str:
        """Получение узла"""
        return f'{self.__data}' if self.__data else ''


class LinkedList:
    def __init__(self) -> None:
        self.head = None
        self.tail = None

    def add_obj(self, obj: ObjList) -> str:
        """Добавление объекта в конец двухсвязного списка"""
        new_obj = obj

        if self.head is None:
            self.head = new_obj
            self.tail = new_obj
        else:
            self.tail.set_next(new_obj)
            new_obj.set_prev(self.tail)
            self.tail = new_obj
        return f'Новый объект "{new_obj.get_data()}" добавлен в список'

    def remove_obj(self) -> str:
        """Удаление объекта с конца двухсвязного списка"""
        if self.tail is None:
            return 'Удаление невозможно. Список пуст.'
        elif self.head == self.tail:
            self.tail.set_data(None)
            self.head = None
            self.tail = None
        else:
            new_tail = self.tail.get_prev()
            self.tail.set_data(None)
            self.tail = new_tail

        return f'Объект успешно удален'

    def get_data(self) -> list[ObjList]:
        """Получение всех объектов двухсвязного списка"""
        result = list()
        obj = self.head

        while obj:
            if obj.get_data():
                result.append(obj.get_data())
            obj = obj.get_next()
        return result
