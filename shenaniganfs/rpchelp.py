#!/usr/bin/env python

# Copyright (c) 2020, Jordan Milne

# This file substantially based on Pinefs, available from
# http://www.pobox.com/~asl2/software/Pinefs
# and is licensed under the X Consortium license:
# Copyright (c) 2003, Aaron S. Lav, asl2@pobox.com
# All rights reserved.

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, provided that the above
# copyright notice(s) and this permission notice appear in all copies of
# the Software and that both the above copyright notice(s) and this
# permission notice appear in supporting documentation.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL
# INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Except as contained in this notice, the name of a copyright holder
# shall not be used in advertising or otherwise to promote the sale, use
# or other dealings in this Software without prior written authorization
# of the copyright holder.

import abc
import dataclasses
import enum
import typing
import xdrlib


def isinstance_or_subclass(val, to_check):
    if isinstance(val, to_check):
        return True
    return isinstance(val, type) and issubclass(val, to_check)


class LengthType(enum.IntEnum):
    VAR = 0
    FIXED = 1


class LengthMismatchException(Exception):
    pass


class BadUnionSwitchException(Exception):
    pass


class Packable:
    @abc.abstractmethod
    def unpack(self, up: xdrlib.Unpacker):
        pass

    @abc.abstractmethod
    def pack(self, p: xdrlib.Packer, val):
        pass

    @classmethod
    @abc.abstractmethod
    def type_hint(cls) -> str:
        pass


class Array(Packable):
    """Pack and unpack a fixed-length or variable-length array,
    both corresponding to a Python list"""

    def __init__(self, base_typ, fixed_len, length=None):
        self.base_type: Packable = base_typ
        self.fixed_len = fixed_len
        self.length = length
        assert (not (fixed_len and length is None))

    def type_hint(self):
        return f"typing.List[{self.base_type.type_hint()}]"

    def pack(self, p, val):
        def pack_one(v):
            self.base_type.pack(p, v)

        if self.fixed_len:
            val_len = len(val)
            if val_len > self.length:
                raise LengthMismatchException(self.length, val_len)
            p.pack_farray(val_len, val, pack_one)
        else:
            p.pack_array(val, pack_one)

    def unpack(self, up):
        def unpack_one():
            return self.base_type.unpack(up)

        if self.fixed_len:
            return up.unpack_farray(self.length, unpack_one)
        else:
            return up.unpack_array(unpack_one)


class Opaque(Packable):
    """Pack and unpack an opaque or string type, both corresponding
    to a Python string"""

    def __init__(self, fixed_len, length=None):
        self.length = length
        self.fixed_len = fixed_len
        assert (not (fixed_len and length is None))

    @classmethod
    def type_hint(cls):
        return "bytes"

    def pack(self, p, val):
        if self.fixed_len:
            val_len = len(val)
            if val_len > self.length:
                raise LengthMismatchException(self.length, val_len)
            p.pack_fopaque(len(val), val)
        else:
            p.pack_opaque(val)

    def unpack(self, up):
        if self.fixed_len:
            return up.unpack_fopaque(self.length)
        else:
            return up.unpack_opaque()


PACKABLE_OR_PACKABLE_CLASS = typing.Union["packable", typing.Type["packable"]]


def rpc_field(serializer: PACKABLE_OR_PACKABLE_CLASS, default=dataclasses.MISSING):
    return dataclasses.field(metadata={"serializer": serializer}, default=default)


@dataclasses.dataclass
class StructUnionBase(Packable, abc.ABC):
    @classmethod
    def get_fields(cls) -> typing.Tuple[dataclasses.Field]:
        return dataclasses.fields(cls)

    @classmethod
    def get_fields_dict(cls) -> typing.Dict[str, dataclasses.Field]:
        return {f.name: f for f in cls.get_fields()}


@dataclasses.dataclass
class Struct(StructUnionBase, abc.ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def have_single_field(cls):
        return len(cls.get_fields()) == 1

    @classmethod
    def pack(cls, p, val, want_single=False):
        if cls.have_single_field() and want_single:
            cls.get_fields()[0].metadata["serializer"].pack(p, val)
            return

        for field in cls.get_fields():
            field.metadata["serializer"].pack(p, getattr(val, field.name))

    @classmethod
    def unpack(cls, up, want_single=False):
        fields = cls.get_fields()
        if cls.have_single_field() and want_single:
            return fields[0].metadata["serializer"].unpack(up)
        return cls(
            **{f.name: f.metadata["serializer"].unpack(up) for f in fields}
        )

    @classmethod
    def type_hint(cls, want_single=False) -> str:
        # If we're a single elem struct (like a linked list) we just
        # (un)pack the bare value
        if cls.have_single_field() and want_single:
            first_type = cls.get_fields()[0].metadata["serializer"]
            return first_type.type_hint()
        return cls.__name__


class LinkedList(Struct, abc.ABC):
    """Pack and unpack an XDR linked list as a Python list."""

    @classmethod
    def type_hint(cls, want_single=True) -> str:
        return f"typing.List[{super().type_hint(want_single)}]"

    @classmethod
    def pack(cls, p, val_list, want_single=True):
        return p.pack_list(val_list, lambda val: super(LinkedList, cls).pack(p, val, want_single))

    @classmethod
    def unpack(cls, up, want_single=True):
        return up.unpack_list(lambda: super(LinkedList, cls).unpack(up, want_single))


UNION_DICT = typing.Dict[typing.Any, typing.Optional[str]]


@dataclasses.dataclass
class Union(StructUnionBase, abc.ABC):
    SWITCH_OPTIONS: typing.ClassVar[UNION_DICT]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def _get_switch_details(cls, sw_val):
        """Get the type descriptor for the arm of the union specified by
        sw_val."""
        if sw_val in cls.SWITCH_OPTIONS:
            field_name = cls.SWITCH_OPTIONS[sw_val]
        elif None in cls.SWITCH_OPTIONS:
            field_name = cls.SWITCH_OPTIONS[None]
        else:
            raise BadUnionSwitchException(sw_val)

        # No field associated with this branch
        if not field_name:
            return None, None
        return field_name, cls.get_fields_dict()[field_name].metadata["serializer"]

    @classmethod
    def type_hint(cls) -> str:
        return cls.__name__

    @classmethod
    def pack(cls, p, val):
        switch_field = cls.get_fields()[0]
        sw_val = getattr(val, switch_field.name)
        switch_field.metadata["serializer"].pack(p, sw_val)

        name, typ = cls._get_switch_details(sw_val)
        # There's a data field associated with this case
        if name is not None:
            typ.pack(p, getattr(val, name))

    @classmethod
    def unpack(cls, up):
        switch_field = cls.get_fields()[0]
        sw_val = switch_field.metadata["serializer"].unpack(up)
        name, typ = cls._get_switch_details(sw_val)
        if name is not None:
            return cls(sw_val, **{name: typ.unpack(up)})
        return cls(sw_val)


class OptData(Packable):
    def __init__(self, typ):
        self.typ: Packable = typ

    @property
    def is_linked_list(self):
        return isinstance_or_subclass(self.typ, LinkedList)

    def type_hint(self) -> str:
        # Ugh. Gross special case because of ambiguity in the IDL.
        # At parse time we don't necessarily know whether this is
        # a pointer to a struct or a linked list-like struct.
        # linked lists are already effectively optional, so don't wrap it.
        if self.is_linked_list:
            return self.typ.type_hint()
        return f"typing.Optional[{self.typ.type_hint()}]"

    def pack(self, p, val):
        if self.is_linked_list:
            return self.typ.pack(p, val)

        if val is None:
            p.pack_bool(False)
        else:
            p.pack_bool(True)
            self.typ.pack(p, val)

    def unpack(self, up):
        if self.is_linked_list:
            return self.typ.unpack(up)

        tmp = up.unpack_bool()
        if tmp:
            return self.typ.unpack(up)
        else:
            return None


class BaseType(Packable):
    def __init__(self, p, up, python_type: typing.Optional[typing.Type]):
        self.p_proc = p
        self.up_proc = up
        self.python_type = python_type

    def pack(self, p, val):
        self.p_proc(p, val)

    def unpack(self, up):
        return self.up_proc(up)

    def type_hint(self) -> str:
        if self.python_type is None:
            return "None"
        return self.python_type.__name__


class Enum(Packable, enum.IntEnum):
    @classmethod
    def type_hint(cls) -> str:
        return f"typing.Union[{cls.__name__}, int]"

    @classmethod
    def pack(cls, p: xdrlib.Packer, val):
        return p.pack_int(val)

    @classmethod
    def unpack(cls, up: xdrlib.Unpacker):
        return cls(up.unpack_int())


# r_ prefix to avoid shadowing Python names
r_uint = BaseType(xdrlib.Packer.pack_uint, xdrlib.Unpacker.unpack_uint, int)
r_int = BaseType(xdrlib.Packer.pack_int, xdrlib.Unpacker.unpack_int, int)
r_bool = BaseType(xdrlib.Packer.pack_bool, xdrlib.Unpacker.unpack_bool, bool)
r_void = BaseType(lambda p, v: None, lambda up: None, None)
r_hyper = BaseType(xdrlib.Packer.pack_hyper, xdrlib.Unpacker.unpack_hyper, int)
r_uhyper = BaseType(xdrlib.Packer.pack_uhyper, xdrlib.Unpacker.unpack_uhyper, int)
r_float = BaseType(xdrlib.Packer.pack_float, xdrlib.Unpacker.unpack_float, float)
r_double = BaseType(xdrlib.Packer.pack_double, xdrlib.Unpacker.unpack_double, float)
r_opaque = BaseType(xdrlib.Packer.pack_opaque, xdrlib.Unpacker.unpack_opaque, bytes)
r_string = r_opaque
# XXX should add quadruple, but no direct Python support for it.


class Proc:
    """Manage a RPC procedure definition."""

    def __init__(self, name, ret_type, arg_types):
        self.name = name
        self.ret_type: Packable = ret_type
        self.arg_types: typing.List[Packable] = arg_types

    def __str__(self):
        return "Proc: %s %s %s" % (self.name, str(self.ret_type),
                                   str(self.arg_types))


def want_ctx(f):
    f.want_ctx = True
    return f


class Prog:
    """Base class for rpcgen-created server classes."""
    prog: int
    vers: int
    min_vers: typing.Optional[int] = None
    procs: typing.Dict[int, Proc]

    def supports_version(self, vers: int) -> bool:
        if self.min_vers is not None:
            return self.min_vers <= vers <= self.vers
        else:
            return self.vers == vers

    def get_handler(self, proc_id) -> typing.Callable:
        return getattr(self, self.procs[proc_id].name)

    async def handle_proc_call(self, call_ctx, proc_id: int, call_body: bytes) -> bytes:
        proc = self.procs.get(proc_id)
        if proc is None:
            raise NotImplementedError()

        unpacker = xdrlib.Unpacker(call_body)
        argl = [arg_type.unpack(unpacker)
                for arg_type in proc.arg_types]
        handler: typing.Callable = self.get_handler(proc_id)
        if getattr(handler, 'want_ctx', False):
            argl = [call_ctx] + argl
        rv = await handler(*argl)

        packer = xdrlib.Packer()
        proc.ret_type.pack(packer, rv)
        return packer.get_buffer()


def addr_to_rpcbind(host: str, port: int) -> bytes:
    # I have literally never seen this address representation
    # outside of RPCBind and I don't like it.
    return f"{host}.{port >> 8}.{port & 0xFF}".encode("utf8")


def rpcbind_to_addr(val: bytes) -> typing.Tuple[str, int]:
    # I have literally never seen this address representation
    # outside of RPCBind and I don't like it.
    host, port_hi, port_lo = val.decode("utf8").rsplit(".", 2)
    return host, ((int(port_hi) << 8) | int(port_lo))
