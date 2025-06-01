"""
Программа расчёта последовательности чисел.
Выводит n первых элементов последовательности.
"""

class NumberSequence:
    """Класс расчёта последовательности чисел."""

    def sequence(self, num):
        """Расчёт последовательности."""
        return "".join(str(k) * k for k in range(1, num + 1))

if __name__ == '__main__':
    num = int(input('Введите количество элементов последовательности n: '))
    number_sequence = NumberSequence()
    print(f'Последовательность: {number_sequence.sequence(num)}')
