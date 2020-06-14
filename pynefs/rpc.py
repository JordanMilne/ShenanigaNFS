import xdrlib as xdr

RPCVERSION = 2

CALL = 0
REPLY = 1

AUTH_NULL = 0
AUTH_UNIX = 1
AUTH_SHORT = 2
AUTH_DES = 3

MSG_ACCEPTED = 0
MSG_DENIED = 1

SUCCESS = 0  # RPC executed successfully
PROG_UNAVAIL = 1  # remote hasn't exported program
PROG_MISMATCH = 2  # remote can't support version #
PROC_UNAVAIL = 3  # program can't support procedure
GARBAGE_ARGS = 4  # procedure can't decode params
SYSTEM_ERR = 5

RPC_MISMATCH = 0  # RPC version number != 2
AUTH_ERROR = 1  # remote can't authenticate caller

AUTH_BADCRED = 1  # bad credentials (seal broken)
AUTH_REJECTEDCRED = 2  # client must begin new session
AUTH_BADVERF = 3  # bad verifier (seal broken)
AUTH_REJECTEDVERF = 4  # verifier expired or replayed
AUTH_TOOWEAK = 5  # rejected for security reasons
AUTH_FAILED = 7  # reason unknown


class Packer(xdr.Packer):

    def pack_auth(self, auth):
        flavor, stuff = auth
        self.pack_enum(flavor)
        self.pack_opaque(stuff)

    def pack_auth_unix(self, stamp, machinename, uid, gid, gids):
        self.pack_uint(stamp)
        self.pack_string(machinename)
        self.pack_uint(uid)
        self.pack_uint(gid)
        self.pack_uint(len(gids))
        for i in gids:
            self.pack_uint(i)

    def pack_callheader(self, xid, prog, vers, proc, cred, verf):
        self.pack_uint(xid)
        self.pack_enum(CALL)
        self.pack_uint(RPCVERSION)
        self.pack_uint(prog)
        self.pack_uint(vers)
        self.pack_uint(proc)
        self.pack_auth(cred)
        self.pack_auth(verf)

    # Caller must add procedure-specific part of call

    def pack_replyheader(self, xid, verf):
        self.pack_uint(xid)
        self.pack_enum(REPLY)
        self.pack_uint(MSG_ACCEPTED)
        self.pack_auth(verf)
        self.pack_enum(SUCCESS)
    # Caller must add procedure-specific part of reply


# Exceptions
class BadRPCFormat(Exception):
    pass


class BadRPCVersion(Exception):
    pass


class GarbageArgs(Exception):
    pass


class Unpacker(xdr.Unpacker):

    def unpack_auth(self):
        flavor = self.unpack_enum()
        stuff = self.unpack_opaque()
        return flavor, stuff

    def unpack_fragheader(self):
        return self.unpack_uint()

    def unpack_callheader(self):
        xid = self.unpack_uint()
        temp = self.unpack_enum()
        if temp != CALL:
            raise BadRPCFormat('no CALL but ' + temp)
        temp = self.unpack_uint()
        if temp != RPCVERSION:
            raise BadRPCVersion('bad RPC version ' + temp)
        prog = self.unpack_uint()
        vers = self.unpack_uint()
        proc = self.unpack_uint()
        cred = self.unpack_auth()
        verf = self.unpack_auth()
        return xid, prog, vers, proc, cred, verf

    # Caller must add procedure-specific part of call

    def unpack_replyheader(self):
        xid = self.unpack_uint()
        mtype = self.unpack_enum()
        if mtype != REPLY:
            raise RuntimeError(f'no REPLY but {mtype}')
        stat = self.unpack_enum()
        if stat == MSG_DENIED:
            stat = self.unpack_enum()
            if stat == RPC_MISMATCH:
                low = self.unpack_uint()
                high = self.unpack_uint()
                raise RuntimeError(f'MSG_DENIED: RPC_MISMATCH: {low}, {high}')
            if stat == AUTH_ERROR:
                stat = self.unpack_uint()
                raise RuntimeError(f'MSG_DENIED: AUTH_ERROR: {stat}')
            raise RuntimeError(f'MSG_DENIED: {stat}')
        elif stat != MSG_ACCEPTED:
            raise RuntimeError(f'Neither MSG_DENIED nor MSG_ACCEPTED: {stat}')
        verf = self.unpack_auth()
        stat = self.unpack_enum()
        if stat == PROG_UNAVAIL:
            raise RuntimeError('call failed: PROG_UNAVAIL')
        if stat == PROG_MISMATCH:
            low = self.unpack_uint()
            high = self.unpack_uint()
            raise RuntimeError(f'call failed: PROG_MISMATCH: {low} {high}')
        if stat == PROC_UNAVAIL:
            raise RuntimeError('call failed: PROC_UNAVAIL')
        if stat == GARBAGE_ARGS:
            raise RuntimeError('call failed: GARBAGE_ARGS')
        if stat != SUCCESS:
            raise RuntimeError(f'call failed: {stat}')
        return xid, verf
        # Caller must get procedure-specific part of reply

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__buf[self.__pos:]!r}>"

