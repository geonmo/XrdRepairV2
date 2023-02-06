#!/bin/bash
WORKSPACE=$(pwd)
cd /tmp
apptainer build --force $WORKSPACE/devspace.sif $WORKSPACE/build_xrdrepair_v2.def
cd -
