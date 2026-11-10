from signals.bit_array import BitArray
from components.behavioral_adder import BehavioralAdder
from components.behavioral_register import BehavioralRegister

increment = BitArray([False, False, True])
counter_value = BitArray([False, False, False])
adder = BehavioralAdder(increment, counter_value)

clock = BitArray(False)
counter = BehavioralRegister(clock, adder, feedback_target=counter_value)
print(counter.output)

for _ in range(7):
    clock.output = False
    clock.output = True
    print(counter.output)
