#!/bin/bash

pushd `dirname $(readlink -f $0)` > /dev/null

function compile_idl {
  python rpcgen.py "pynefs/idl/${1}.x" > "pynefs/generated/${1}.py"
}


compile_idl rfc1094
compile_idl rfc1813
compile_idl rfc1831
compile_idl rfc1833_portmapper
compile_idl rfc1833_rpcbind

echo "Done"