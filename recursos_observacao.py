"""Recursos de observação e depuração permitidos pelo simulador.

Cada seção corresponde a um exemplo da Seção "Recursos de Observação e
Depuração" do Capítulo 5 do TCC; a saída impressa é a reproduzida nos Quadros.
"""

import inspect
from itertools import product

from signals.bit_array import BitArray
from components.behavioral_adder import BehavioralAdder
from components.ripple_carry_adder import RippleCarryAdder
from components.sr_latch import SRLatch


def bits(value):
    return "".join("1" if bit else "0" for bit in value)


def to_bits(number, width):
    return [c == "1" for c in format(number, f"0{width}b")]


print("=== 1) Estados transitórios: estrutural x comportamental ===")
a = BitArray([False, True, True, True])      # 0111
b = BitArray([False, False, False, False])   # 0000
estrutural = RippleCarryAdder(a, b).sum
comportamental = BehavioralAdder(a, b)
estrutural.add_listener(lambda old, new: print("estrutural:    ", bits(new)))
comportamental.add_listener(lambda old, new: print("comportamental:", bits(new)))
b.output = [False, False, False, True]       # 0111 + 0001 = 1000

print()
print("=== 2) Atividade: sinais internos que mudam em uma soma ===")
for inicial in ([False] * 8, [False] + [True] * 7):
    a = BitArray(inicial)
    b = BitArray([False] * 8)
    somador = RippleCarryAdder(a, b)
    mudancas = []
    for estagio in somador.full_adders:
        estagio.sum.add_listener(lambda old, new: mudancas.append(1))
        estagio.carry_out.add_listener(lambda old, new: mudancas.append(1))
    b.output = [False] * 7 + [True]          # soma 1
    print(f"{bits(inicial)} + 00000001: {len(mudancas)} mudança(s) nas saídas dos estágios")

print()
print("=== 3) Sonda com asserção: combinação inválida no latch SR ===")
s, r = BitArray([False]), BitArray([False])
latch = SRLatch(s, r)


def sonda(old, new):
    assert not (s.output[0] and r.output[0]), "combinação inválida S = R = 1"


s.add_listener(sonda)
r.add_listener(sonda)
s.output = [True]
print("S=1 R=0 -> Q =", bits(latch.output))
try:
    r.output = [True]
except AssertionError as erro:
    print("AssertionError:", erro)

print()
print("=== 4) Caminho da propagação até o carry_out ===")
a = BitArray([True, True])                   # 11
b = BitArray([False, False])                 # 00
somador = RippleCarryAdder(a, b)


def caminho(old, new):
    componentes = [type(f.frame.f_locals["self"]).__name__
                   for f in inspect.stack()
                   if "self" in f.frame.f_locals]
    print(" -> ".join(reversed(componentes)))


somador.carry_out.add_listener(caminho)
b.output = [False, True]                     # 11 + 01: o carry atravessa os dois estágios

print()
print("=== 5) Equivalência estrutural x comportamental (exaustiva) ===")
for x, y in product(range(8), repeat=2):
    a, b = BitArray(to_bits(x, 3)), BitArray(to_bits(y, 3))
    assert RippleCarryAdder(a, b).sum.output == BehavioralAdder(a, b).output
print("64 combinações verificadas: as duas descrições são equivalentes")
