#!/bin/bash
apptainer run -B /etc/grid-security/certificates devspace.sif $*
