import random
import time


class StopGameException(Exception):
    pass


class GamePole:
    def __init__(self, n: int = 10, m: int = 12) -> None:
        self.n = n
        self.m = m
        self.board = [[None] * self.n for _ in range(self.n)]
        self.init()

    def init(self) -> None:
        # Расчет координат мин
        mine_indexes = random.sample(range(self.n ** 2), self.m)
        mine_indexes = [divmod(num, self.n) for num in mine_indexes]
        # Заполняю поле, включая расстановку мин
        for y in range(self.n):
            for x in range(self.n):
                is_mine = True if (y, x) in mine_indexes else False
                self.board[y][x] = Cell(mine=is_mine)
        # Создаю метки о количестве соседних мин
        for y in range(self.n):
            for x in range(self.n):
                self.board[y][x].around_mines = self._calculate_around_mines(y, x)

    def show(self) -> None:
        """Отрисовка поля в консоли"""
        field = ''
        field += 'ᵪ\ʸ' + ' '.join([f'{i:^1d}' for i in range(self.n)])
        for n, i in enumerate(self.board):
            row = ''.join(str(i))
            row = row.replace(',', '').replace(
                '[', '').replace('\'', '').replace(']', '')
            field += '\n' + f'{n:<3}' + row
        print(field)

    def _calculate_around_mines(self, y: int, x: int) -> int:
        """Расчет количества мин на соседних клетках"""
        counter = 0
        neighbour_coords = [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x), (y - 1, x - 1), (y + 1, x + 1),
                            (y - 1, x + 1), (y + 1, x - 1)]
        neighbour_coords = [x for x in neighbour_coords if not self._is_out(x)]

        for coord in neighbour_coords:
            if self.board[coord[0]][coord[1]].mine:
                counter += 1
        return counter

    def _is_out(self, coords: tuple[int, int]) -> bool:
        """Проверка координат на вылет за пределы поля"""
        return not ((0 <= coords[0] < self.n) and (0 <= coords[1] < self.n))

    def mark_cell(self, coords: tuple[int, int]) -> None:
        """Пометить клетку как минную"""
        if not self.board[coords[0]][coords[1]].is_opened:
            self.board[coords[0]][coords[1]].is_marked = True

    def unmark_cell(self, coords: tuple[int, int]) -> None:
        """Отменить пометку клетки как минной"""
        self.board[coords[0]][coords[1]].is_marked = False

    def open_cell(self, coords: tuple[int, int]) -> None:
        """Открыть клетку"""
        self.board[coords[0]][coords[1]].is_opened = True
        self._check_cell(coords)

    def _check_cell(self, coords: tuple[int, int]) -> None:
        """Проверка клетки на наличие мин и открытие соседних клеток"""
        y, x = coords
        if self.board[y][x].mine:
            raise StopGameException('Взрыв...')
        if self.board[y][x].around_mines == 0:
            neighbour_coords = [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x), (y - 1, x - 1), (y + 1, x + 1),
                                (y - 1, x + 1), (y + 1, x - 1)]
            neighbour_coords = [
                x for x in neighbour_coords if not self._is_out(x)]
            for coord in neighbour_coords:
                self.board[coord[0]][coord[1]].is_opened = True

    def is_winner(self) -> int | bool:
        """Проверка поля на полное разминирование"""
        counter = 0
        for row in self.board:
            for i in row:
                if i.is_opened:
                    counter += 1
        if counter >= self.n ** 2 - self.m:
            return counter
        return False


class Cell:
    def __init__(self, around_mines: int = 0, mine: bool = False) -> None:
        self.around_mines = around_mines
        self.mine = mine
        self.is_opened = False
        self.is_marked = False

    def __repr__(self) -> str:
        if self.is_opened and self.mine:
            return '☀'
        elif self.is_opened and not self.mine:
            return f'{self.around_mines}'
        elif self.is_marked and not self.is_opened:
            return '✔'
        else:
            return f'•'


class Game:

    def __init__(self, board_size: int, mines_number: int) -> None:
        self.board = GamePole(n=board_size, m=mines_number)

    @staticmethod
    def _greetings() -> None:
        print('Добро пожаловать в игру "Сапер"')

    @staticmethod
    def _show_menu():
        """Вывод меню"""
        print('Выберите число для навигации по меню:')
        print('1 - Завершение игры')
        print('2 - Отметить клетку как заминированную')
        print('3 - Снять отметку заминированной клетки')
        print('4 - Открыть клетку')

    def _enter_menu_selection(self) -> int:
        """Запрос ввода пункта меню"""
        while True:
            data = input(
                'Введите число от 1 до 4:')
            if self._is_correct_choice(data):
                return int(data)
            print('Ошибка меню.Повторите ввод...')

    def _enter_coordinates(self) -> tuple[int, int]:
        """Запрос ввода координат"""
        while True:
            data = input(
                'Введите координаты (числа) через пробел в формате "X Y":')
            coords = tuple(data.split())
            if self._are_correct_coordinates(coords):
                return tuple(map(int, coords))
            print('Ошибка получения координат.Повторите ввод...')

    def _are_correct_coordinates(self, coords: tuple[str, str]) -> bool:
        """Валидация координат"""
        if len(coords) != 2:
            return False
        try:
            y, x = int(coords[0]), int(coords[1])
        except Exception:
            return False
        return 0 <= y < self.board.n and 0 <= x < self.board.n

    @staticmethod
    def _is_correct_choice(number: str) -> bool:
        """Валидация ввода пункта меню"""
        try:
            number = int(number)
        except ValueError:
            return False
        return 0 < number < 5

    def game_loop(self):
        """Запуск игрового цикла"""
        self._greetings()
        while True:
            try:
                self.board.show()
                if self.board.is_winner():
                    print(
                        f'Поздравляем Вас с победой. Вы набрали {self.board.is_winner()} очков')
                    break
                self._show_menu()
                choice = self._enter_menu_selection()

                match choice:
                    case 1:
                        print('Выход из игры...')
                        time.sleep(2)
                        break
                    case 2:
                        coords = self._enter_coordinates()
                        self.board.mark_cell(coords=coords)
                    case 3:
                        coords = self._enter_coordinates()
                        self.board.unmark_cell(coords=coords)
                    case 4:
                        coords = self._enter_coordinates()
                        self.board.open_cell(coords=coords)
            except StopGameException:
                print('Вы проиграли')
                break
        self.board.show()
        print('Конец игры...')


game = Game(10, 12)
game.game_loop()
