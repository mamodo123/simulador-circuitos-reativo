"""Barramento de bits reativo: a peça mais básica do simulador."""


class BitArray:
    """Sinal de 1 ou N bits que notifica listeners sempre que seu valor muda."""

    def __init__(self, initial_value):
        self._output = initial_value
        self._listeners = []

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        previous_output = self._output
        if value == previous_output:
            return
        self._output = value
        for listener in self._listeners:
            listener(previous_output, value)

    def add_listener(self, listener):
        self._listeners.append(listener)

    def trigger_change(self, old, new):
        self.output = new
        return self._output
