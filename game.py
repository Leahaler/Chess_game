from board import Board, Move

class ChessGame:
    """Класс, управляющий шахматной игрой с консольным интерфейсом и дополнительными командами.

    """
    def __init__(self):
        """Инициализирует новую игру, создает доску и устанавливает начальный ход."""

        self.board = Board()
        self.current_turn = "white"
        self.setup_game()
        
    def setup_game(self):
        """Настраивает начальную позицию фигур, запрашивая версию игры у пользователя."""
 
        while True:
            version = input("Выберите версию игры (1 - классическая, 2 - с новыми фигурами): ")
            if version in ["1", "2"]:
                self.board.setup_initial_position(int(version))
                break
            print("Неверный выбор. Введите 1 или 2.")
        
    def switch_turn(self):
        """Переключает текущего игрока между белыми и черными."""
        
        self.current_turn = "black" if self.current_turn == "white" else "white"
        
    def pos_to_coords(self, pos):
        """Преобразует шахматную нотацию в координаты на доске.

        Args:
            pos (str): Позиция в формате шахматной нотации (например, "E2").

        Returns:
            tuple: Кортеж (row, col) с координатами (например, (1, 4)).
        """

        col = ord(pos[0].upper()) - ord('A')
        row = int(pos[1]) - 1
        return (row, col)
        
    def play(self):
        """Запускает основной игровой цикл с обработкой ходов и команд."""

        while True:
            self.board.display()
            print(f"Ход {'белых' if self.current_turn == 'white' else 'черных'}")
            if self.board.is_in_check(self.current_turn):
                print("Шах!")
            if self.board.is_checkmate(self.current_turn):
                print(f"Мат! {'Белые' if self.current_turn == 'black' else 'Чёрные'} победили!")
                return
            while True:
                cmd = input("Введите ход (например, 'E1 G1'), или команду ('hint', 'undo', 'threat', 'quit'): ")
                if cmd.lower() == "quit":
                    return
                elif cmd.lower() == "undo":
                    if self.board.undo_last_move():
                        self.switch_turn()
                        print("Ход отменен")
                    break
                elif cmd.lower() == "hint":
                    pos = input("Введите позицию фигуры для подсказки (например, 'E2'): ")
                    try:
                        coords = self.pos_to_coords(pos)
                        piece = self.board.get_piece(*coords)
                        if piece and piece.color == self.current_turn:
                            moves = piece.get_valid_moves(self.board)
                            self.board.display(highlight_moves=moves)
                        else:
                            print("Неверный ввод. Попробуйте снова.")
                    except:
                        print("Неверный ввод. Попробуйте снова.")
                    continue
                elif cmd.lower() == "threat":
                    threatened = self.board.get_threatened_pieces(self.current_turn)
                    if threatened:
                        self.board.display(threatened=threatened)
                        king_threat = any(self.board.get_piece(*pos).symbol in ["K", "k"] for pos in threatened)
                        if king_threat:
                            print("Шах королю!")
                        print(f"Угрожаемые фигуры: {len(threatened)}")
                    else:
                        print("Нет угрожаемых фигур.")
                    continue
                try:
                    from_pos_str, to_pos_str = cmd.split()
                    from_pos = self.pos_to_coords(from_pos_str)
                    to_pos = self.pos_to_coords(to_pos_str)
                    piece = self.board.get_piece(*from_pos)
                    if not piece or piece.color != self.current_turn:
                        print("Неверный ввод. Попробуйте снова.")
                        continue
                    if self.board.move_piece(from_pos, to_pos):
                        self.switch_turn()
                        break
                    else:
                        print("Неверный ход. Попробуйте снова.")
                except:
                    print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    game = ChessGame()
    game.play()