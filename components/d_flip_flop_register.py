"""Registrador de N bits "real": um DFlipFlop por bit, sem abstração de borda em Python."""

from signals.bit_slice import BitSlice
from signals.bus import Bus
from components.d_flip_flop import DFlipFlop


class DFlipFlopRegister:
    """Contraparte do BehavioralRegister construída só com portas lógicas: N DFlipFlop em paralelo, um por bit, compartilhando o mesmo clock."""

    def __init__(self, clock, data_in, feedback_target=None):
        width = len(data_in.output)
        self._bits = [DFlipFlop(BitSlice(data_in, i), clock) for i in range(width)]
        self._output_bus = Bus(self._bits)

        if feedback_target is not None:
            self._output_bus.add_listener(feedback_target.trigger_change)
            feedback_target.trigger_change(feedback_target.output, self._output_bus.output)

    @property
    def output(self):
        return self._output_bus.output

    def add_listener(self, listener):
        self._output_bus.add_listener(listener)
