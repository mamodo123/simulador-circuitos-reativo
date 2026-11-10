"""Somador com descrição comportamental: soma via conversão para inteiro, sem portas lógicas."""

from utils.binary_conversion import sum_via_integer_conversion


class BehavioralAdder:
    """Soma dois barramentos convertendo-os para int; ver RippleCarryAdder para a versão com portas."""

    def __init__(self, a, b):
        self._a = a
        self._b = b
        self._output = None
        self._listeners = []

        self._a.add_listener(self.trigger_change)
        self._b.add_listener(self.trigger_change)
        self.trigger_change(None, None)

    def trigger_change(self, old, new):
        previous_output = self._output
        new_value = sum_via_integer_conversion(self._a.output, self._b.output)
        if new_value == previous_output:
            return self._output
        self._output = new_value
        for listener in self._listeners:
            listener(previous_output, new_value)
        return self._output

    @property
    def output(self):
        return self._output

    def add_listener(self, listener):
        self._listeners.append(listener)
