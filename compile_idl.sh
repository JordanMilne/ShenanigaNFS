#!/bin/bash

pushd `dirname $(readlink -f $0)` > /dev/null

function compile_idl {
  REMAP_NAMES=1 python -m shenaniganfs.tools.rpcgen "shenaniganfs/idl/${1}.x" > "shenaniganfs/generated/${1}.py"
}


compile_idl rfc1094
compile_idl rfc1813
compile_idl rfc1831
compile_idl rfc1833_portmapper
compile_idl rfc1833_rpcbind
compile_idl statd

echo "Done"
