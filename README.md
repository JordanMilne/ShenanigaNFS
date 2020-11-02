# ShenanigaNFS

Python library for making somewhat conformant-ish low-level NFSv2/3 clients and servers.
Includes tools for making NFS servers with mount-specific FS state and a 
VFS API similar to FUSE for making custom filesystems.

Primarily meant for use-cases where a real FUSE filesystem shared over NFS
wouldn't be appropriate, such as when each client _must_ receive a distinct
filesystem. Authentication is intentionally unsupported as are file locking and
transport encryption.

## Features

* SunRPC IDL -> Client / Server stub generator (outputs type hints too!)
* RPCBind / PortMapper server implementation
* * Optional, can register services with system RPCbind if preferred
* Basic NFSv2 and NFSv3 implementations
* `asyncio`-based networking, TCP-only for the moment
* Example filesystems (SimpleFS, ZipFS)

## Is this appropriate for production use?
No.

I needed the ability to expose an unauthenticated, world-writable filesystem
to the public internet, and each mounter needed to have their writes only 
accessible to themselves, and it needed to be somewhat hardened against DoS.
If you just need a user mode NFS server, I recommend NFS Ganesha.

Otherwise, the tools are low-level enough to be useful for reverse engineering
and creating intentionally misbehaved filesystems.

## Running RPCBind as non-root
See <https://stackoverflow.com/a/414258> for how to allow your script to bind 
to low ports. In short:

> `sudo setcap 'cap_net_bind_service=+ep' /path/to/python`

## Acknowledgements

* [PineFS](https://www.panix.com/~asl2/software/Pinefs/) - Used as the basis for the 
  XDR and IDL parsing code
* [go-nfs](https://github.com/willscott/go-nfs) - Unrelated, but seems like we started writing 
  them at the same time. Also it looks nice and is probably more stable, give it a look.