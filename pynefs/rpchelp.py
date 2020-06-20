#!/usr/bin/env python

# This file should be available from
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
import enum as py_enum
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


class packable:
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


class arr(packable):
    """Pack and unpack a fixed-length or variable-length array,
    both corresponding to a Python list"""

    def __init__(self, base_typ, fixed_len, length=None):
        self.base_type: packable = base_typ
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


class opaque_or_string(packable):
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


# so happens that the underlying encodings are the same for opaque and string
opaque = opaque_or_string
string = opaque_or_string


PACKABLE_OR_PACKABLE_CLASS = typing.Union["packable", typing.Type["packable"]]


def rpc_field(serializer: PACKABLE_OR_PACKABLE_CLASS):
    return dataclasses.field(metadata={"serializer": serializer})


@dataclasses.dataclass
class struct(packable, abc.ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_fields(cls) -> typing.Tuple[dataclasses.Field]:
        return dataclasses.fields(cls)

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
            type_hint = first_type.type_hint()
            return f"typing.Union[{type_hint}, {cls.__name__}]"
        return cls.__name__


class linked_list(struct, abc.ABC):
    """Pack and unpack an XDR linked list as a Python list."""

    @classmethod
    def type_hint(cls, want_single=True) -> str:
        return f"typing.List[{super().type_hint(want_single)}]"

    @classmethod
    def pack(cls, p, val_list, want_single=True):
        return p.pack_list(val_list, lambda val: super(linked_list, cls).pack(p, val, want_single))

    @classmethod
    def unpack(cls, up, want_single=True):
        return up.unpack_list(lambda: super(linked_list, cls).unpack(up, want_single))


class union(packable):
    """Pack and unpack a union as a two-membered instance, with
    members switch_name and '_data'.  Note that _data is not a valid
    switch_name, and I use it for that reason, rather than because the
    data member is private."""

    def __init__(self, union_name, switch_decl, switch_name, union_dict, from_parser=False):
        super().__init__()
        self.name = union_name
        self.switch_decl: packable = switch_decl
        self.switch_name: str = switch_name
        self.union_dict: typing.Dict[typing.Any, typing.Tuple[str, packable]] = union_dict
        self.def_typ = self.union_dict.get(None, (None, None))
        self.val_base_class: typing.Optional[typing.Type] = None
        self.from_parser = from_parser

    @property
    def is_simple_option(self):
        """check if the union is basically just a fancy opt_data"""
        type_hints = {k: v[1].type_hint() for k, v in self.union_dict.items()}
        return len(type_hints) == 2 and type_hints.get(False, "") == "None"

    @property
    def val_name(self):
        return "v_" + self.name

    def _sw_val_to_typ(self, sw_val):
        """Get the type descriptor for the arm of the union specified by
        sw_val."""
        typ = self.union_dict.get(sw_val, self.def_typ)[1]
        if typ is None:  # no default clause
            raise BadUnionSwitchException(sw_val)
        return typ

    def type_hint(self) -> str:
        type_hints = {k: (v[0], v[1].type_hint()) for k, v in self.union_dict.items()}
        type_values = list(type_hints.values())
        if self.is_simple_option:
            return f"typing.Optional[{type_hints[True][1]}]"
        if self.val_base_class:
            return self.val_base_class.__name__
        if self.from_parser:
            return self.val_name
        type_str = f"typing.Tuple[{self.switch_decl.type_hint()}, "

        # Might still be able to make just the type hint shorter
        if "None" in type_values and len(type_values) == 2:
            type_values.remove("None")
            return type_str + f"typing.Optional[{', '.join(type_values)}]]"
        return type_str + f"typing.Union[{', '.join(type_values)}]]"

    def pack(self, p, val):
        if self.is_simple_option:
            p.pack_bool(val is not None)
            if val is not None:
                self.union_dict[True][1].pack(p, val)
            return
        if dataclasses.is_dataclass(val):
            sw_val = getattr(val, self.switch_name)
            name = self.union_dict.get(sw_val, self.def_typ)[0]
            if name:
                data = getattr(val, name)
            else:
                # void case
                data = None
        else:
            sw_val, data = val
        self.switch_decl.pack(p, sw_val)
        typ = self._sw_val_to_typ(sw_val)
        typ.pack(p, data)

    def unpack(self, up):
        sw_val = self.switch_decl.unpack(up)
        if self.is_simple_option:
            if sw_val:
                return self.union_dict[True][1].unpack(up)
            return None
        unpacked = self._sw_val_to_typ(sw_val).unpack(up)
        if self.val_base_class:
            name = self.union_dict.get(sw_val, self.def_typ)[0]
            val_dict = {}
            if unpacked is not None:
                val_dict[name] = unpacked
            return self.val_base_class(sw_val, **val_dict)
        return sw_val, unpacked


class opt_data(packable):
    """Pack and unpack an optional value, as either None or the value
    itself.  This choice means that we can't encode declarations which
    resolve to void * in both ways (both void absent, and void
    present).  It looks like the rfc1832 grammar disallows such
    declarations, and they aren't all that useful anyway (since they
    could be replaced w/ a bool with no change in wire format or
    semantic content), so disallowing them seems worth the simplicity
    gain for users of opt_data.  (OTOH, if we had the ML-style
    "option" type ...)"""

    def __init__(self, typ):
        self.typ: packable = typ

    @property
    def is_linked_list(self):
        return isinstance_or_subclass(self.typ, linked_list)

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


class base_type(packable):
    def __init__(self, p, up, python_type: typing.Optional[typing.Type]):
        self.p_proc = p
        self.up_proc = up
        self.python_type = python_type

    def pack(self, p, val):
        self.p_proc(p, val)

    def unpack(self, up):
        return self.up_proc(up)

    def type_hint(self) -> str:
        if not self.python_type:
            return "None"
        return self.python_type.__name__


class enum(packable, py_enum.IntEnum):
    @classmethod
    def type_hint(cls) -> str:
        return cls.__name__

    @classmethod
    def pack(cls, p: xdrlib.Packer, val):
        return p.pack_int(val)

    @classmethod
    def unpack(cls, up: xdrlib.Unpacker):
        return cls(up.unpack_int())


# r_ prefix to avoid shadowing Python names
r_uint = base_type(xdrlib.Packer.pack_uint, xdrlib.Unpacker.unpack_uint, int)
r_int = base_type(xdrlib.Packer.pack_int, xdrlib.Unpacker.unpack_int, int)
r_bool = base_type(xdrlib.Packer.pack_bool, xdrlib.Unpacker.unpack_bool, bool)
r_void = base_type(lambda p, v: None, lambda up: None, None)
r_hyper = base_type(xdrlib.Packer.pack_hyper, xdrlib.Unpacker.unpack_hyper, int)
r_uhyper = base_type(xdrlib.Packer.pack_uhyper, xdrlib.Unpacker.unpack_uhyper, int)
r_float = base_type(xdrlib.Packer.pack_float, xdrlib.Unpacker.unpack_float, float)
r_double = base_type(xdrlib.Packer.pack_double, xdrlib.Unpacker.unpack_double, float)
r_opaque = base_type(xdrlib.Packer.pack_opaque, xdrlib.Unpacker.unpack_opaque, bytes)
r_string = r_opaque
# XXX should add quadruple, but no direct Python support for it.


class Proc:
    """Manage a RPC procedure definition."""

    def __init__(self, name, ret_type, arg_types):
        self.name = name
        self.ret_type: packable = ret_type
        self.arg_types: typing.List[packable] = arg_types

    def __str__(self):
        return "Proc: %s %s %s" % (self.name, str(self.ret_type),
                                   str(self.arg_types))


class Prog:
    """Base class for rpcgen-created server classes."""
    prog: int
    vers: int
    procs: typing.Dict[int, Proc]

    def get_handler(self, proc_id) -> typing.Callable:
        return getattr(self, self.procs[proc_id].name)

    def handle_proc_call(self, proc_id, call_body: bytes) -> bytes:
        proc = self.procs.get(proc_id)
        if proc is None:
            raise NotImplementedError()

        unpacker = xdrlib.Unpacker(call_body)
        argl = [arg_type.unpack(unpacker)
                for arg_type in proc.arg_types]
        rv = self.get_handler(proc_id)(*argl)

        packer = xdrlib.Packer()
        proc.ret_type.pack(packer, rv)
        return packer.get_buffer()
