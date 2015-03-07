"""
pyMultihash is a python implementation of the Multihash standard: https://github.com/jbenet/multihash

"""

import hashlib
import base58


"""
These first two methods are kinda inefficient, but python is not really designed to mess with bytes
"""
def int_to_byte_array(big_int):
    array = []
    while big_int > 1:
        array.append(big_int%256)
        big_int/=256
    print array
    print len(array)
    return array

def bytes_to_long(bytes):
    return int( ''.join('{:02x}'.format(x) for x in bytes), 16)


"""
    the main event!
"""
def parseHash(hashstr):
    hashint = base58.decode(hashstr)
    hashbytes = int_to_byte_array(hashint)
    if len(hashbytes) < 3:
        raise Exception("Multihash must be at least 3 bytes")
    hash_func_id = hashbytes[0]
    hash_length = hashbytes[1]
    hash_contents = hashbytes[2:hash_length+2]

    return bytes_to_long(hash_contents)

def genHash(bytes,func_id):
    hashfunc = None
    if func_id == 0x11:
        #function is sha1
        hashfunc = hashlib.sha1()
    elif func_id == 0x12:
        #function is sha256
        hashfunc = hashlib.sha256()
    elif func_id == 0x13:
        #function is sha512
        hashfunc = hashlib.sha512()
    else:
        raise Exception("Requested hash is not supported")
    hashfunc.update(bytes)
    data = hashfunc.digest()
    size = hashfunc.digest_size
    bytes = [func_id,size]+[ord(x) for x in data]
    return base58.encode(bytes_to_long(bytes))

print genHash("foo",0x12)
