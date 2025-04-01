class Piece:
    """Базовый класс для всех шахматных фигур.

    Args:
        color (str): Цвет фигуры ("white" или "black").
        symbol (str): Символ фигуры для отображения на доске (например, "P" для пешки).
    """
    
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol
        self.position = None
        
    def get_valid_moves(self, board):
        return []
    
    def _get_moves_in_directions(self, board, directions, max_steps=8):
        moves = []
        row, col = self.position
        for dr, dc in directions:
            for i in range(1, max_steps + 1):
                new_row, new_col = row + i * dr, col + i * dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if board.is_empty(new_row, new_col):
                        moves.append((new_row, new_col))
                    else:
                        if board.get_piece(new_row, new_col).color != self.color:
                            moves.append((new_row, new_col))
                        break
                else:
                    break
        return moves
    
    def __str__(self):
        """Возвращает строковое представление фигуры.

        Returns:
            str: Символ фигуры (например, "P" или "p").
        """
        
        return self.symbol

class Pawn(Piece):
    """Класс пешки, наследуется от Piece.

    Args:
        color (str): Цвет пешки ("white" или "black").
    """
    
    def __init__(self, color):
        super().__init__(color, "P" if color == "white" else "p")
        self.has_moved = False
        
    def get_valid_moves(self, board):
        """Возвращает список допустимых ходов для пешки.

        Args:
            board (Board): Объект доски, на которой находится пешка.

        Returns:
            list: Список кортежей (row, col) — допустимые позиции для хода.
        """
        
        moves = []
        row, col = self.position
        direction = 1 if self.color == "white" else -1
        new_row = row + direction
        if 0 <= new_row < 8 and board.is_empty(new_row, col):
            moves.append((new_row, col))
            if not self.has_moved and board.is_empty(row + 2*direction, col):
                moves.append((row + 2*direction, col))
        for dc in [-1, 1]:
            new_col = col + dc
            if (0 <= new_col < 8 and 0 <= new_row < 8 and 
                not board.is_empty(new_row, new_col) and 
                board.get_piece(new_row, new_col).color != self.color):
                moves.append((new_row, new_col))
        if (self.color == "white" and row == 4) or (self.color == "black" and row == 3):
            last_move = board.move_history[-1] if board.move_history else None
            if (last_move and isinstance(last_move.piece, Pawn) and 
                abs(last_move.from_pos[0] - last_move.to_pos[0]) == 2):
                moves.append((row + direction, last_move.to_pos[1]))
        return moves

class Rook(Piece):
    """Класс ладьи, наследуется от Piece.

    Args:
        color (str): Цвет ладьи ("white" или "black").
    """
    
    def __init__(self, color):
        super().__init__(color, "R" if color == "white" else "r")
        self.has_moved = False
        
    def get_valid_moves(self, board):
        """Возвращает список допустимых ходов для ладьи.

        Args:
            board (Board): Объект доски, на которой находится ладья.

        Returns:
            list: Список кортежей (row, col) — допустимые позиции для хода.
        """
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return self._get_moves_in_directions(board, directions)

class Knight(Piece):
    """Класс коня, наследуется от Piece.

    Args:
        color (str): Цвет коня ("white" или "black").
    """
    
    def __init__(self, color):
        super().__init__(color, "N" if color == "white" else "n")
        
    def get_valid_moves(self, board):
        """Возвращает список допустимых ходов для коня.

        Args:
            board (Board): Объект доски, на которой находится конь.

        Returns:
            list: Список кортежей (row, col) — допустимые позиции для хода.
        """
        moves = []
        row, col = self.position
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.is_empty(new_row, new_col) or board.get_piece(new_row, new_col).color != self.color:
                    moves.append((new_row, new_col))
        return moves

class Bishop(Piece):
    """Класс слона, наследуется от Piece.

    Args:
        color (str): Цвет слона ("white" или "black").
    """
    
    def __init__(self, color):
        super().__init__(color, "B" if color == "white" else "b")
        
    def get_valid_moves(self, board):
        """Возвращает список допустимых ходов для слона.

        Args:
            board (Board): Объект доски, на которой находится слон.

        Returns:
            list: Список кортежей (row, col) — допустимые позиции для хода.
        """
        
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._get_moves_in_directions(board, directions)

class Queen(Piece):
    """Класс ферзя, наследуется от Piece.

    Args:
        color (str): Цвет ферзя ("white" или "black").
    """
    
    def __init__(self, color):
        super().__init__(color, "Q" if color == "white" else "q")
        
    def get_valid_moves(self, board):
        """Возвращает список допустимых ходов для ферзя (комбинация ладьи и слона).

        Args:
            board (Board): Объект доски, на которой находится ферзь.

        Returns:
            list: Список кортежей (row, col) — допустимые позиции для хода.
        """
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._get_moves_in_directions(board, directions)

class King(Piece):
    """Класс короля, наследуется от Piece.

    Args:
        color (str): Цвет короля ("white" или "black").
    """
    
    def __init__(self, color):
        super().__init__(color, "K" if color == "white" else "k")
        self.has_moved = False
        
    def get_valid_moves(self, board, check_castling=True):
        """Возвращает список допустимых ходов для короля, включая рокировку.

        Args:
            board (Board): Объект доски, на которой находится король.

        Returns:
            list: Список кортежей (row, col) — допустимые позиции для хода.
        """
        
        moves = []
        row, col = self.position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.is_empty(new_row, new_col) or board.get_piece(new_row, new_col).color != self.color:
                    original_piece = board.get_piece(new_row, new_col)
                    board.grid[new_row][new_col] = self
                    board.grid[row][col] = None
                    temp_pos = self.position
                    self.position = (new_row, new_col)
                    in_check = board.is_in_check(self.color)
                    board.grid[row][col] = self
                    board.grid[new_row][new_col] = original_piece
                    self.position = temp_pos
                    if not in_check:
                        moves.append((new_row, new_col))
        if check_castling and not self.has_moved and not board.is_in_check(self.color):
            if (col == 4 and board.is_empty(row, 5) and board.is_empty(row, 6) and
                isinstance(board.get_piece(row, 7), Rook) and not board.get_piece(row, 7).has_moved):
                if not board.is_square_attacked(self.color, (row, 5)) and not board.is_square_attacked(self.color, (row, 6)):
                    moves.append((row, 6))
            if (col == 4 and board.is_empty(row, 3) and board.is_empty(row, 2) and board.is_empty(row, 1) and
                isinstance(board.get_piece(row, 0), Rook) and not board.get_piece(row, 0).has_moved):
                if not board.is_square_attacked(self.color, (row, 3)) and not board.is_square_attacked(self.color, (row, 2)):
                    moves.append((row, 2))
        return moves

class Rabbit(Piece):
    """Класс кролика (новая фигура), наследуется от Piece.

    Args:
        color (str): Цвет кролика ("white" или "black").
    """
    
    def __init__(self, color):
        super().__init__(color, "M" if color == "white" else "m")
        
    def get_valid_moves(self, board):
        """Возвращает список допустимых ходов для кролика (как конь, но только вперед).

        Args:
            board (Board): Объект доски, на которой находится кролик.

        Returns:
            list: Список кортежей (row, col) — допустимые позиции для хода.
        """
        
        moves = []
        row, col = self.position
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (2, -2), (-2, 2), (-2, -2)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.is_empty(new_row, new_col) or board.get_piece(new_row, new_col).color != self.color:
                    moves.append((new_row, new_col))
        return moves

class Dog(Piece):
    """Класс собаки (новая фигура), наследуется от Piece.

    Args:
        color (str): Цвет собаки ("white" или "black").
    """
    
    def __init__(self, color):
        super().__init__(color, "D" if color == "white" else "d")
        
    def get_valid_moves(self, board):
        """Возвращает список допустимых ходов для собаки (вперед на 1 или диагональ назад).

        Args:
            board (Board): Объект доски, на которой находится собака.

        Returns:
            list: Список кортежей (row, col) — допустимые позиции для хода.
        """
        
        moves = []
        row, col = self.position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        has_neighbor = False
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if (dr, dc) != (0, 0):
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and not board.is_empty(new_row, new_col):
                        has_neighbor = True
                        break
            if has_neighbor:
                break
        if has_neighbor:
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if board.is_empty(new_row, new_col) or board.get_piece(new_row, new_col).color != self.color:
                        moves.append((new_row, new_col))
        return moves

class Cat(Piece):
    """Класс кота (новая фигура), наследуется от Piece.

    Args:
        color (str): Цвет кота ("white" или "black").
    """
    
    def __init__(self, color):
        super().__init__(color, "C" if color == "white" else "c")
        
    def get_valid_moves(self, board):
        """Возвращает список допустимых ходов для кота (как король, но без рокировки).

        Args:
            board (Board): Объект доски, на которой находится кот.

        Returns:
            list: Список кортежей (row, col) — допустимые позиции для хода.
        """
        
        moves = []
        row, col = self.position
        if row in [0, 7]:
            for new_col in range(col + 1, 8):
                piece = board.get_piece(row, new_col)
                if piece:
                    if piece.color == self.color:
                        continue
                    else:
                        moves.append((row, new_col))
                        break
                else:
                    moves.append((row, new_col))
            for new_col in range(col - 1, -1, -1):
                piece = board.get_piece(row, new_col)
                if piece:
                    if piece.color == self.color:
                        continue
                    else:
                        moves.append((row, new_col))
                        break
                else:
                    moves.append((row, new_col))
        if col in [0, 7]:
            for new_row in range(row + 1, 8):
                piece = board.get_piece(new_row, col)
                if piece:
                    if piece.color == self.color:
                        continue
                    else:
                        moves.append((new_row, col))
                        break
                else:
                    moves.append((new_row, col))
            for new_row in range(row - 1, -1, -1):
                piece = board.get_piece(new_row, col)
                if piece:
                    if piece.color == self.color:
                        continue
                    else:
                        moves.append((new_row, col))
                        break
                else:
                    moves.append((new_row, col))
        return moves