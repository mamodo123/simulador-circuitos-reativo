"""Porta lógica NOT."""


class Not:
    """Inverte, bit a bit, o sinal de entrada."""

    def __init__(self, input_signal):
        self._input = input_signal
        self._output = None
        self._listeners = []

        self._input.add_listener(self.trigger_change)
        self.trigger_change(None, input_signal.output)

    def trigger_change(self, old, new):
        previous_output = self._output
        new_value = [not bit for bit in self._input.output]
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
