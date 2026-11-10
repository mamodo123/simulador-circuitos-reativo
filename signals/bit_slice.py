"""Projeção de um único bit de um sinal maior."""


class BitSlice:
    """Sinal de 1 bit que acompanha, em tempo real, um índice de um sinal de N bits."""

    def __init__(self, source, index):
        self._source = source
        self._index = index
        self._output = None
        self._listeners = []

        self._source.add_listener(self.trigger_change)
        self.trigger_change(None, None)

    def trigger_change(self, old, new):
        previous_output = self._output
        new_value = [self._source.output[self._index]]
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
