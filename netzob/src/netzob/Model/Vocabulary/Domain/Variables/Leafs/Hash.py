#-*- coding: utf-8 -*-

#+---------------------------------------------------------------------------+
#|          01001110 01100101 01110100 01111010 01101111 01100010            |
#|                                                                           |
#|               Netzob : Inferring communication protocols                  |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011-2017 Georges Bossert and Frédéric Guihéry              |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.netzob.org                                         |
#| @contact  : contact@netzob.org                                            |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#|             Supélec, http://www.rennes.supelec.fr/ren/rd/cidre/           |
#|             ANSSI,   https://www.ssi.gouv.fr                              |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| File contributors :                                                       |
#|       - Frédéric Guihéry <frederic.guihery (a) amossys.fr>                |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Standard library imports                                                  |
#+---------------------------------------------------------------------------+
import hashlib
import abc
from bitarray import bitarray
import binascii

#+---------------------------------------------------------------------------+
#| Related third party imports                                               |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Local application imports                                                 |
#+---------------------------------------------------------------------------+
from netzob.Common.Utils.Decorators import typeCheck, NetzobLogger
from netzob.Model.Vocabulary import partialclass
from netzob.Model.Vocabulary.Domain.Variables.Leafs.AbstractRelationVariableLeaf import AbstractRelationVariableLeaf
from netzob.Model.Vocabulary.AbstractField import AbstractField
from netzob.Model.Vocabulary.Types.HexaString import HexaString
from netzob.Model.Vocabulary.Types.AbstractType import AbstractType, Endianness, Sign
from netzob.Model.Vocabulary.Types.TypeConverter import TypeConverter
from netzob.Model.Vocabulary.Types.BitArray import BitArray
from netzob.Model.Vocabulary.Types.Raw import Raw
from netzob.Model.Vocabulary.Types.Integer import Integer


@NetzobLogger
class Hash(AbstractRelationVariableLeaf):
    r"""The Hash class implements a list of hash relationships between fields.

    The Hash constructor expects some parameters:

    :param targets: The targeted fields of the relationship.
    :param dataType: Specify that the produced value should be
                     represented according to this dataType.
                     If None, default value is Raw(nbBytes=1).
    :param name: The name of the Value variable. If None, the name will be generated.
    :type targets: a :class:`list` of :class:`AbstractField <netzob.Model.Vocabulary.AbstractField>`, required
    :type dataType: :class:`AbstractType <netzob.Model.Vocabulary.Types.AbstractType>`, optional
    :type name: :class:`str`, optional

    Supported hash functions are:

    * md5 (default hash function)
    * sha1
    * sha1-96
    * sha224
    * sha256
    * sha384
    * sha512


    The following examples show how to create a hash relation with
    another field, with different hash functions:

    >>> from netzob.all import *
    >>> f1 = Field(Raw(b'\xaa\xbb'))
    >>> f2 = Field(MD5([f1]))
    >>> s = Symbol(fields = [f1, f2])
    >>> binascii.hexlify(s.specialize())
    b'aabb58cea1f6b2b06520613e09af90dc1c47'

    >>> f2 = Field(SHA1([f1]))
    >>> s = Symbol(fields = [f1, f2])
    >>> binascii.hexlify(s.specialize())
    b'aabb65b1e351a6cbfeb41c927222bc9ef53aad3396b0'

    >>> f2 = Field(SHA1_96([f1]))
    >>> s = Symbol(fields = [f1, f2])
    >>> binascii.hexlify(s.specialize())
    b'aabb65b1e351a6cbfeb41c927222'

    >>> f2 = Field(SHA2_224([f1]))
    >>> s = Symbol(fields = [f1, f2])
    >>> binascii.hexlify(s.specialize())
    b'aabb6b14a319ec360af5bbc69eea2bfb3a7ef278705e742c5b1dd1c11239'

    >>> f2 = Field(SHA2_256([f1]))
    >>> s = Symbol(fields = [f1, f2])
    >>> binascii.hexlify(s.specialize())
    b'aabbd798d1fac6bd4bb1c11f50312760351013379a0ab6f0a8c0af8a506b96b2525a'

    >>> f2 = Field(SHA2_384([f1]))
    >>> s = Symbol(fields = [f1, f2])
    >>> binascii.hexlify(s.specialize())  # doctest: +ELLIPSIS
    b'aabb0f12c407a97010b974d7e08e4b1e452f5336c14eea305c0c84a41d1810c9b1cb1...'

    >>> f2 = Field(SHA2_512([f1]))
    >>> s = Symbol(fields = [f1, f2])
    >>> binascii.hexlify(s.specialize())  # doctest: +ELLIPSIS
    b'aabb13868e66e10c8825be2054b8fa56faf06938a2c6a7e8e3830f0c274777b0431f1...'

    """

    def __init__(self, varType, targets, dataType=None, name=None):
        super(Hash, self).__init__(varType,
                                   dataType=dataType,
                                   targets=targets,
                                   name=name)

    @abc.abstractmethod
    def relationOperation(self, msg):
        """The relationOperation receive a bitarray object and should return a
        bitarray object.

        """
        raise NotImplementedError("Internal Error: 'relationOperation' method not implemented")
