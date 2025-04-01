from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King, Rabbit, Dog, Cat

class Move:
    """
    Класс, представляющий один ход в шахматной игре.

    Args:
        piece (Piece): Фигура, которая совершает ход.
        from_pos (tuple): Начальная позиция в формате (row, col).
        to_pos (tuple): Конечная позиция в формате (row, col).
    """

    def __init__(self, piece, from_pos, to_pos):
        self.piece = piece
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.captured = None
        self.promoted_to = None

class Board:
    """Класс, представляющий шахматную доску и управляющий её состоянием."""

    def __init__(self):
        """Инициализирует пустую доску, историю ходов и счетчик ходов."""
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.move_history = []
        self.move_count = 0
        
    def setup_initial_position(self, version):
        """Расставляет фигуры на доске в начальной позиции.

        Args:
            version (int): Вариант расстановки (1 — классические шахматы, 2 — с новыми фигурами).
        """
        for col in range(8):
            self.place_piece(Pawn("white"), 1, col)
            self.place_piece(Pawn("black"), 6, col)
        if version == 1:
            self.place_piece(Rook("white"), 0, 0)
            self.place_piece(Knight("white"), 0, 1)
            self.place_piece(Bishop("white"), 0, 2)
            self.place_piece(Queen("white"), 0, 3)
            self.place_piece(King("white"), 0, 4)
            self.place_piece(Bishop("white"), 0, 5)
            self.place_piece(Knight("white"), 0, 6)
            self.place_piece(Rook("white"), 0, 7)
            self.place_piece(Rook("black"), 7, 0)
            self.place_piece(Knight("black"), 7, 1)
            self.place_piece(Bishop("black"), 7, 2)
            self.place_piece(Queen("black"), 7, 3)
            self.place_piece(King("black"), 7, 4)
            self.place_piece(Bishop("black"), 7, 5)
            self.place_piece(Knight("black"), 7, 6)
            self.place_piece(Rook("black"), 7, 7)
        elif version == 2:
            self.place_piece(Cat("white"), 0, 0)
            self.place_piece(Rabbit("white"), 0, 1)
            self.place_piece(Dog("white"), 0, 2)
            self.place_piece(Queen("white"), 0, 3)
            self.place_piece(King("white"), 0, 4)
            self.place_piece(Dog("white"), 0, 5)
            self.place_piece(Rabbit("white"), 0, 6)
            self.place_piece(Cat("white"), 0, 7)
            self.place_piece(Cat("black"), 7, 0)
            self.place_piece(Rabbit("black"), 7, 1)
            self.place_piece(Dog("black"), 7, 2)
            self.place_piece(Queen("black"), 7, 3)
            self.place_piece(King("black"), 7, 4)
            self.place_piece(Dog("black"), 7, 5)
            self.place_piece(Rabbit("black"), 7, 6)
            self.place_piece(Cat("black"), 7, 7)
            
    def place_piece(self, piece, row, col):
        """Размещает фигуру на указанной клетке доски.

        Args:
            piece (Piece): Фигура для размещения.
            row (int): Номер строки (0-7).
            col (int): Номер столбца (0-7).
        """
        self.grid[row][col] = piece
        piece.position = (row, col)
        
    def is_empty(self, row, col):
        """Проверяет, пуста ли указанная клетка.

        Args:
            row (int): Номер строки (0-7).
            col (int): Номер столбца (0-7).

        Returns:
            bool: True, если клетка пуста, False — если занята.
        """
        return self.grid[row][col] is None
        
    def get_piece(self, row, col):
        """Возвращает фигуру на указанной клетке.

        Args:
            row (int): Номер строки (0-7).
            col (int): Номер столбца (0-7).

        Returns:
            Piece or None: Фигура на клетке или None, если клетка пуста.
        """
        return self.grid[row][col]

    def _find_king(self, color):
        """Находит позицию короля заданного цвета.

        Args:
            color (str): Цвет короля ("white" или "black").

        Returns:
            tuple or None: Кортеж (row, col) с позицией короля или None, если король не найден.
        """
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None

    def is_in_check(self, color):
        """Проверяет, находится ли король заданного цвета под шахом.

        Args:
            color (str): Цвет короля ("white" или "black").

        Returns:
            bool: True, если король под шахом, False — если нет.
        """
        king_pos = self._find_king(color)
        if not king_pos:
            return False
        opponent_color = "black" if color == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == opponent_color:
                    moves = piece.get_valid_moves(self, check_castling=False) if isinstance(piece, King) else piece.get_valid_moves(self)
                    if king_pos in moves:
                        return True
        return False

    def is_square_attacked(self, color, pos):
        """Проверяет, атакована ли указанная клетка фигурами противника.

        Args:
            color (str): Цвет игрока, для которого проверяется угроза ("white" или "black").
            pos (tuple): Позиция клетки в формате (row, col).

        Returns:
            bool: True, если клетка атакована, False — если нет.
        """
        opponent_color = "black" if color == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == opponent_color:
                    if pos in piece.get_valid_moves(self):
                        return True
        return False

    def is_checkmate(self, color):
        """Проверяет, является ли позиция матовой для игрока заданного цвета.

        Args:
            color (str): Цвет игрока ("white" или "black").

        Returns:
            bool: True, если мат, False — если есть ход для избежания шаха.
        """
        if not self.is_in_check(color):
            return False
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    moves = piece.get_valid_moves(self)
                    for move in moves:
                        captured = self.get_piece(*move)
                        self.grid[move[0]][move[1]] = piece
                        self.grid[row][col] = None
                        old_pos = piece.position
                        piece.position = move
                        was_moved = piece.has_moved if hasattr(piece, 'has_moved') else None
                        if hasattr(piece, 'has_moved'):
                            piece.has_moved = True
                        still_in_check = self.is_in_check(color)
                        self.grid[row][col] = piece
                        self.grid[move[0]][move[1]] = captured
                        piece.position = old_pos
                        if was_moved is not None:
                            piece.has_moved = was_moved
                        if not still_in_check:
                            return False
        return True
        
    def move_piece(self, from_pos, to_pos):
        """Выполняет ход фигуры с одной позиции на другую.

        Args:
            from_pos (tuple): Начальная позиция в формате (row, col).
            to_pos (tuple): Конечная позиция в формате (row, col).

        Returns:
            bool: True, если ход успешен, False — если ход недопустим.
        """
        piece = self.get_piece(*from_pos)
        if not piece:
            return False
        valid_moves = piece.get_valid_moves(self)
        if to_pos not in valid_moves:
            return False
        move = Move(piece, from_pos, to_pos)
        move.captured = self.get_piece(*to_pos)
        if isinstance(piece, King) and abs(to_pos[1] - from_pos[1]) == 2:
            if to_pos[1] == 6:
                rook = self.get_piece(from_pos[0], 7)
                self.grid[from_pos[0]][5] = rook
                self.grid[from_pos[0]][7] = None
                rook.position = (from_pos[0], 5)
                rook.has_moved = True
            elif to_pos[1] == 2:
                rook = self.get_piece(from_pos[0], 0)
                self.grid[from_pos[0]][3] = rook
                self.grid[from_pos[0]][0] = None
                rook.position = (from_pos[0], 3)
                rook.has_moved = True
        if isinstance(piece, Pawn):
            if (piece.color == "white" and to_pos[0] == 7) or (piece.color == "black" and to_pos[0] == 0):
                new_piece = Queen(piece.color)
                move.promoted_to = new_piece
                self.grid[to_pos[0]][to_pos[1]] = new_piece
                new_piece.position = to_pos
            else:
                self.grid[to_pos[0]][to_pos[1]] = piece
                piece.position = to_pos
        else:
            self.grid[to_pos[0]][to_pos[1]] = piece
            piece.position = to_pos
        self.grid[from_pos[0]][from_pos[1]] = None
        if hasattr(piece, 'has_moved'):
            piece.has_moved = True
        self.move_history.append(move)
        self.move_count += 1
        return True
        
    def undo_last_move(self):
        """Отменяет последний сделанный ход.

        Returns:
            bool: True, если отмена успешна, False — если нет ходов для отмены.
        """
        if not self.move_history:
            return False
        last_move = self.move_history.pop()
        self.grid[last_move.from_pos[0]][last_move.from_pos[1]] = last_move.piece
        self.grid[last_move.to_pos[0]][last_move.to_pos[1]] = last_move.captured
        last_move.piece.position = last_move.from_pos
        if isinstance(last_move.piece, King) and abs(last_move.to_pos[1] - last_move.from_pos[1]) == 2:
            if last_move.to_pos[1] == 6:
                rook = self.get_piece(last_move.from_pos[0], 5)
                self.grid[last_move.from_pos[0]][7] = rook
                self.grid[last_move.from_pos[0]][5] = None
                rook.position = (last_move.from_pos[0], 7)
                rook.has_moved = False
            elif last_move.to_pos[1] == 2:
                rook = self.get_piece(last_move.from_pos[0], 3)
                self.grid[last_move.from_pos[0]][0] = rook
                self.grid[last_move.from_pos[0]][3] = None
                rook.position = (last_move.from_pos[0], 0)
                rook.has_moved = False
        if last_move.promoted_to:
            self.grid[last_move.to_pos[0]][last_move.to_pos[1]] = last_move.captured
        if hasattr(last_move.piece, 'has_moved') and last_move.from_pos[0] == (1 if last_move.piece.color == "white" else 6):
            last_move.piece.has_moved = False
        self.move_count -= 1
        return True
        
    def display(self, highlight_moves=None, threatened=None):
        """Отображает текущее состояние доски в консоли с подсветкой ходов или угроз.

        Args:
            highlight_moves (list, optional): Список позиций (row, col) для подсветки допустимых ходов.
            threatened (list, optional): Список позиций (row, col) для подсветки угрожаемых фигур.
        """
        print("\n   A  B  C  D  E  F  G  H")
        for row in range(7, -1, -1):
            line = [f"{row+1} "]
            for col in range(8):
                piece = self.grid[row][col]
                cell = str(piece or '.')
                if highlight_moves and (row, col) in highlight_moves:
                    cell = f"[{cell}]"
                elif threatened and (row, col) in threatened:
                    cell = f"*{cell}*"
                line.append(cell.center(3))
            line.append(f" {row+1}")
            print(''.join(line))
        print("   A  B  C  D  E  F  G  H")
        print(f"\nХодов сделано: {self.move_count}")

    def get_threatened_pieces(self, color):
        """Возвращает список позиций фигур заданного цвета, находящихся под угрозой.

        Args:
            color (str): Цвет игрока ("white" или "black").

        Returns:
            list: Список кортежей (row, col) с позициями угрожаемых фигур.
        """
        threatened = []
        opponent_color = "black" if color == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == opponent_color:
                    moves = piece.get_valid_moves(self)
                    for move in moves:
                        target = self.get_piece(*move)
                        if target and target.color == color:
                            threatened.append(move)
        return threatened