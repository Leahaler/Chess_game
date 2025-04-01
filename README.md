![Снимок экрана 2025-04-01 082929](https://github.com/user-attachments/assets/0a8e27e5-8201-4cdb-b68f-f3733bc78fb2)
# Chess_game

#Щелокова Ксения ТРПО24-3
Реализовать программу, которая позволяет играть в шахматы на компьютере.
Взаимодействие с программой производится через консоль (базовый вариант). Игровое
поле изображается в виде 8 текстовых строк, плюс строки с буквенным обозначением
столбцов (см. пример на Рис. 1) и перерисовывается при каждом изменении состояния
поля. При запросе данных от пользователя программа сообщает, что ожидает от
пользователя (например, позицию фигуры для следующего хода белыми; целевую
позицию выбранной фигуры) и проверяет корректность ввода (допускаются только ходы
соответствующие правилам шахмат; поддержка рокировки, сложных правил для пешек и
проверки мата вынесена в отдельные пункты). Программа должна считать количество
сделанных ходов.

Рис. 1 Пример изображения шахматного поля в текстовом режиме
Сама программа НЕ ходит: т.е. не пытается выполнить ходы за одну из сторон, а
предоставляет поочередно вводить ходы за белых и черных.

Дополнительные задания:
1. Придумать 3 новых вида фигур с оригинальными правилами перемещения и
реализовать их классы. Создать модификацию шахмат с новыми фигурами с
минимальным вмешательством в существующий код.
5. Реализовать возможность «отката» ходов. С помощью специальной команды
можно возвращаться на ход (или заданное количество ходов) назад вплоть до
начала партии. Информация о ходах в партии должна храниться в объектно-
ориентированном виде.
6. Реализовать функцию подсказки выбора новой позиции фигуры: после выбора
фигуры для хода функция визуально на поле показывает поля доступные для хода
или фигуры соперника, доступные для взятия, выбранной фигурой. Информация о
допустимых ходах должна храниться в объектно-ориентированном виде, алгоритм
без модификации должен работать при добавлении новых типов фигур (задание
берется совместно с Заданием 1).
7. Реализовать функцию подсказки угрожаемых фигур: она возвращает информацию
о том, какие фигуры ходящего игрока сейчас находятся под боем (т.е. могут быть
взяты соперником на следующий ход) и визуально выделяет их на поле. Функция
отдельно указывает на наличие шаха королю. Информация о допустимых ходах
должна храниться в объектно-ориентированном виде, алгоритм без модификации
должен работать при добавлении новых типов фигур (задание берется совместно с
Заданием 1).
8. Реализовать поддержку для пешки сложных правил: «взятие на проходе» и замены
на другух фигуру при достижении крайней горизонтали (в базовой версии их
поддержка не обязательна, но возможность первого хода на одну или две
горизонтали - обязательно).

10 + 5 = 15

комбинация... сижу за шахматной доской... ситуация... и на тебя смотрю с тоской
