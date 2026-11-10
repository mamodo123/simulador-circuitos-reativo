"""Composição de vários sinais de 1 bit em um único barramento."""


class Bus:
    """Combina uma lista de sinais de 1 bit (MSB primeiro) em um sinal de N bits."""

    def __init__(self, bits):
        self._bits = bits
        self._output = None
        self._listeners = []

        for bit in self._bits:
            bit.add_listener(self.trigger_change)
        self.trigger_change(None, None)

    def trigger_change(self, old, new):
        previous_output = self._output
        new_value = [bit.output[0] for bit in self._bits]
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
