"""Conversões usadas pelo BehavioralAdder para somar barramentos via inteiro."""


def sum_via_integer_conversion(a, b):
    """Soma dois vetores de bits convertendo-os para int (atalho do BehavioralAdder)."""
    a_int = binary_array_to_int(a)
    b_int = binary_array_to_int(b)
    sum_int = a_int + b_int
    sum_array = int_to_binary_array(sum_int)
    return pad_binary_array(sum_array, len(a))


def binary_array_to_int(binary_array):
    """Converte uma lista de bits (MSB primeiro) para inteiro."""
    bits_as_str = "".join("1" if bit else "0" for bit in binary_array)
    return int(bits_as_str, 2)


def int_to_binary_array(value):
    """Converte um inteiro para lista de bits, sem preenchimento de largura."""
    binary_str = bin(value)[2:]
    return [bit == "1" for bit in binary_str]


def pad_binary_array(binary_array, length):
    """Ajusta o vetor para `length` bits: preenche à esquerda ou trunca o excesso (overflow)."""
    if len(binary_array) < length:
        return [False] * (length - len(binary_array)) + binary_array
    if len(binary_array) > length:
        return binary_array[-length:]
    return binary_array[:]
