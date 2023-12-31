"""
coupling subpackage
-------------------
OASIS is a Fortran coupling library that performs field exchanges between two coupled executables.
Last release provided C and Python APIs, which enables coupling between non-homogeneously written codes.

This subpackage is built on this librabry and provides:
    1. an OASIS interface wrapper to exchange data with Earth-System
    2. tools to create and manipulate OASIS and Fortran namelists
"""
# package export
from .tunnel import *
from .namelist import *
from .namcouple import *

# eophis modules
from ..utils import logs, paral
# external modules
import os
import shutil

def _init_coupling():
    """
    Run the coupling subpackage initialization:
        - Inquire coupling namelists 'namcouple' and 'namcouple_ref'
        - Create 'namcouple' from 'namcouple_ref' if exists, from Eophis otherwise
        - Save copy of 'namcouple' as 'namcouple_ref' if exists alone
        - If both exist, does nothing
        - instantiate Namcouple singleton with 'namcouple'
    """
    logs.info('---------------------------')
    logs.info('  Coupling Initialization  ')
    logs.info('---------------------------')
    logs.info('  Checking up OASIS namelists...')
    
    cpl_nml = os.path.join(os.getcwd(), 'namcouple')
    cpl_nml_ref = os.path.join(os.getcwd(), 'namcouple_ref')
    cpl_nml_base = os.path.join(os.path.abspath(tunnel.__file__)[:-26], 'namcouple_eophis')
    
    if not os.path.isfile(cpl_nml):
        logs.info(f'    "namcouple" not found, looking for reference file "namcouple_ref"')
        if not os.path.isfile(cpl_nml_ref):
            logs.info(f'    "namcouple_ref" not found either, creating it from {cpl_nml_base} \n')
            shutil.copy(cpl_nml_base, cpl_nml_ref) if paral.RANK == 0 else None
        else:
            logs.info(f'    "namcouple_ref" found, copied as "namcouple"\n')
            shutil.copy(cpl_nml_ref,cpl_nml) if paral.RANK == 0 else None
    else:
        if not os.path.isfile(cpl_nml_ref):
            logs.info(f'  only "namcouple" found, save copy as {cpl_nml_ref}\n')
            shutil.copy(cpl_nml, cpl_nml_ref) if paral.RANK == 0 else None
        else:
            logs.info(f'  "namcouple" and "namcouple_ref" found, nothing done\n')
            logs.warning(f'Priority given to "namcouple" for reading if "namcouple_ref" is also present')
            cpl_nml_ref = cpl_nml

    # Instantiate OASIS namcouple
    init_namcouple(cpl_nml_ref,cpl_nml)
