"""Flip-flop D mestre-escravo: o registrador \"real\", construído só com portas lógicas."""

from gates.not_gate import Not
from components.d_latch import DLatch


class DFlipFlop:
    """Dois DLatch em série; a saída só muda na borda de subida de `clock`."""

    def __init__(self, d, clock, feedback_target=None):
        not_clock = Not(clock)

        self._master = DLatch(d, not_clock)
        self._slave = DLatch(self._master, clock)

        if feedback_target is not None:
            self._slave.add_listener(feedback_target.trigger_change)
            feedback_target.trigger_change(feedback_target.output, self._slave.output)

    @property
    def output(self):
        return self._slave.output

    def add_listener(self, listener):
        self._slave.add_listener(listener)
