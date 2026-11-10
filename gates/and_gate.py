"""Porta lógica AND."""


class And:
    """Calcula o E lógico, bit a bit, entre duas entradas do mesmo tamanho."""

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
        new_value = [self._a.output[i] and self._b.output[i]
                     for i in range(len(self._a.output))]
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
