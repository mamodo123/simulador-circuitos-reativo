# Simulador de Circuitos Digitais com Propagação Reativa

Biblioteca desenvolvida como Trabalho de Conclusão de Curso em Ciência da Computação (UFSC). O texto do TCC está na pasta [`latex/`](latex/), com a versão compilada em [`latex/main.pdf`](latex/main.pdf).

Simulador de circuitos digitais em Python puro (sem dependências externas), construído em torno de um **modelo reativo/orientado a eventos**: cada componente (fio, porta lógica, somador, registrador) expõe uma saída (`output`) e uma lista de *listeners*. Quando a saída de um componente muda, ele notifica automaticamente todos os componentes ligados a ele, propagando o sinal pelo circuito, de forma parecida com o que aconteceria em hardware real.

## Sumário

- [Requisitos](#requisitos)
- [Instalação com ambiente virtual (venv)](#instalação-com-ambiente-virtual-venv)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Conceito: o modelo reativo por eventos](#conceito-o-modelo-reativo-por-eventos)
- [Referência da API](#referência-da-api)
  - [`BitArray`](#bitarray)
  - [Portas lógicas: `Not`, `Or`, `And`, `Xor`](#portas-lógicas-not-or-and-xor)
  - [Somador com portas lógicas: `FullAdder` e `RippleCarryAdder`](#somador-com-portas-lógicas-fulladder-e-ripplecarryadder)
  - [`BehavioralAdder`](#behavioraladder)
  - [`BehavioralRegister`](#behavioralregister)
- [Como rodar](#como-rodar)
- [Exemplos de uso](#exemplos-de-uso)
  - [1. Porta NOT reagindo a mudanças](#1-porta-not-reagindo-a-mudanças)
  - [2. Meio-somador (half adder) com Xor + And](#2-meio-somador-half-adder-com-xor--and)
  - [3. Registrador (latch) simples](#3-registrador-latch-simples)
  - [4. Contador binário de 3 bits com BehavioralAdder](#4-contador-binário-de-3-bits-com-behavioraladder)
  - [5. Flip-flop toggle (T-FF)](#5-flip-flop-toggle-t-ff)
  - [6. Somador completo (FullAdder) com portas lógicas](#6-somador-completo-fulladder-com-portas-lógicas)
  - [7. Contador de N bits só com portas lógicas](#7-contador-de-n-bits-só-com-portas-lógicas)
- [Como criar seu próprio circuito](#como-criar-seu-próprio-circuito)
- [Limitações conhecidas](#limitações-conhecidas)
- [Possíveis extensões](#possíveis-extensões)
- [Compilar o TCC](#compilar-o-tcc)

## Requisitos

- Python 3.8 ou mais recente. O simulador usa apenas a biblioteca padrão, sem nenhuma dependência externa, então o `requirements.txt` não instala nada; ele existe para que o fluxo usual com `pip` funcione também aqui.
- Para compilar o texto do TCC (opcional): uma distribuição LaTeX e os pacotes de `requirements-tcc.txt` (ver [Compilar o TCC](#compilar-o-tcc)).

## Instalação com ambiente virtual (venv)

O passo a passo abaixo cria um ambiente virtual isolado, roda os testes e executa os exemplos. Execute os comandos a partir da pasta raiz do projeto (a que contém este README).

**1. Obtenha o código**

```bash
git clone https://github.com/mamodo123/simulador-circuitos-reativo.git
cd simulador-circuitos-reativo
```

**2. Crie o ambiente virtual**

```bash
python -m venv .venv
```

No Linux e no macOS, use `python3` no lugar de `python` se o comando `python` não existir.

**3. Ative o ambiente virtual**

| Sistema | Comando |
|---|---|
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (Prompt de Comando) | `.venv\Scripts\activate.bat` |
| Linux / macOS (bash, zsh) | `source .venv/bin/activate` |

Com o ambiente ativo, o nome `(.venv)` aparece no início da linha do terminal. No PowerShell, se aparecer um erro de política de execução de *scripts*, libere-a só para a sessão atual com `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` e ative de novo.

**4. Instale as dependências**

```bash
python -m pip install -r requirements.txt
```

Como o simulador não tem dependências externas, este passo não instala nada, mas pode ser mantido como hábito. Se for compilar o TCC, instale também `requirements-tcc.txt` (ver [Compilar o TCC](#compilar-o-tcc)).

**5. Verifique a instalação rodando os testes**

```bash
python -m unittest discover -s tests -t .
```

A saída deve terminar com `OK`.

**6. Execute os exemplos**

```bash
python main.py                  # contador binário de 3 bits
python experiments.py           # 12 experimentos (portas, somadores, latches, flip-flops, contadores)
python recursos_observacao.py   # recursos de observação e depuração (transitórios, sondas, etc.)
```

Os detalhes de cada programa estão em [Como rodar](#como-rodar).

**7. Use o simulador no interpretador**

Com o ambiente ativo e dentro da pasta do projeto, abra o interpretador com `python` e monte um circuito:

```python
>>> from signals.bit_array import BitArray
>>> from gates.and_gate import And
>>> a = BitArray([True])
>>> b = BitArray([False])
>>> porta = And(a, b)
>>> porta.output
[False]
>>> b.output = [True]   # a porta recalcula sozinha
>>> porta.output
[True]
```

**8. Desative o ambiente ao terminar**

```bash
deactivate
```

Nas próximas vezes, basta repetir o passo 3 (ativar) antes de usar o projeto.

## Estrutura do projeto

```
simulador-circuitos-reativo/
├── main.py                        # Exemplo pronto: contador binário de 3 bits
├── experiments.py                 # 12 experimentos (portas, somadores, latches, flip-flops, contadores)
├── recursos_observacao.py         # Recursos de observação e depuração (Seção 5.3 do TCC)
├── requirements.txt               # Dependências do simulador (nenhuma: só biblioteca padrão)
├── requirements-tcc.txt           # Dependências para compilar o TCC (Pygments)
├── README.md
├── signals/                       # representação de sinais (fios/barramentos)
│   ├── bit_array.py                # BitArray: sinal/vetor de bits que notifica listeners
│   ├── bit_slice.py                 # BitSlice: projeta 1 bit de um sinal maior
│   └── bus.py                       # Bus: combina vários sinais de 1 bit em um barramento
├── gates/                          # portas lógicas elementares
│   ├── not_gate.py                  # Not
│   ├── and_gate.py                   # And
│   ├── or_gate.py                    # Or
│   ├── xor_gate.py                   # Xor
│   └── nor_gate.py                   # Nor (Or + Not), base do SRLatch
├── components/                    # componentes compostos (aritméticos e sequenciais)
│   ├── full_adder.py                # FullAdder: somador completo feito só com Xor/And/Or
│   ├── ripple_carry_adder.py         # RippleCarryAdder: somador de N bits com portas lógicas
│   ├── behavioral_adder.py                 # BehavioralAdder: soma via conversão para int (atalho Python)
│   ├── behavioral_register.py              # BehavioralRegister: registrador por borda de clock, em lógica Python
│   ├── sr_latch.py                   # SRLatch: latch de NOR cruzadas
│   ├── d_latch.py                    # DLatch: latch D transparente
│   ├── d_flip_flop.py                # DFlipFlop: flip-flop D mestre-escravo (só portas)
│   └── d_flip_flop_register.py       # DFlipFlopRegister: N DFlipFlop em paralelo
├── utils/
│   └── binary_conversion.py        # Conversões binário <-> inteiro e padding/truncamento
├── tests/
│   └── test_circuitos.py           # testes automatizados (unittest)
└── latex/                          # texto do TCC
    ├── main.tex                    # documento principal (abnTeX2)
    ├── capitulos/                  # um arquivo .tex por capítulo
    ├── figuras/                    # imagens usadas no documento
    ├── referencias.bib             # referências bibliográficas
    ├── main.pdf                    # TCC compilado
    └── main-diff.pdf               # versão comparativa com as alterações da revisão
```

## Conceito: o modelo reativo por eventos

Todo componente do projeto segue o mesmo contrato:

- Tem uma propriedade `output` (o valor atual do sinal: um `bool` ou uma lista de `bool`, representando um vetor de bits).
- Tem um método `add_listener(callback)`, onde `callback` é uma função `(old, new) -> None` chamada sempre que o componente muda de valor.
- Internamente, ao mudar, o componente chama `trigger_change(old, new)`, recalcula sua própria saída, e então notifica seus próprios listeners.

Isso forma uma **cadeia de propagação**: se você conecta a saída do componente A como entrada do componente B (`A.add_listener(B.trigger_change)`), toda mudança em A dispara automaticamente um recálculo em B, e se algo estiver ligado a B, o efeito continua se propagando.

> **Detalhe de implementação:** os listeners são notificados em ordem **inversa** à que foram adicionados (`self._listeners[::-1]`). Normalmente isso não importa (cada listener recalcula seu próprio estado de forma independente), mas é bom ter em mente se você depender da ordem de execução.

## Referência da API

### `BitArray`

Representa um sinal: um bit único (`bool`) ou um vetor de bits (`list[bool]`).

```python
from signals.bit_array import BitArray

BitArray(initial_value: bool | list[bool])
```

| Membro | Descrição |
|---|---|
| `.output` (get/set) | Lê ou define o valor atual. Ao **definir**, notifica todos os listeners com `(valor_antigo, valor_novo)`. |
| `.add_listener(fn)` | Registra `fn(old, new)` para ser chamada a cada mudança de `.output`. |
| `.trigger_change(old, new)` | Força a propagação de um valor (usado internamente pelas portas/registradores). |

```python
sinal = BitArray([False, True, False])
sinal.add_listener(lambda old, new: print("mudou de", old, "para", new))
sinal.output = [True, True, False]
# mudou de [False, True, False] para [True, True, False]
```

Duas classes auxiliares em `signals/` completam a representação de sinais quando é preciso trabalhar bit a bit dentro de um barramento maior:

| Classe | Descrição |
|---|---|
| `BitSlice(source, index)` | Projeta o bit de índice `index` de um `BitArray` (ou de outro componente multi-bit) como um sinal de 1 bit próprio, que se atualiza automaticamente quando `source` muda. |
| `Bus(bits)` | Faz o caminho inverso: recebe uma lista de componentes de 1 bit (ordenados do mais significativo ao menos significativo) e expõe a concatenação deles como um único sinal de N bits. |

### Portas lógicas: `Not`, `Or`, `And`, `Xor`

Localizadas em `gates/`. Todas seguem a mesma interface: recebem componente(s) de entrada no construtor, se inscrevem como listeners deles, e expõem `.output` já calculado (recalculado automaticamente a cada mudança de entrada).

```python
from gates.not_gate import Not
from gates.or_gate import Or
from gates.and_gate import And
from gates.xor_gate import Xor

Not(input_signal)  # saída = [not b for b in input_signal.output]
Or(a, b)            # saída = [a.output[i] or  b.output[i] for i in range(len(a.output))]
And(a, b)           # saída = [a.output[i] and b.output[i] for i in range(len(a.output))]
Xor(a, b)           # saída = [a.output[i] ^   b.output[i] for i in range(len(a.output))]
```

**Atenção:** `Or`, `And` e `Xor` esperam que `a.output` e `b.output` tenham o **mesmo tamanho** (comparam bit a bit por índice) — por isso, para montar um somador de N bits (que precisa de carry propagando entre posições), é preciso operar bit a bit com `BitSlice` em vez de aplicar essas portas direto sobre o barramento inteiro (ver próxima seção).

Todas expõem `.output` e `.add_listener(fn)`, podendo ser encadeadas como entrada de outras portas, de outro `FullAdder`, do `BehavioralAdder` ou do `BehavioralRegister`.

### Somador com portas lógicas: `FullAdder` e `RippleCarryAdder`

Essa é a forma **recomendada** de montar um somador no simulador: construído inteiramente a partir das portas lógicas básicas, sem nenhum atalho em Python. Ambos ficam em `components/`.

Um somador completo de 1 bit (`FullAdder`) é montado com dois meios-somadores mais uma porta OR para combinar os dois possíveis carries:

```python
from components.full_adder import FullAdder

FullAdder(a, b, carry_in)   # a, b, carry_in: sinais de 1 bit
```

```python
class FullAdder:
    def __init__(self, a, b, carry_in):
        xor_ab = Xor(a, b)
        and_ab = And(a, b)
        and_xor_carry = And(xor_ab, carry_in)

        self.sum = Xor(xor_ab, carry_in)
        self.carry_out = Or(and_ab, and_xor_carry)
```

`FullAdder` expõe `.sum` e `.carry_out` como portas lógicas comuns (cada uma com `.output` e `.add_listener`), prontas para serem usadas como entrada de outro componente.

O `RippleCarryAdder` encadeia N `FullAdder`, um por bit, do menos significativo ao mais significativo, usando `BitSlice` para extrair cada bit dos dois barramentos de entrada e um `Bus` para recompor os N bits de soma em um único sinal:

```python
from components.ripple_carry_adder import RippleCarryAdder

RippleCarryAdder(a, b, carry_in=None)   # a, b: BitArray de N bits
```

```python
a = BitArray([True, True, True])    # 111 = 7
b = BitArray([False, False, True])  # 001 = 1
adder = RippleCarryAdder(a, b)
print(adder.sum.output)        # [False, False, False]  -> 000 (estourou os 3 bits)
print(adder.carry_out.output)  # [True]                 -> sinaliza o overflow
```

Importante: aqui o overflow **não** é tratado por nenhuma função de padding/truncamento. Ele surge naturalmente da topologia do circuito: a soma só tem N fios de saída (um por `FullAdder`), e o "vai-um" do último estágio vira um sinal `carry_out` separado. Se `carry_out` não for conectado a mais nada (como em um contador simples), a informação do estouro se perde e a soma "dá a volta", exatamente como em um contador de hardware real.

### `BehavioralAdder`

O prefixo `Behavioral` segue a terminologia das HDLs: uma descrição **comportamental** diz *o que* o componente faz (aqui, com código Python comum), enquanto uma descrição **estrutural** diz *de quais portas* ele é feito. Os pares do projeto são `BehavioralAdder` ↔ `RippleCarryAdder` e `BehavioralRegister` ↔ `DFlipFlopRegister`.

```python
from components.behavioral_adder import BehavioralAdder

BehavioralAdder(a, b)   # soma dois BitArray (ou qualquer componente com .output e .add_listener)
```

Diferente do `RippleCarryAdder`, o `BehavioralAdder` **não** monta um somador com portas lógicas: ele converte as duas entradas para inteiro, soma, e converte o resultado de volta para bits (usando `utils/binary_conversion.py`). Isso não é uma limitação a ser corrigida, e sim um recurso do simulador: ele demonstra que é possível **misturar um trecho de Python "puro" com o restante do circuito reativo**, útil quando o que se quer testar é outra parte do circuito (por exemplo, o `BehavioralRegister` e a realimentação) e não a aritmética em si — evitando obrigar o estudante a implementar todo componente com portas lógicas o tempo todo.

Internamente usa `utils/binary_conversion.py`:

| Função | O que faz |
|---|---|
| `binary_array_to_int(binary_array)` | Converte `list[bool]` (MSB primeiro) para `int`. |
| `int_to_binary_array(value)` | Converte `int` para `list[bool]` (binário, sem padding). |
| `pad_binary_array(binary_array, length)` | Ajusta o array para ter exatamente `length` bits: preenche com `False` à esquerda se for menor, **e trunca os bits mais significativos se for maior** (simula o overflow/wraparound que, no `RippleCarryAdder`, surge naturalmente do `carry_out` não conectado). |
| `sum_via_integer_conversion(a, b)` | Combina as três funções acima: soma `a + b` como inteiros e devolve um `list[bool]` do mesmo tamanho de `a`. É o que o `BehavioralAdder` usa internamente. |

```python
a = BitArray([False, True, True])   # 011 = 3
b = BitArray([False, False, True])  # 001 = 1
soma = BehavioralAdder(a, b)
print(soma.output)  # [True, False, False]  -> 100 = 4
```

`pad_binary_array` só é usado aqui, dentro de `sum_via_integer_conversion` — é exclusivo do atalho em Python do `BehavioralAdder`. Se o somador for montado com portas lógicas (`RippleCarryAdder`), o overflow é tratado pelo `carry_out`, não por essa função.

### `BehavioralRegister`

Simula um latch/flip-flop controlado por borda de subida (tipo um registrador de hardware com pino de *clock/enable*). É o componente que dá início aos circuitos sequenciais: qualquer circuito com estado (contador, flip-flop, acumulador) depende de um `BehavioralRegister` para "lembrar" um valor entre pulsos de clock.

```python
from components.behavioral_register import BehavioralRegister

BehavioralRegister(clock: BitArray, data_in, feedback_target=None)
```

- `clock`: um `BitArray` **escalar** (`bool`, não lista) usado como clock/enable. A saída do registrador só é atualizada quando `clock.output` sofre uma transição para `True` (transição de nível baixo para alto; aceita clock `bool` ou `[bool]`).
- `data_in`: componente cujo `.output` será "capturado" no instante da borda de subida.
- `feedback_target` (opcional): outro componente com `.trigger_change`, notificado automaticamente da nova saída do registrador; útil para fechar um laço de realimentação (feedback), como no contador.

```python
clock = BitArray(False)
dado = BitArray([True, False, True])
reg = BehavioralRegister(clock, dado)

print(reg.output)      # None (ainda não houve borda de subida)
clock.output = True
print(reg.output)      # [True, False, True]  -> capturou o valor de "dado"

dado.output = [False, False, False]
print(reg.output)      # [True, False, True]  -> não mudou, pois não houve nova borda
clock.output = False
clock.output = True
print(reg.output)      # [False, False, False] -> capturou o novo valor de "dado"
```

## Como rodar

```bash
python main.py
```

Executa o exemplo padrão: um **contador binário de 3 bits** (usando `BehavioralAdder`).

```bash
python experiments.py
```

Executa 12 exemplos (NOT, meio-somador, OR/AND, flip-flop toggle, contador com `BehavioralAdder`, somador completo com portas lógicas, `RippleCarryAdder` com overflow via `carry_out`, contador refeito só com portas lógicas, latch SR, latch D/flip-flop D, toggle com `DFlipFlop` e contador com `DFlipFlopRegister`); ver seção de exemplos abaixo.

```bash
python recursos_observacao.py
```

Demonstra recursos de observação e depuração construídos só com *listeners*: estados transitórios (*glitches*) do somador estrutural, contagem de atividade de chaveamento, sonda com `assert` no latch SR, caminho da propagação reconstruído pela pilha de chamadas e verificação de equivalência entre `RippleCarryAdder` e `BehavioralAdder`.

```bash
python -m unittest discover -s tests -t .
```

Roda os testes automatizados (`tests/test_circuitos.py`), que verificam com `assert` os mesmos resultados apresentados no Capítulo 5 do TCC.

## Exemplos de uso

### 1. Porta NOT reagindo a mudanças

```python
from signals.bit_array import BitArray
from gates.not_gate import Not

a = BitArray([False, True, False])
not_a = Not(a)
print(not_a.output)          # [True, False, True]

a.output = [True, True, True]
print(not_a.output)          # [False, False, False]  -> atualizado automaticamente
```

### 2. Meio-somador (half adder) com Xor + And

Um meio-somador clássico é `soma = A xor B` e `carry = A and B`:

```python
from signals.bit_array import BitArray
from gates.xor_gate import Xor
from gates.and_gate import And

for x, y in [(False, False), (False, True), (True, False), (True, True)]:
    bx, by = BitArray([x]), BitArray([y])
    soma = Xor(bx, by)
    carry = And(bx, by)
    print(f"{int(x)} + {int(y)} -> soma={int(soma.output[0])} carry={int(carry.output[0])}")

# 0 + 0 -> soma=0 carry=0
# 0 + 1 -> soma=1 carry=0
# 1 + 0 -> soma=1 carry=0
# 1 + 1 -> soma=0 carry=1
```

### 3. Registrador (latch) simples

```python
from signals.bit_array import BitArray
from components.behavioral_register import BehavioralRegister

clock = BitArray(False)
dado = BitArray([True, False, False])
reg = BehavioralRegister(clock, dado)

print(reg.output)   # None
clock.output = True
print(reg.output)   # [True, False, False]
```

### 4. Contador binário de 3 bits com BehavioralAdder

Esse é o circuito do `main.py`: um `BehavioralRegister` realimentado por um `BehavioralAdder`, que soma sempre `001` ao valor atual sempre que o clock sobe. Use essa versão quando o que se quer testar/demonstrar é o `BehavioralRegister` e a realimentação, e não a aritmética em si.

```
        ┌────────────┐
   001 ─┤            │
        │  BehavioralAdder ├──► signal ──┐
signal ─┤            │             │
        └────────────┘             ▼
                             ┌────────────┐
                      clock─►│BehavioralRegister├──► signal (realimenta)
                             └────────────┘
```

```python
from signals.bit_array import BitArray
from components.behavioral_adder import BehavioralAdder
from components.behavioral_register import BehavioralRegister

increment = BitArray([False, False, True])     # constante 001
counter_value = BitArray([False, False, False])  # valor atual do contador

adder = BehavioralAdder(increment, counter_value)     # soma = counter_value + 001
clock = BitArray(False)
counter = BehavioralRegister(clock, adder, feedback_target=counter_value)  # realimenta

for _ in range(7):
    clock.output = False
    clock.output = True
    print(counter.output)

# [False, False, True]   -> 1
# [False, True,  False]  -> 2
# [False, True,  True]   -> 3
# [True,  False, False]  -> 4
# [True,  False, True]   -> 5
# [True,  True,  False]  -> 6
# [True,  True,  True]   -> 7
```

Se continuar pulsando o clock, no 8º pulso (`111 + 001 = 1000`) o contador sofre *overflow* e volta para `[False, False, False]` (000), graças ao truncamento feito em `pad_binary_array`.

### 5. Flip-flop toggle (T-FF)

Um T-FF inverte sua própria saída a cada pulso de clock. É a mesma ideia do contador, trocando o `BehavioralAdder` por um `Xor` com uma constante `1`:

```python
from signals.bit_array import BitArray
from gates.xor_gate import Xor
from components.behavioral_register import BehavioralRegister

one = BitArray([True])
clock = BitArray(False)
signal = BitArray([False])          # estado atual do flip-flop

toggle_logic = Xor(signal, one)     # inverte o bit atual
flip_flop = BehavioralRegister(clock, toggle_logic, feedback_target=signal)

for _ in range(4):
    clock.output = False
    clock.output = True
    print(signal.output)

# [True]
# [False]
# [True]
# [False]
```

### 6. Somador completo (FullAdder) com portas lógicas

```python
from signals.bit_array import BitArray
from components.full_adder import FullAdder

a, b, cin = BitArray([True]), BitArray([True]), BitArray([True])
fa = FullAdder(a, b, cin)
print(fa.sum.output)        # [True]   -> 1+1+1 = 11, soma = 1
print(fa.carry_out.output)  # [True]   -> carry = 1
```

### 7. Contador de N bits só com portas lógicas

A mesma ideia do exemplo 4, mas trocando o `BehavioralAdder` por um `RippleCarryAdder`. O overflow aparece sozinho: quando `signal` chega em `111` e soma `001`, `carry_out` vira `[True]` e a soma "dá a volta" para `000`, sem nenhum tratamento especial em código:

```python
from signals.bit_array import BitArray
from components.ripple_carry_adder import RippleCarryAdder
from components.behavioral_register import BehavioralRegister

one = BitArray([False, False, True])
signal = BitArray([False, False, False])
gate_adder = RippleCarryAdder(signal, one)

clock = BitArray(False)
counter = BehavioralRegister(clock, gate_adder.sum, feedback_target=signal)

for _ in range(8):
    clock.output = False
    clock.output = True
    print(counter.output, gate_adder.carry_out.output)

# ... [True, True, True] [False]   -> pulso 7: 111, carry ainda False
# ... [False, False, False] [True] -> logo em seguida, com signal=111, carry_out sobe para True
# pulso 8: [False, False, False] [False]  -> capturou o 000, carry volta a False
```

## Como criar seu próprio circuito

1. **Defina as entradas** como `BitArray`, com o tamanho (número de bits) que seu circuito vai usar. Sinais de controle (clock de um `BehavioralRegister`) podem ser `BitArray(False)` ou `BitArray([False])`; o `DFlipFlop` exige a forma em lista.
2. **Encadeie as portas/componentes** passando as entradas anteriores no construtor (`Xor(a, b)`, `Not(a)`, `FullAdder(a, b, cin)`, `BehavioralRegister(clock, data_in)`). Cada construtor já se registra como listener das entradas.
3. **Prefira montar a lógica com portas** (`Not`/`And`/`Or`/`Xor`, compostas em coisas como `FullAdder`/`RippleCarryAdder`) em vez de atalhos em Python como o `BehavioralAdder`. Use um atalho em Python apenas quando o objetivo do teste for outra parte do circuito, e não o componente que está sendo substituído.
4. **Para operar bit a bit dentro de um barramento maior** (necessário para propagar carry, por exemplo), use `BitSlice(source, index)` para extrair cada bit, e `Bus(lista_de_bits)` para recompor o resultado em um único sinal de N bits.
5. **Para fechar um laço de realimentação** (um componente cuja saída alimenta de volta sua própria entrada, como no contador), use o parâmetro `feedback_target=` do `BehavioralRegister`, passando o `BitArray` que deve ser atualizado a cada borda de clock.
6. **Para observar o circuito**, ou leia `.output` a qualquer momento, ou registre seu próprio listener com `componente.add_listener(lambda old, new: ...)`.
7. **Para "pulsar o clock"**, sempre faça a transição explícita `clock.output = False` seguido de `clock.output = True`. O `BehavioralRegister` só reage quando `clock.output` **muda** para `True` (transição de nível baixo para alto; aceita clock `bool` ou `[bool]`); se a chave já estiver em `True` e você atribuir `True` de novo, nada acontece (não há mudança de valor). Por isso todo pulso precisa passar por `False` antes.

## Limitações conhecidas

- `Or`, `And` e `Xor` assumem que as duas entradas têm **o mesmo número de bits**; não há checagem/erro amigável se os tamanhos divergirem (o código simplesmente vai indexar `b.output[i]` e pode gerar `IndexError`).
- `BehavioralRegister` só suporta um único `clock`; não há reset assíncrono, nem múltiplas entradas de controle.
- Não há detecção de laços combinacionais inválidos (realimentação sem passar por um `BehavioralRegister`), o que poderia causar recursão infinita.

## Possíveis extensões

- Multiplexador / decodificador.
- Reset assíncrono no `BehavioralRegister`.
- Um "gerador de clock" que dispare os pulsos automaticamente (ex.: via loop/`time.sleep`), em vez de alternar `clock.output` manualmente.
- Visualização gráfica do circuito e da propagação dos sinais.

## Compilar o TCC

O texto do TCC (pasta `latex/`) usa a classe **abnTeX2** e o pacote **minted** para as listagens de código. A versão compilada já está em [`latex/main.pdf`](latex/main.pdf); os passos abaixo só são necessários para gerar o PDF de novo após alterar o texto.

**Pré-requisitos**

- Uma distribuição LaTeX: [MiKTeX](https://miktex.org/) (Windows) ou TeX Live (Linux/macOS). No MiKTeX, ative a instalação automática de pacotes ausentes; no TeX Live, a instalação completa (`texlive-full`) já traz tudo.
- Perl, usado pelo `makeglossaries` para gerar a lista de siglas (o Git para Windows e o TeX Live já incluem um).
- O Pygments, instalado no ambiente virtual do projeto:

```bash
python -m pip install -r requirements-tcc.txt
```

**Compilação**

Com o ambiente virtual ativo (para que o Pygments seja encontrado), entre na pasta `latex/` e execute:

```bash
cd latex
pdflatex -shell-escape main.tex
bibtex main
makeglossaries main
pdflatex -shell-escape main.tex
pdflatex -shell-escape main.tex
```

A opção `-shell-escape` é obrigatória, porque o minted chama o Pygments durante a compilação. As três passagens do `pdflatex` resolvem as referências cruzadas, a bibliografia e a lista de siglas. Os arquivos intermediários gerados (`.aux`, `.log`, `.toc`, `.bbl`, `_minted/` etc.) estão no `.gitignore`.
