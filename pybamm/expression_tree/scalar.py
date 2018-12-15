#
# Scalar class
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
import pybamm


class Scalar(pybamm.Symbol):
    def __init__(self, value, name=None, parent=None):
        super().__init__(name, parent)
        self._value = value

    def evaluate(self, y):
        return self._value
