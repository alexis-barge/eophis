# package import
from .cpl import *
from .namelists import *
from .namcouple import *

# eophis modules
from ..utils import logs, params
# external modules
import os
import shutil

"""
Coupling initialization
-----------------------
- Inquire namcouple file
- Copy namcouple file from Eophis reference if not
- Rename namcouple file to work with in peace (avoid other programs to start a coupling before namcouple automatic writing)
- instantiate Namcouple object
"""
def _init_coupling():
    logs.info('---------------------------')
    logs.info('  Coupling Initialization  ')
    logs.info('---------------------------')
    logs.info('  Looking for OASIS namelist "namcouple"')
    
    cpl_nml = os.path.join(os.getcwd(), "namcouple")
    cpl_nml_ref = os.path.join(os.getcwd(), "namcouple_ref")
    cpl_nml_base = os.path.join(os.path.abspath(cpl.__file__)[:-23], "namcouple_base")
    
    if params.RANK == 0:
        if not os.path.isfile(cpl_nml):
            shutil.copy(cpl_nml_base, cpl_nml_ref)
            logs.info(f'  "namcouple" not found, create one from {cpl_nml_base} \n')
        else:
            shutil.copy(cpl_nml, cpl_nml_ref)
            logs.info(f'  "namcouple" found, save copy as {cpl_nml_ref}\n')

    # Instantiate OASIS namcouple
    init_namcouple(cpl_nml_ref,cpl_nml)
