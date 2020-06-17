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
import random
import typing
import xdrlib


fixed = 1
var = 0


class LengthMismatchException(Exception):
    pass


class BadUnionSwitchException(Exception):
    pass


class packable(abc.ABC):
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

    def __init__(self, base_type, fixed_len, length=None):
        self.base_type = base_type
        self.fixed_len = fixed_len
        self.length = length
        assert (not (fixed_len and length is None))

    def type_hint(self):
        inner_hint_func = getattr(self.base_type, 'type_hint')
        if getattr(base_type, 'override', False):
            return inner_hint_func()
        return f"typing.List[{inner_hint_func()}]"

    def check_pack_len(self, v):
        if self.fixed_len and self.length is not None:
            # if it's a fixed type, xdrlib checks
            val_len = len(v)
            if val_len > self.length:
                raise LengthMismatchException(self.length, val_len)

    def pack(self, p, val):
        def pack_one(v):
            self.base_type.pack(p, v)

        self.check_pack_len(val)
        if self.fixed_len:
            p.pack_farray(len(val), val, pack_one)
        else:
            p.pack_array(val, pack_one)

    def unpack(self, up):
        def unpack_one():
            return self.base_type.unpack(up)

        if self.fixed_len:
            return up.unpack_farray(self.length, unpack_one)
        else:
            return up.unpack_array(unpack_one)


class opaque_or_string(arr):
    """Pack and unpack an opaque or string type, both corresponding
    to a Python string"""

    def __init__(self, fixed_len, length=None):
        super().__init__(bytes, fixed_len, length)
        assert (not (fixed_len and length is None))

    @classmethod
    def type_hint(cls):
        return "bytes"
    type_hint.override = True

    def pack(self, p, val):
        self.check_pack_len(val)
        if self.fixed_len:
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


class struct_val_base:
    """Base class for struct or union data.  The packing code for
    struct or union types doesn't require values to be derived
    from this class, but it does provide some minor conveniences."""

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def __repr__(self):
        if hasattr(self, '__slots__'):
            member_dict = dict(
                (k, getattr(self, k, None))
                for k in self.__slots__
            )
        else:
            member_dict = self.__dict__
        return f"<{self.__class__.__name__}: {member_dict!r}>"

    def __str__(self):
        return repr(self)


def struct_val_factory(class_name, class_dict):
    """Create a class type with name class_name, descended from
    struct_or_union_base and object, to be a factory for instantiating
    struct/union values."""
    return type(class_name, (struct_val_base,), class_dict)


class struct_base(packable):
    """Base class for packing/unpacking structs/unions"""
    name: str
    nested_defs_list: typing.List

    def __init__(self, name, elt_list):
        self.name = name
        self.elt_list = elt_list
        # Will only be used for dynamically constructed structs
        self.val_base_class = self.mk_val_class()

    @property
    def val_name(self):
        return "v_" + self.name

    def _base_mk_val_class(self, member_names, nested_typ_list):
        class_dict = {'__slots__': member_names}
        for typ in nested_typ_list:
            if isinstance(typ, struct_base):
                class_dict[typ.name] = typ
        return struct_val_factory(self.val_name, class_dict)

    def mk_val_class(self) -> typing.Type:
        member_names = [elt[0] for elt in self.elt_list]
        return self._base_mk_val_class(member_names, [elt[1] for elt in self.elt_list])

    def __call__(self, **kw):
        return self.val_base_class(**kw)


class struct(struct_base):
    """Pack and unpack an instance with member names as given
    by the structure definition."""

    @property
    def single_elem(self):
        return len(self.elt_list) == 1

    def type_hint(self, want_single=False) -> str:
        # If we're a single elem struct (like a linked list) we just
        # (un)pack the bare value
        val_name = self.val_base_class.__name__
        if self.single_elem and want_single:
            return f"typing.Union[{self.elt_list[0][1].type_hint()}, {val_name}]"
        return val_name

    def pack(self, p, val, want_single=False):
        if self.single_elem and want_single:
            self.elt_list[0][1].pack(p, val)
            return

        for (nm, typ) in self.elt_list:
            typ.pack(p, getattr(val, nm))

    def unpack(self, up, want_single=False):
        if self.single_elem and want_single:
            return self.elt_list[0][1].unpack(up)
        return self(**{nm: typ.unpack(up) for nm, typ in self.elt_list})


class linked_list(struct):
    """Pack and unpack an XDR linked list as a Python list."""

    def type_hint(self, want_single=True) -> str:
        return f"typing.List[{super().type_hint(want_single)}]"

    def pack(self, p, val_list, want_single=True):
        return p.pack_list(val_list, lambda val: super(linked_list, self).pack(p, val, want_single))

    def unpack(self, up, want_single=True):
        return up.unpack_list(lambda: super(linked_list, self).unpack(up, want_single))


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
        self.union_dict: typing.Dict[typing.Any, packable] = union_dict
        self.def_typ = self.union_dict.get(None, None)
        self.val_base_class: typing.Optional[typing.Type] = None
        self.from_parser = from_parser

    @property
    def is_simple_option(self):
        """check if the union is basically just a fancy opt_data"""
        type_hints = {k: v.type_hint() for k, v in self.union_dict.items()}
        return len(type_hints) == 2 and type_hints.get(False, "") == "None"

    @property
    def val_name(self):
        return "v_" + self.name

    def _sw_val_to_typ(self, sw_val):
        """Get the type descriptor for the arm of the union specified by
        sw_val."""
        typ = self.union_dict.get(sw_val, self.def_typ)
        if typ is None:  # no default clause
            raise BadUnionSwitchException(sw_val)
        return typ

    def type_hint(self) -> str:
        type_hints = {k: v.type_hint() for k, v in self.union_dict.items()}
        type_values = list(type_hints.values())
        if self.is_simple_option:
            return f"typing.Optional[{type_hints[True]}]"
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
                self.union_dict[True].pack(p, val)
            return
        sw_val, data = val
        self.switch_decl.pack(p, sw_val)
        typ = self._sw_val_to_typ(sw_val)
        typ.pack(p, data)

    def unpack(self, up):
        sw_val = self.switch_decl.unpack(up)
        if self.is_simple_option:
            if sw_val:
                return self.union_dict[True].unpack(up)
            return None
        unpacked = self._sw_val_to_typ(sw_val).unpack(up)
        if self.val_base_class:
            return self.val_base_class(sw_val, unpacked)
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
        return isinstance(self.typ, linked_list)

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


class Server:
    """Base class for rpcgen-created server classes.  Unpack arguments,
    dispatch to appropriate procedure, and pack return value.  Check,
    at instantiation time, whether there are any procedures defined in the
    IDL which are both unimplemented and whose names are missing from the
    deliberately_unimplemented member.
    As a convenience, allows creation of transport server w/
    create_transport_server.  In what every way the server is created,
    you must call register."""
    prog: int
    vers: int
    procs: typing.Dict[int, Proc]

    def __init__(self):
        pass

    def get_handler(self, proc_id) -> typing.Callable:
        return getattr(self, self.procs[proc_id].name)

    def register(self, transport_server):
        transport_server.register(self.prog, self.vers, self)

    def handle_proc_call(self, proc_id, unpacker: xdrlib.Unpacker) -> bytes:
        proc = self.procs[proc_id]
        if proc is None:
            raise NotImplementedError()

        argl = [arg_type.unpack(unpacker)
                for arg_type in proc.arg_types]
        rv = self.get_handler(proc_id)(*argl)

        packer = xdrlib.Packer()
        proc.ret_type.pack(packer, rv)
        return packer.get_buffer()


class BaseClient(abc.ABC):
    prog: int
    vers: int
    procs: typing.Dict[int, Proc]

    def pack_args(self, proc_id: int, args: typing.List[typing.Any], packer: xdrlib.Packer):
        arg_specs = self.procs[proc_id].arg_types
        if len(args) != len(arg_specs):
            raise ValueError("Wrong number of arguments!")

        for spec, arg in zip(arg_specs, args):
            spec.pack(packer, arg)

    def unpack_return(self, proc_id: int, unpacker: xdrlib.Unpacker):
        return self.procs[proc_id].ret_type.unpack(unpacker)

    def gen_xid(self) -> int:
        return random.getrandbits(32)

    @abc.abstractmethod
    async def connect(self):
        pass

    @abc.abstractmethod
    async def send_call(self, proc_id: int, args: typing.List[typing.Any], xid: typing.Optional[int] = None):
        pass
