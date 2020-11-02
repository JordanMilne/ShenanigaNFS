"""
Reach out to rpcbind on the specified addr, asking for the mount
service's addr, then ask the mount service for all exported filesystems.
"""

import asyncio
import argparse
import pprint
import sys

from shenaniganfs.generated.rfc1813 import MOUNT_PROGRAM_3_CLIENT
import shenaniganfs.generated.rfc1833_rpcbind as rb
from shenaniganfs.rpchelp import rpcbind_to_addr
from shenaniganfs.server import TCPClient, SimpleRPCBindClient


class SimpleMountV3Client(TCPClient, MOUNT_PROGRAM_3_CLIENT):
    pass


async def main():
    parser = argparse.ArgumentParser(description="List NFS exports")
    parser.add_argument("host", nargs='?', default="127.0.0.1")
    parser.add_argument("port", nargs='?', default=111, type=int)
    parsed = parser.parse_args(sys.argv[1:])
    async with SimpleRPCBindClient(parsed.host, parsed.port) as rpc_client:
        resp = await rpc_client.GETADDR(rb.RPCB(
            r_prog=MOUNT_PROGRAM_3_CLIENT.prog,
            r_addr=b"",
            r_netid=b"tcp",
            r_owner=b"",
            r_vers=MOUNT_PROGRAM_3_CLIENT.vers,
        ))
        host, port = rpcbind_to_addr(resp.body)
        async with SimpleMountV3Client(host, port) as mount_client:
            pprint.pprint((await mount_client.EXPORT()).body)


if __name__ == "__main__":
    asyncio.run(main())
