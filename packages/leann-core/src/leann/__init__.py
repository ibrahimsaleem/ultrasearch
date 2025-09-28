# Fix OpenMP threading issues on macOS ARM64
import os
if os.uname().machine == 'arm64' and os.uname().sysname == 'Darwin':
    os.environ['OMP_NUM_THREADS'] = '1'

from .api import LeannBuilder, LeannChat, LeannSearcher

__all__ = ['LeannBuilder', 'LeannChat', 'LeannSearcher']