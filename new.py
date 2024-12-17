class New:
    def __init__(self, name=False):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

    def set_name(self):
        self.name = True


indexes = [(1, 2), (0, 0), (2, 0)]
board = [['']*5 for _ in range(5)]
for x in range(5):
    for y in range(5):
        if (y, x) in indexes:
            board[y][x] = New(name=True)
        else:
            board[y][x] = New(name=False)


print(indexes)
print(board)
