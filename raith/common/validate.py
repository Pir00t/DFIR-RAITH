# Author: Steven Folek | @Pir00t
# Version:  1.0

import os

def validate_path(path):
    """Validate if the given path is a file or directory."""
    if os.path.exists(path):
        if os.path.isfile(path):
            return 'file'
        elif os.path.isdir(path):
            return 'directory'
    return 'invalid'