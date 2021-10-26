import os
import numpy as np
import base64
import sys
import ctypes

def convert_and_save(b64_string):
    buffsize=len(b64_string)+1
    offset = sys.getsizeof(b64_string) - buffsize
    try:
        b64decoded = base64.b64decode(b64_string)
        
        decompressed = b64decoded #zlib.decompress(b64decoded)
    except Exception as e:
        decompressed = b64_string.encoded()
        
    #ctypes.memset(id(b64_string), offset, 0, buffsize)
    nparr = np.frombuffer(decompressed, np.uint8)
    return nparr
