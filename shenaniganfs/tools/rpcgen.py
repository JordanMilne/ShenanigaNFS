#!/usr/bin/env python

# Copyright (c) 2020, Jordan Milne

# This file substantially based on Pinefs, available from
# http://www.pobox.com/~asl2/software/Pinefs
# and is licensed under the X Consortium license:
# Copyright(c) 2003, Aaron S. Lav, asl2@pobox.com
# All rights reserved. 

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files(the
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
import os
import re
import string
import sys
import tempfile

import typing
from io import StringIO

from ply import lex
from ply import yacc

from shenaniganfs import rpchelp


class LexError(Exception):
    pass


class ParseError(Exception):
    pass


tokens = ('LPAREN', 'RPAREN', 'LBRACK', 'RBRACK', 'LANGLE', 'RANGLE',
          'STAR', 'COMMA', 'COLON', 'VOID', 'UNSIGNED', 'TYPE',
          'ENUM', 'LCBRACK', 'RCBRACK', 'EQ', 'STRUCT', 'UNION',
          'SWITCH', 'CASE', 'DEFAULT', 'CONST', 'SEMICOLON', 'IDENT',
          'CONSTVAL', 'OPAQUE', 'STRING', 'TYPEDEF', 'PROGRAM', 'VERSION')

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LANGLE = r'<'
t_RANGLE = r'>'
t_STAR = r'\*'
t_COMMA = r','
t_COLON = r':'
t_LCBRACK = r'{'
t_RCBRACK = r'}'
t_EQ = r'='
t_SEMICOLON = r';'

reserved_tuple = (
    # RFC 1832, XDR
    'void',
    'unsigned',
    'opaque',
    'string',
    'enum',
    'struct',
    'union',
    'switch',
    'case',
    'default',
    'const',
    'typedef',
    # RFC 1831, RPC
    'program',
    'version')

types = ('int', 'hyper', 'float', 'double', 'quadruple', 'bool', 'long', 'string', 'opaque')

py_reserved_words = ['def', 'print', 'del', 'pass', 'break', 'continue',
                     'return', 'yield', 'raise', 'import', 'from',
                     'global', 'exec', 'assert', 'if', 'while', 'else',
                     'for', 'in', 'try', 'finally', 'except', 'and',
                     'not', 'or', 'is', 'lambda', 'class']

reserved_dict = {
    **{k: k.upper() for k in reserved_tuple},
    **{t: "TYPE" for t in types}
}


def t_CONSTVAL(t):
    r"""(0x[0-9A-Fa-f]+)|(-?\d+)"""
    return t


def t_COMMENT(t):
    r"""/\*(.|\n)*?\*/"""
    t.lexer.lineno += t.value.count('\n')
    return None


def t_NEWLINE(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")


t_ignore = " \t"


def needs_escaping(val):
    """Check whether this identifier is a valid IDL but not Python identifier,
    or whether it would otherwise be an escaped IDL identifier. (Escaping
    is done by appending a '_', if the identifier, once stripped of all
    trailing underscores, is a Python keyword."""
    while val[-1] == '_':
        val = val[:-1]
    return val in py_reserved_words


def t_IDENT(t):
    r"""[a-zA-Z]([a-zA-Z]|_|[0-9])*"""
    t.type = reserved_dict.get(t.value, 'IDENT')
    if needs_escaping(t.value):
        t.value += '_'
    return t


def t_error(t):
    raise LexError(t)


class RecasedName(str):
    pass


class Ctx:
    # mostly specific to RPC2 / NFS
    NAME_REPLACEMENTS: typing.List[typing.Tuple[typing.Any, str]] = [
        (r"ok(\d*)$", r"OK\1"),
        (r"fail(\d*)$", r"Fail\1"),
        (r"rpc", r"RPC"),
        (r"rpcb", r"RPCB"),
        (r"nfs", r"NFS"),
        (r"attr(\d*)$", r"Attr\1"),
        (r"data(\d*)$", r"Data\1"),
        (r"stat(\d*)$", r"Stat\1"),
        (r"time(\d*)$", r"Time\1"),
        (r"args(\d*)$", r"Args\1"),
        (r"handle(\d*)$", r"Handle\1"),
        (r"path(\d*)$", r"Path\1"),
        (r"list(\d*)$", r"List\1"),
        (r"res(\d*)$", r"Res\1"),
        (r"status(\d*)$", r"Status\1"),
        (r"dat(\d*)$", r"Dat\1"),
        (r"^fh", r"FH"),
    ]

    def __init__(self, remap_names=False):
        self.indent = 0
        self.remap_names = remap_names
        self.deferred_list = []  # used for deferring nested Enum definitions
        self.progs: typing.List["Program"] = []
        self.type_mapping: typing.Dict[str, rpchelp.PACKABLE_OR_PACKABLE_CLASS] = {}
        self.const_mapping: typing.Dict[str, int] = {}
        self.locals = {}
        self.globals = {}

    def exec(self, src):
        # Gross. This file probably needs to be totally rewritten.
        # Might be ok to construct the classes instead and give them
        # a __repr__ that will completely recreate them?
        try:
            exec(src, self.globals, self.locals)
            self.globals.update(self.locals)
        except Exception:
            print(src, file=sys.stderr)
            print(self.locals, file=sys.stderr)
            raise

    def get_name(self, name: str):
        if not self.remap_names:
            return name
        if isinstance(name, RecasedName):
            return name
        if "." in name or name in reserved_tuple or name in types:
            return name
        if not any(x in string.ascii_lowercase for x in name):
            return name

        no_underscore = name.replace("_", "")
        name = name.title().replace("_", "")
        for regex, replace in self.NAME_REPLACEMENTS:
            if not isinstance(regex, re.Pattern):
                regex = re.compile(regex, re.I)
            name = regex.sub(replace, name)

        # Never make a character that was uppercase lowercase
        name = ''.join(min(old, new) for old, new in zip(no_underscore, name))
        return name

    def defer(self, val):
        self.deferred_list.append(val)

    def defer_prog(self, val):
        self.progs.append(val)

    def finish(self):
        return "\n".join(self.deferred_list)

    def collect_types(self):
        self.type_mapping.clear()
        self.const_mapping.clear()
        for name, val in self.locals.items():
            if rpchelp.isinstance_or_subclass(val, rpchelp.Packable):
                self.type_mapping[name] = val
            elif isinstance(val, int):
                self.const_mapping[name] = val

    def finish_progs(self):
        val = ""
        if self.progs:
            # Make sure this doesn't get printed for rfc1831 so we
            # don't get weird circular imports.
            val = "from shenaniganfs import client\n"
        return val + "\n".join("\n".join(
            [p.str_one_vers(self, vers) for vers in p.versions.children] +
            [p.str_one_vers(self, vers, as_client=True) for vers in p.versions.children]
        ) for p in self.progs)

    def finish_exports(self):
        prog_names = []
        for prog in self.progs:
            for vers in prog.versions.children:
                for variant in ("SERVER", "CLIENT"):
                    prog_names.append(f"{prog.ident}_{vers.version_id}_{variant}")
        exportable_types = list({**self.const_mapping, **self.type_mapping}.keys())
        return f"__all__ = {repr(prog_names + exportable_types)}"


class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.name = None
        self.children = children or []

    def set_ident(self, ident):
        """Sets name(currently only used to get struct/union tags into
        the right place)"""
        pass

    def visit(self, visitor):
        visitor.visit(self)

        seen = set()

        # Be careful, visitor may mutate tree.
        for key, val in list(self.__dict__.items()):
            if key == "children":
                continue
            if val is self:
                continue
            if not isinstance(val, Node):
                continue
            if id(val) in seen:
                continue
            seen.add(id(val))
            val.visit(visitor)
        for node in self.children[:]:
            if id(node) in seen:
                continue
            seen.add(id(node))
            node.visit(visitor)

        visitor.leave()

    def to_str(self, ctx):
        raise NotImplementedError(f'{self.__class__.__name__}.to_str()')


class NodeList(Node):
    sep = '\n'

    def __init__(self, node, node_list=None):
        Node.__init__(self)
        self.children = [node]
        if node_list is not None:
            self.children.extend(node_list.children)

    def to_str(self, ctx):
        str_children = [c.to_str(ctx) for c in self.children]
        return self.sep.join(str_children)


class NodeListComma(NodeList):
    sep = ', '


class Specification(NodeList):
    pass


class SimpleType(Node):
    def __init__(self, typ, ident):  # ident can be None
        Node.__init__(self)
        typ.set_ident(ident)
        self.typ = typ
        self.ident = ident

    def to_str(self, ctx):
        return self.typ.to_str(ctx)


class ArrType(Node):
    def __init__(self, typ, ident, var_fixed, maxind=None):
        Node.__init__(self)
        self.ident = ident
        self.typ = typ
        self.var_fixed = var_fixed
        self.maxind = maxind

    def to_str(self, ctx):
        var_fixed = ['rpchelp.LengthType.VAR', 'rpchelp.LengthType.FIXED'][self.var_fixed]
        is_string = False
        typ = self.typ
        if self.typ in ['string', 'opaque']:
            is_string = True
        elif isinstance(self.typ, TypeSpec) and self.typ.val in ['string', 'opaque']:
            is_string = True
            typ = self.typ.val

        if is_string:
            # Encoding is unspecified so strings are byte strings too
            str_class_map = {
                'opaque': 'Opaque',
                'string': 'Opaque',
            }
            return 'rpchelp.%s(%s, %s)' % (str_class_map[typ], var_fixed, self.maxind)
        return 'rpchelp.Array(%s, %s, %s)' % (
            typ.to_str(ctx), var_fixed, self.maxind)


class OptData(Node):
    def __init__(self, type_spec, ident):
        self.type_spec = type_spec
        self.ident = ident
        Node.__init__(self)

    def to_str(self, ctx):
        return 'rpchelp.OptData(%s)' % (self.type_spec.to_str(ctx))


class TypeSpec(Node):
    unsignable = {'int': 'uint', 'hyper': 'uhyper'}

    def __init__(self, val, unsigned, base, compound=0):
        Node.__init__(self)
        if val == "long":
            val = "int"
        if unsigned:
            v = self.unsignable.get(val, None)
            if v is None:
                raise ParseError(val + ' cannot be combined w/ unsigned ')
            val = v
        self.base = base
        self.compound = compound
        self.val = val

    def set_ident(self, ident):
        if self.compound:
            self.val.set_ident(ident)

    def to_str(self, ctx):
        if self.base:
            return 'rpchelp.r_' + self.val
        else:
            if self.compound:
                return self.val.to_str(ctx)
            return ctx.get_name(self.val)


class Enum(Node):
    def __init__(self, body):
        Node.__init__(self)
        self.body = body

    def to_str(self, ctx):
        return self.body.to_str(ctx)


class EnumList(NodeList):
    sep = '\n'


class EnumClause(Node):
    def __init__(self, ident, val):
        Node.__init__(self)
        self.ident = ident
        self.val = val

    def to_str(self, ctx):
        # For now we need both a bare and enum class version, defer.
        val = '%s = %s' % (self.ident, self.val)
        ctx.exec(val)
        ctx.defer(val)
        return '\t' + val


class Struct(Node):
    def __init__(self, body):
        Node.__init__(self)
        self.body = body

    def set_ident(self, ident):
        self.body.name = ident

    def to_str(self, ctx):
        return self.body.to_str(ctx)


class StructList(NodeList):
    def to_str(self, ctx):
        children = []
        have_tail_pointer = False
        for (decl, i) in zip(self.children, range(0, len(self.children))):
            # Self-referential tail pointer means we get treated like a linked list
            if (self.name and isinstance(decl, OptData)
                    and decl.type_spec.val == self.name):
                # If it's not actually a tail pointer something's very wrong
                if i != len(self.children) - 1:
                    raise ValueError(f"Self-referential pointer not at end of struct in {self.name}")
                have_tail_pointer = True
            else:
                children.append((decl.ident, decl.to_str(ctx)))
        class_name = "Struct"
        if have_tail_pointer:
            class_name = "LinkedList"
        buf = f"\n\n\n@dataclass\nclass {ctx.get_name(self.name)}(rpchelp.{class_name}):  # {self.name}\n"
        for field in children:
            field_type = eval(field[1], globals(), ctx.locals)
            field_data = ' = rpchelp.rpc_field(%s)' % field[1]
            buf += f"\t{field[0]}: {field_type.type_hint()}{field_data}\n"
        buf += "\n\n\n"
        ctx.exec(buf)
        return buf


class Union(Node):
    def __init__(self, body):
        self.body = body
        Node.__init__(self)

    def set_ident(self, ident):
        self.body.name = ident

    def to_str(self, ctx):
        return self.body.to_str(ctx)


class UnionBody(Node):
    def __init__(self, sw_decl, body):
        self.sw_decl = sw_decl
        self.body = body
        Node.__init__(self)

    def to_str(self, ctx):
        buf = f"\n\n\n@dataclass\nclass {ctx.get_name(self.name)}(rpchelp.Union):  # {self.name}\n"
        fields = {k: v for (k, v) in self.body.to_fields(ctx)}
        switch_options = ", ".join("%s: %r" % (k, v[0]) for (k, v) in fields.items())
        buf += f"\tSWITCH_OPTIONS = {{{switch_options}}}\n"

        sw_field = (self.sw_decl.ident, self.sw_decl.typ.to_str(ctx))
        field_type = eval(sw_field[1], globals(), ctx.locals)
        field_data = ' = rpchelp.rpc_field(%s)' % sw_field[1]
        buf += f"\t{sw_field[0]}: {field_type.type_hint()}{field_data}\n"

        # Don't output dupes of fields used in multiple branches
        for field in sorted(set(fields.values()), key=lambda x: str(x)):
            if not field[0]:
                continue
            field_type = eval(field[1], globals(), ctx.locals)
            field_data = f' = rpchelp.rpc_field({field[1]}, default=None)'
            buf += f"\t{field[0]}: typing.Optional[{field_type.type_hint()}]{field_data}\n"
        buf += "\n\n\n"
        ctx.exec(buf)
        return buf


class UnionList(NodeListComma):
    def __init__(self, node, node_list=None):
        super().__init__(node, node_list=node_list)
        self.children = sorted(self.children, key=lambda x: x.decl.ident or "")

    def to_fields(self, ctx):
        for child in self.children:
            yield child.to_field(ctx)


class UnionElt(Node):
    def __init__(self, val, decl):
        Node.__init__(self)
        self.val = val
        self.decl = decl

    def to_str(self, ctx):
        typestr = self.decl.to_str(ctx)
        return "%s: (%r, %s)" % (self.val, self.decl.ident, typestr)

    def to_field(self, ctx):
        return self.val, (self.decl.ident, self.decl.to_str(ctx))


class UnionDefElt(UnionElt):
    def __init__(self, decl):
        Node.__init__(self)
        self.val = 'None'
        self.decl = decl


class VersionList(NodeList):
    pass


class ProcedureList(NodeListComma):
    @staticmethod
    def _common_prefix(vals):
        if not vals:
            return ""
        prefix = vals[-1]
        for val in vals:
            shortest = min(len(prefix), len(val))
            prefix = prefix[:shortest]
            last_match = 0
            for x, y in zip(prefix, val[:shortest]):
                if x != y:
                    break
                last_match += 1
            prefix = prefix[:last_match]
        return prefix

    def remove_common_prefix(self):
        prefix = self._common_prefix([p.ident for p in self.children])
        if not prefix:
            return
        for proc in self.children:
            proc.ident = proc.ident[len(prefix):]


class TypeSpecList(NodeList):
    sep = ', '


class Const(Node):
    def __init__(self, ident, val):
        Node.__init__(self)
        self.ident = ident
        self.val = val

    def to_str(self, ctx):
        val = '%s = %s' % (ctx.get_name(self.ident), self.val)
        ctx.exec(val)
        return val


class TypeDef(Node):
    def __init__(self, decl):
        Node.__init__(self)
        self.decl = decl

    def to_str(self, ctx):
        if self.decl.ident is None:
            # a legit construction according to my reading of the grammar, but not
            # semantically useful.
            return '# "typedef void;" encountered'
        typestr = self.decl.to_str(ctx)
        val = '%s = %s' % (ctx.get_name(self.decl.ident), typestr)
        ctx.exec(val)
        return val


class TypeDefCompound(Node):
    def __init__(self, ident, typ, body):
        body.name = ident
        Node.__init__(self)
        self.ident = ident
        self.typ = typ
        self.body = body

    def to_str(self, ctx):
        new_ident = ctx.get_name(self.ident)
        body_str = self.body.to_str(ctx)
        if self.typ == "enum":
            val = "\n\n\nclass %s(rpchelp.Enum):  # %s\n%s\n\n\n" % (new_ident, self.ident, body_str)
        elif self.typ in ("struct", "union"):
            val = body_str
        else:
            raise ValueError(f"Unknown compound typedef {self.typ}")
        ctx.exec(val)
        return val


class Program(Node):
    def __init__(self, ident, versions, program_id):
        Node.__init__(self)
        self.ident = ident
        self.versions = versions
        self.program_id = program_id

    def str_one_vers(self, ctx, vers, as_client=False):
        class_suffix = "CLIENT" if as_client else "SERVER"
        base_class = "client.BaseClient" if as_client else "rpchelp.Prog"
        class_decl = f'\n\n\nclass {self.ident}_{vers.version_id}_{class_suffix}({base_class}):'
        prog = 'prog = %s' % (self.program_id,)
        vers_str = 'vers = %s' % (vers.version_id,)
        procs_str = "procs = {\n"
        for proc in vers.proc_defs.children:
            proc.simplify_parms()
            procs_str += f"\t\t{proc.proc_id}: {proc.to_str(ctx)},\n"
        procs_str += "\t}\n"

        funcs_str = ""

        def _get_type(p_typ):
            if p_typ.base:
                return getattr(rpchelp, 'r_' + p_typ.val)
            return ctx.type_mapping[ctx.get_name(p_typ.val)]

        for proc in vers.proc_defs.children:
            if not as_client:
                funcs_str += "\t@abc.abstractmethod\n"
            funcs_str += f"\tasync def {proc.ident}(self"
            for i, parm_type in enumerate(proc.parm_list.children):
                funcs_str += f", arg_{i}: {_get_type(parm_type).type_hint()}"
            ret_type_hint = _get_type(proc.ret_type).type_hint()
            if as_client:
                funcs_str += f") -> client.UnpackedRPCMsg[{ret_type_hint}]:\n"
            else:
                funcs_str += f") -> {ret_type_hint}:\n"
            if as_client:
                arg_list = ', '.join(f"arg_{i}" for i in range(len(proc.parm_list.children)))
                funcs_str += f"\t\treturn await self.send_call({proc.proc_id}, {arg_list})\n\n"
            else:
                funcs_str += "\t\traise NotImplementedError()\n\n"

        return "\n\t".join([class_decl, prog, vers_str, procs_str]) + "\n" + funcs_str

    def to_str(self, ctx):
        ctx.defer_prog(self)
        return ""


class Version(Node):
    def __init__(self, ident, proc_defs, version_id):
        Node.__init__(self)
        self.ident = ident
        proc_defs.remove_common_prefix()
        # All programs have an implicit NULL procedure
        if not any(str(proc.proc_id) == "0" for proc in proc_defs.children):
            void_spec = TypeSpec("void", False, True, False)
            proc_defs.children.insert(0, Procedure("NULL", void_spec, TypeSpecList(void_spec), 0))
        self.proc_defs = proc_defs
        self.version_id = version_id

    def to_str(self, ctx):
        return ""


class Procedure(Node):
    def __init__(self, ident, ret_type, parm_list, proc_id):
        Node.__init__(self)
        self.ident = ident
        self.ret_type = ret_type
        self.parm_list = parm_list
        self.proc_id = proc_id

    def simplify_parms(self):
        if len(self.parm_list.children) != 1:
            return
        if self.parm_list.children[0].val != "void":
            return
        # Single void param is the same as no params
        self.parm_list.children.clear()

    def to_str(self, ctx):
        return "rpchelp.Proc('%s', %s, [%s])" % (self.ident, self.ret_type.to_str(ctx), self.parm_list.to_str(ctx))


def p_specification_1(t):
    """specification : definition specification
    | program_def specification"""
    t[0] = Specification(t[1], t[2])


def p_specification_2(t):
    """specification : definition
    | program_def"""
    t[0] = Specification(t[1])


def p_decl_1(t):
    """declaration : type_specifier IDENT"""
    t[0] = SimpleType(t[1], t[2])


def p_decl_2(t):
    """declaration : type_specifier IDENT LBRACK value RBRACK"""
    t[0] = ArrType(t[1], t[2], rpchelp.LengthType.FIXED, t[4])


def p_decl_3(t):
    """declaration : type_specifier IDENT LANGLE value RANGLE"""
    t[0] = ArrType(t[1], t[2], rpchelp.LengthType.VAR, t[4])


def p_decl_4(t):
    """declaration : type_specifier IDENT LANGLE RANGLE"""
    t[0] = ArrType(t[1], t[2], rpchelp.LengthType.VAR)


def p_decl_5(t):
    """declaration : OPAQUE IDENT LBRACK value RBRACK"""  # fixed opaque
    t[0] = ArrType('Opaque', t[2], rpchelp.LengthType.FIXED, t[4])


def p_decl_6(t):
    """declaration : OPAQUE IDENT LANGLE value RANGLE
    | STRING IDENT LANGLE value RANGLE"""  # var-len opaque/string
    t[0] = ArrType(t[1], t[2], rpchelp.LengthType.VAR, t[4])


def p_decl_7(t):
    """declaration : OPAQUE IDENT LANGLE RANGLE
    | STRING IDENT LANGLE RANGLE"""  # var-len opaque/string
    t[0] = ArrType(t[1], t[2], rpchelp.LengthType.VAR)


def p_decl_8(t):  # optional data
    """declaration : type_specifier STAR IDENT"""
    t[0] = OptData(t[1], t[3])


def p_decl_9(t):
    """declaration : void"""
    t[0] = SimpleType(t[1], None)


def p_void(t):
    """void : VOID"""
    t[0] = TypeSpec(t[1], unsigned=0, base=1)


def p_value(t):
    """value : CONSTVAL
    | IDENT"""
    t[0] = t[1]


# XXX some idl uses "unsigned" by itself(= unsigned int).
# Should revise grammar to allow 1 or more TYPE, sort out semantics
# later
def p_type_spec_1(t):
    """type_specifier : UNSIGNED TYPE"""
    t[0] = TypeSpec(t[2], unsigned=1, base=1)


def p_type_spec_2(t):
    """type_specifier : TYPE"""
    t[0] = TypeSpec(t[1], unsigned=0, base=1)


def p_type_spec_3(t):
    """type_specifier :  enum_spec 
    | struct_spec 
    | union_spec"""
    t[0] = TypeSpec(t[1], unsigned=0, base=0, compound=1)


def p_type_spec_4(t):
    """type_specifier : IDENT"""
    t[0] = TypeSpec(t[1], unsigned=0, base=0)


def p_type_spec_5(t):
    """type_specifier : UNSIGNED"""
    t[0] = TypeSpec("int", unsigned=1, base=1)


def p_enum(t):
    """enum_spec : ENUM enum_body"""
    t[0] = Enum(t[2])


def p_enum_body(t):
    """enum_body : LCBRACK enum_body_aux RCBRACK"""
    t[0] = t[2]


def p_enum_body_aux_1(t):
    """enum_body_aux : IDENT EQ value COMMA enum_body_aux"""
    t[0] = EnumList(EnumClause(t[1], t[3]), t[5])


def p_enum_body_aux_2(t):
    """enum_body_aux : IDENT EQ value"""
    t[0] = EnumList(EnumClause(t[1], t[3]))


def p_struct_spec(t):
    """struct_spec : STRUCT struct_body"""
    t[0] = Struct(t[2])


def p_struct_body(t):
    """struct_body : LCBRACK struct_body_aux RCBRACK"""
    t[0] = t[2]


def p_struct_body_aux_1(t):
    """struct_body_aux : declaration SEMICOLON struct_body_aux"""
    t[0] = StructList(t[1], t[3])


def p_struct_body_aux_2(t):
    """struct_body_aux : declaration SEMICOLON"""
    t[0] = StructList(t[1])


def p_union(t):
    """union_spec : UNION union_body"""
    t[0] = Union(t[2])


def p_union_body(t):
    """union_body : SWITCH LPAREN declaration RPAREN LCBRACK union_body_aux RCBRACK"""
    t[0] = UnionBody(t[3], t[6])


def p_union_body_aux_1(t):
    """union_body_aux : union_case"""
    t[0] = UnionList(t[1])


def p_union_body_aux_2(t):
    """union_body_aux : union_case union_body_aux"""
    t[0] = UnionList(t[1], t[2])


def p_union_case_1(t):
    """union_case : CASE value COLON declaration SEMICOLON"""
    t[0] = UnionElt(t[2], t[4])


def p_union_case_2(t):
    """union_case : DEFAULT COLON declaration SEMICOLON"""
    t[0] = UnionDefElt(t[3])


def p_constant_def(t):
    """constant_def : CONST IDENT EQ CONSTVAL SEMICOLON"""
    t[0] = Const(t[2], t[4])


def p_type_def_1(t):
    """type_def : TYPEDEF declaration SEMICOLON"""
    t[0] = TypeDef(t[2])


def p_type_def_2(t):
    """type_def : ENUM IDENT enum_body SEMICOLON  
    | STRUCT IDENT struct_body SEMICOLON 
    | UNION IDENT union_body SEMICOLON"""
    t[0] = TypeDefCompound(t[2], t[1], t[3])


def p_definition(t):
    """definition : type_def 
    | constant_def"""
    t[0] = t[1]


def p_program_def(t):
    """program_def : PROGRAM IDENT LCBRACK version_defs RCBRACK EQ CONSTVAL SEMICOLON"""
    t[0] = Program(t[2], t[4], t[7])


def p_version_defs_1(t):
    """version_defs : version_def version_defs"""
    t[0] = VersionList(t[1], t[2])


def p_version_defs_2(t):
    """version_defs : version_def"""
    t[0] = VersionList(t[1])


def p_version_def(t):
    """version_def : VERSION IDENT LCBRACK procedure_defs RCBRACK EQ CONSTVAL SEMICOLON"""
    t[0] = Version(t[2], t[4], t[7])


def p_procedure_defs_1(t):
    """procedure_defs : procedure_def procedure_defs"""
    t[0] = ProcedureList(t[1], t[2])


def p_procedure_defs_2(t):
    """procedure_defs : procedure_def"""
    t[0] = ProcedureList(t[1])


def p_procedure_def(t):
    """procedure_def : arg_type_specifier IDENT LPAREN type_spec_list RPAREN EQ CONSTVAL SEMICOLON"""
    t[0] = Procedure(t[2], t[1], t[4], t[7])


def p_type_spec_list_1(t):
    """type_spec_list : arg_type_specifier COMMA type_spec_list"""
    t[0] = TypeSpecList(t[1], t[3])


def p_type_spec_list_2(t):
    """type_spec_list : arg_type_specifier"""
    t[0] = TypeSpecList(t[1])


def p_arg_type_specifier_1(t):
    """arg_type_specifier : type_specifier
    | void"""
    # void isn't mentioned as a possibility in the RFC183[12] grammar,
    # but it happens in IDL files.  I should add semantics that
    # if void appears in an arglist, it must be the only elt. XXX
    t[0] = t[1]


def p_arg_type_specifier_2(t):
    """arg_type_specifier : type_specifier STAR"""
    # TODO: need some special-casing to treat this as "optional",
    # right now all cases get treated as linked lists anyway?
    t[0] = t[1]


def p_error(t):
    raise ParseError(t)


class NodeVisitor(abc.ABC):
    def __init__(self, ctx: Ctx):
        self.ctx = ctx
        self.node_stack = []

    @abc.abstractmethod
    def visit(self, node: Node):
        self.node_stack.append(node)

    def leave(self):
        self.node_stack.pop(-1)


class StructHoistingVisitor(NodeVisitor):
    def visit(self, node: Node):
        """Hoist struct declarations up and out of unions"""
        super().visit(node)
        if not isinstance(node, UnionElt):
            return
        typ_spec: TypeSpec = node.decl.typ
        if not typ_spec.compound:
            return
        root = self.node_stack[0]
        base_typedef = self.node_stack[-4]

        # XXX: How do we handle naming conflicts anyways? Can there be any?

        # Extract the struct def and create a new top-level node for it
        struct_val = typ_spec.val
        new_typ_spec = TypeDefCompound(struct_val.body.name, "struct", struct_val.body)

        # Have the union reference this instead
        typ_spec.base = False
        typ_spec.compound = False
        typ_spec.val = struct_val.body.name

        # Insert the struct just before the union
        root.children.insert(root.children.index(base_typedef), new_typ_spec)


def print_ast(ast, level=0):
    print(" " * 4 * level)
    if isinstance(ast, Node):
        print(ast.__class__.__name__)
        if ast.val is not None:
            print_ast(ast.val)
        if ast.children is not None:
            for c in ast.children:
                print_ast(c, level + 1)
    else:
        print(ast)


def compile(s, temp_directory):
    lexer = lex.lex(outputdir=temp_directory)
    parser = yacc.yacc(outputdir=temp_directory)
    ast = parser.parse(s)
    ctx = Ctx(os.environ.get("REMAP_NAMES") == "1")
    hoister = StructHoistingVisitor(ctx)
    ast.visit(hoister)

    header = "# Auto-generated from IDL file\n"
    src = """import abc
import dataclasses
import typing
from dataclasses import dataclass

from shenaniganfs import rpchelp

TRUE = True
FALSE = False
"""
    ctx.exec(src)
    tmp = ast.to_str(ctx)
    src += "\n".join((ctx.finish(), tmp))

    ctx.collect_types()

    s = StringIO()
    s.write(header)
    s.write(src)
    s.write("\n\n\n")
    s.write(ctx.finish_progs())
    s.write("\n\n")
    s.write(ctx.finish_exports())

    strbuf = s.getvalue().replace("\t", " " * 4)
    strbuf = re.sub(r"\n\n[\n]+", "\n\n\n", strbuf, flags=re.M | re.S)

    print(strbuf)


def main():
    testfn = compile
    #    testfn = testyacc
    #    testfn = testlex

    for fn in sys.argv[1:]:
        with open(fn) as f:
            s = f.read()
        with tempfile.TemporaryDirectory() as d:
            testfn(s, d)


if __name__ == '__main__':
    main()
