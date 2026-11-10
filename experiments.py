from signals.bit_array import BitArray
from components.behavioral_adder import BehavioralAdder
from components.ripple_carry_adder import RippleCarryAdder
from components.full_adder import FullAdder
from components.behavioral_register import BehavioralRegister
from components.sr_latch import SRLatch
from components.d_latch import DLatch
from components.d_flip_flop import DFlipFlop
from components.d_flip_flop_register import DFlipFlopRegister
from gates.not_gate import Not
from gates.or_gate import Or
from gates.and_gate import And
from gates.xor_gate import Xor

print("=== 1) NOT gate ===")
a = BitArray([False, True, False])
not_a = Not(a)
print("a     =", a.output)
print("not a =", not_a.output)
a.output = [True, True, True]
print("a changed -> not a =", not_a.output)

print()
print("=== 2) Half adder (Xor = sum, And = carry) ===")
for x, y in [(False, False), (False, True), (True, False), (True, True)]:
    bit_x = BitArray([x])
    bit_y = BitArray([y])
    sum_gate = Xor(bit_x, bit_y)
    carry_gate = And(bit_x, bit_y)
    print(f"x={x} y={y} -> sum={sum_gate.output[0]} carry={carry_gate.output[0]}")

print()
print("=== 3) OR / AND comparison ===")
p = BitArray([False, True])
q = BitArray([True, True])
or_gate = Or(p, q)
and_gate = And(p, q)
print("p =", p.output, " q =", q.output)
print("p OR q  =", or_gate.output)
print("p AND q =", and_gate.output)

print()
print("=== 4) Toggle flip-flop (T-FF) using Xor + BehavioralRegister feedback ===")
# T-FF: a cada pulso de clock, a saida inverte de valor (0,1,0,1,...)
# construimos com Xor(saida_atual, 1) realimentando um BehavioralRegister
one = BitArray([True])
clock = BitArray(False)

# 'signal' guarda a saida atual do FF, comeca em [False]
signal = BitArray([False])
toggle_logic = Xor(signal, one)
flip_flop = BehavioralRegister(clock, toggle_logic, feedback_target=signal)

print("estado inicial:", signal.output)
for i in range(6):
    clock.output = False
    clock.output = True
    print(f"pulso {i + 1}: saida = {signal.output}")

print()
print("=== 4b) Log de propagacao ate a estabilizacao (mesmo circuito) ===")
# Registra um listener de log em cada componente do circuito acima para
# observar a ORDEM em que a propagacao reativa realmente acontece dentro
# de um unico pulso de clock, ate o sinal se estabilizar.
clock.output = False  # reseta o clock em silencio, antes de logar
signal.add_listener(lambda old, new: print(f"  signal:       {old} -> {new}"))
toggle_logic.add_listener(lambda old, new: print(f"  toggle_logic: {old} -> {new}"))
flip_flop.add_listener(lambda old, new: print(f"  flip_flop:    {old} -> {new}"))
clock.add_listener(lambda old, new: print(f"  clock:        {old} -> {new}"))
print("estado antes do pulso: signal =", signal.output)
print("pulso de clock (False -> True):")
clock.output = False
clock.output = True
print("estado apos o pulso: signal =", signal.output)

print()
print("=== 5) Contador de 3 bits usando BehavioralAdder (atalho em Python) ===")
# O BehavioralAdder NAO monta um somador com portas logicas: ele converte os
# bits para int, soma e converte de volta. E util para testar outras
# partes de um circuito (ex.: o BehavioralRegister e a realimentacao) sem precisar
# implementar a aritmetica bit a bit -- mistura codigo Python "puro" com
# o resto do circuito reativo. Nao e a forma "ideal" de montar um somador
# (ver secoes 6-8), mas e uma opcao valida quando o somador em si nao e
# o que se quer testar no momento.
increment = BitArray([False, False, True])
count_signal = BitArray([False, False, False])
behavioral_adder = BehavioralAdder(increment, count_signal)
clock2 = BitArray(False)
counter = BehavioralRegister(clock2, behavioral_adder, feedback_target=count_signal)
print("inicial:", counter.output)
for i in range(8):
    clock2.output = False
    clock2.output = True
    print(f"pulso {i + 1}: {counter.output}")

print()
print("=== 6) Somador completo (FullAdder) feito so com portas logicas ===")
for bit_a, bit_b, bit_cin in [(False, False, False), (True, False, False),
                              (True, True, False), (True, True, True)]:
    ba, bb, bc = BitArray([bit_a]), BitArray([bit_b]), BitArray([bit_cin])
    full_adder = FullAdder(ba, bb, bc)
    print(f"a={int(bit_a)} b={int(bit_b)} cin={int(bit_cin)} -> "
          f"sum={int(full_adder.sum.output[0])} carry_out={int(full_adder.carry_out.output[0])}")

print()
print("=== 7) Somador de N bits (RippleCarryAdder) encadeando FullAdders ===")
a3 = BitArray([False, True, True])    # 011 = 3
b3 = BitArray([False, False, True])   # 001 = 1
adder3 = RippleCarryAdder(a3, b3)
print(f"3 + 1 -> sum={adder3.sum.output} (100=4) carry_out={adder3.carry_out.output} (sem overflow)")

a4 = BitArray([True, True, True])     # 111 = 7
b4 = BitArray([False, False, True])   # 001 = 1
adder4 = RippleCarryAdder(a4, b4)
print(f"7 + 1 -> sum={adder4.sum.output} (000, estourou) carry_out={adder4.carry_out.output} (sinaliza overflow!)")

print()
print("=== 8) Contador de 3 bits usando SOMENTE portas logicas (sem atalho Python) ===")
# Mesma ideia da secao 5, mas o somador agora e um circuito real montado
# com Xor/And/Or (via RippleCarryAdder). O overflow nao precisa de
# nenhum tratamento especial em codigo: ele aparece naturalmente porque
# a soma so tem 3 fios de saida, e o "vai-um" do ultimo estagio vira um
# carry_out separado, que aqui simplesmente nao e reconectado a nada.
increment2 = BitArray([False, False, True])
signal2 = BitArray([False, False, False])
gate_adder = RippleCarryAdder(signal2, increment2)
clock3 = BitArray(False)
counter2 = BehavioralRegister(clock3, gate_adder.sum, feedback_target=signal2)
print("inicial:", counter2.output)
for i in range(9):
    clock3.output = False
    clock3.output = True
    print(f"pulso {i + 1}: sum={counter2.output} carry_out={gate_adder.carry_out.output}")

print()
print("=== 9) Latch SR (NOR cruzado) -- Set/Reset/Hold ===")
# Latch construido com realimentacao combinacional de verdade: Q depende
# de Q_not, que depende de Q. Isso exige quebrar a ordem de construcao
# com um "proxy" (ver components/sr_latch.py) e so funciona porque as
# portas passaram a notificar listeners apenas quando o valor calculado
# realmente muda (sem isso, o laco entraria em recursao infinita).
s = BitArray([True])
r = BitArray([False])
latch = SRLatch(s, r)
print(f"S=1 R=0 -> Q={latch.output} (set)")
s.output, r.output = [False], [False]
print(f"S=0 R=0 -> Q={latch.output} (hold, mantem o valor anterior)")
s.output, r.output = [False], [True]
print(f"S=0 R=1 -> Q={latch.output} (reset)")
r.output = [False]
print(f"S=0 R=0 -> Q={latch.output} (hold, mantem o valor anterior)")

print()
print("=== 10) D Latch (transparente) e Flip-Flop D mestre-escravo ===")
d = BitArray([False])
enable = BitArray([True])
d_latch = DLatch(d, enable)
print(f"enable=1, D=0 -> Q={d_latch.output} (transparente: segue D)")
d.output = [True]
print(f"enable=1, D=1 -> Q={d_latch.output} (ainda transparente)")
enable.output = [False]
d.output = [False]
print(f"enable=0, D=0 -> Q={d_latch.output} (opaco: NAO acompanha D)")

d2 = BitArray([False])
clock4 = BitArray([False])
flip_flop = DFlipFlop(d2, clock4)
print(f"inicial (indefinido antes do 1o pulso) -> Q={flip_flop.output}")
d2.output = [True]
clock4.output = [True]
print(f"D=1, clock sobe -> Q={flip_flop.output} (capturou D)")
d2.output = [False]
print(f"D muda p/ 0 com clock ainda em 1 -> Q={flip_flop.output} (nao muda)")
clock4.output = [False]
print(f"clock desce (1->0) -> Q={flip_flop.output} (flip-flop so muda na borda de subida)")
clock4.output = [True]
print(f"clock sobe de novo com D=0 -> Q={flip_flop.output} (capturou o novo D)")

print()
print("=== 11) Flip-flop toggle montado so com portas (DFlipFlop realimentado) ===")
# Repete a demonstracao da secao 4, trocando o BehavioralRegister abstrato pelo
# DFlipFlop mestre-escravo (components/d_flip_flop.py): a propria saida,
# invertida, e realimentada de volta para a entrada D. Isso so estabiliza
# corretamente porque os listeners de um mesmo sinal sao notificados na
# ordem de registro (e nao na ordem inversa) -- ver Secao "A Engine de
# Propagacao" do Capitulo 4 e "Registrador Real com Latches" do Capitulo 5.
clock5 = BitArray([False])
signal5 = BitArray([False])
not_signal5 = Not(signal5)
toggle_ff = DFlipFlop(not_signal5, clock5, feedback_target=signal5)
print("estado inicial:", signal5.output)
for i in range(6):
    clock5.output = [False]
    clock5.output = [True]
    print(f"pulso {i + 1}: saida = {signal5.output}")

print()
print("=== 12) Contador de 3 bits com DFlipFlopRegister (registrador 'real') ===")
# Mesmo contador da secao 8 (RippleCarryAdder), mas agora trocando tambem
# o BehavioralRegister abstrato por um DFlipFlopRegister: N DFlipFlop em paralelo,
# um por bit (components/d_flip_flop_register.py), sem nenhuma abstracao
# de borda em Python -- so portas logicas do inicio ao fim do circuito.
increment3 = BitArray([False, False, True])
signal3 = BitArray([False, False, False])
gate_adder3 = RippleCarryAdder(signal3, increment3)
clock6 = BitArray([False])
counter3 = DFlipFlopRegister(clock6, gate_adder3.sum, feedback_target=signal3)
print("inicial:", counter3.output)
for i in range(9):
    clock6.output = [False]
    clock6.output = [True]
    print(f"pulso {i + 1}: sum={counter3.output} carry_out={gate_adder3.carry_out.output}")
