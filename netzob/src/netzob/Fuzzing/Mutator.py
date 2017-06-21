# -*- coding: utf-8 -*-

# +---------------------------------------------------------------------------+
# |          01001110 01100101 01110100 01111010 01101111 01100010            |
# |                                                                           |
# |               Netzob : Inferring communication protocols                  |
# +---------------------------------------------------------------------------+
# | Copyright (C) 2011-2017 Georges Bossert and Frédéric Guihéry              |
# | This program is free software: you can redistribute it and/or modify      |
# | it under the terms of the GNU General Public License as published by      |
# | the Free Software Foundation, either version 3 of the License, or         |
# | (at your option) any later version.                                       |
# |                                                                           |
# | This program is distributed in the hope that it will be useful,           |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of            |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
# | GNU General Public License for more details.                              |
# |                                                                           |
# | You should have received a copy of the GNU General Public License         |
# | along with this program. If not, see <http://www.gnu.org/licenses/>.      |
# +---------------------------------------------------------------------------+
# | @url      : http://www.netzob.org                                         |
# | @contact  : contact@netzob.org                                            |
# | @sponsors : Amossys, http://www.amossys.fr                                |
# |             Supélec, http://www.rennes.supelec.fr/ren/rd/cidre/           |
# |             ANSSI,   https://www.ssi.gouv.fr                              |
# +---------------------------------------------------------------------------+

# +---------------------------------------------------------------------------+
# | File contributors :                                                       |
# |       - Frédéric Guihéry <frederic.guihery (a) amossys.fr>                |
# |       - Rémy Delion <remy.delion (a) amossys.fr>                          |
# +---------------------------------------------------------------------------+

# +---------------------------------------------------------------------------+
# | Standard library imports                                                  |
# +---------------------------------------------------------------------------+
import abc

# +---------------------------------------------------------------------------+
# | Related third party imports                                               |
# +---------------------------------------------------------------------------+

# +---------------------------------------------------------------------------+
# | Local application imports                                                 |
# +---------------------------------------------------------------------------+
from netzob.Common.Utils.Decorators import typeCheck
from netzob.Model.Grammar.Automata import Automata  # noqa: F401


class Mutator(metaclass=abc.ABCMeta):
    """The model of any mutator.

    This class provides the common properties and API to all inherited mutators.

    **Mutators for message formats fuzzing**

    Mutators may be used during symbol specialization process, in
    order to fuzz targeted fields variables. Mutators are specified in
    the ``symbol.specialize()`` through the ``mutators=``
    parameter. This parameter expects a dict containing fields objects
    for its keys and Mutators objects for its values. We can provide
    parameters to mutators by using tuple as values of the dict.

    The Mutator constructor expects some parameters:

    :param domain: The domain of the field to mutate, in case of a data
        mutator.
    :param automata: The automata to mutate, in case of an automata mutator.
    :param mode: If set to **MutatorMode.GENERATE**, :meth:`generate` will be
        used to produce the value.
        If set to **MutatorMode.MUTATE**, :meth:`mutate` will be used to
        produce the value (not implemented).
        Default value is **MutatorMode.GENERATE**.
    :type domain: :class:`AbstractVariable
        <netzob.Model.Vocabulary.Domain.Variables.AbstractVariable>`, optional
    :type automata: :class:`Automata
        <netzob.Model.Grammar.Automata>`, optional
    :type mode: :class:`int`, optional

    The following code shows the instantiation of a symbol composed of
    a string and an integer, and the fuzzing request during the
    specialization process:

    >>> from netzob.all import *
    >>> f1 = Field(String())
    >>> f2 = Field(Integer())
    >>> symbol = Symbol(fields=[f1, f2])
    >>> mutators = {f1: StringMutator,
    ...             f2: (PseudoRandomIntegerMutator, minValue=12, maxValue=20)}  # doctest: +SKIP
    >>> symbol.specialize(mutators=mutators)  # doctest: +SKIP


    Constant definitions :
    """
    SEED_DEFAULT = 10
    COUNTER_MAX_DEFAULT = 2**16

    def __init__(self,
                 seed=SEED_DEFAULT,
                 counterMax=COUNTER_MAX_DEFAULT
                 ):
        # Handle class variables
        self._seed = seed
        self._currentState = 0
        self._counterMax = counterMax
        self._currentCounter = 0

    @typeCheck(int)
    def updateSeed(self, seedValue):
        self._seed = seedValue

    @property
    def currentState(self):
        """
        Property (getter/setter).
        The current state of the pseudo-random generator.
        the generator can reproduce a value by using this state.

        :type: :class:`int`
        """
        return self._currentState

    @currentState.setter
    @typeCheck(int)
    def currentState(self, stateValue):
        self._currentState = stateValue

    @property
    def counterMax(self):
        """
        Property (getter/setter).
        The max number of values that the generator has to produce.
        When this limit is reached, mutate() returns None.

        :type: :class:`int`
        """
        return self._counterMax

    @counterMax.setter
    @typeCheck(int)
    def counterMax(self, counterMaxValue):
        self._counterMax = counterMaxValue

    @property
    def currentCounter(self):
        """
        Property (getter).
        The counter of mutate() calls.
        In mutate(), this value is compared to counterMax, to determine if the
        limit of mutation is reached.

        :type: :class:`int`
        """
        return self._currentCounter

    def resetCurrentCounter(self):
        """Reset the current counter of mutate().

        :type: :class:`int`
        """
        self._currentCounter = 0

    def reset(self):
        """Reset environment of the mutator.
        """
        self._currentCounter = 0

    def generate(self):
        """This is the fuzz generation method of the field domain. It has to
        be overridden by all the inherited mutators which call the
        generate() function.

        :return: a generated content represented with bytes
        :rtype: :class:`bytes`
        :raises: :class:`Exception` when **currentCounter** reaches \
**counterMax**.
        """
        if self._currentCounter >= self.counterMax:
            raise Exception("Max mutation counter reached")
        self._currentCounter += 1

    @abc.abstractmethod
    def mutate(self, *args):
        """This is the mutation method of the field domain. It has to be
        overridden by all the inherited mutators which call the
        mutate() function.

        If the currentCounter reached counterMax, mutate() returns None.

        :param data: The data to mutate.
        :type data: :class:`bitarray.bitarray`
        :return: a generated content represented with bytes
        :rtype: :class:`bytes`

        :meth:`mutate` is an *abstract method* and must be inherited.
        """
