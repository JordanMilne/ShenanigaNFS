import xdrlib as xdr

from pynefs.generated.rfc1831 import rpc_msg


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




