"""Registrador com descrição comportamental em Python (não modela latches internos; ver components/d_flip_flop.py)."""


def _is_high(value):
    """Nível lógico de um sinal de clock, seja ele `bool` ou lista de 1 bit (`[bool]`)."""
    if isinstance(value, list):
        return bool(value) and bool(value[0])
    return bool(value)


class BehavioralRegister:
    """Captura `data_in` na borda de subida de `clock` usando lógica Python; ver DFlipFlopRegister para a versão com portas."""

    def __init__(self, clock, data_in, feedback_target=None):
        self._clock = clock
        self._data_in = data_in
        self._output = None
        self._listeners = []

        self._clock.add_listener(self.trigger_change)
        if feedback_target is not None:
            self.add_listener(feedback_target.trigger_change)

    def trigger_change(self, old, new):
        previous_output = self._output
        if not _is_high(old) and _is_high(new):
            self._output = self._data_in.output
            for listener in self._listeners:
                listener(previous_output, self._output)
        return self._output

    @property
    def output(self):
        return self._output

    def add_listener(self, listener):
        self._listeners.append(listener)
