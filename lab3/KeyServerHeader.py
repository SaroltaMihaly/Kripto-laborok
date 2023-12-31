from typing import Type, Tuple

SERVER_PORT = 3005
SERVER_HOST = 'localhost'
MESSAGE_SIZE = 1024

PublicKeyType = Tuple[int, ...]
RegisterType = Tuple[int, PublicKeyType]

GOOD = 'GOOD'
END_CONN = 'END_CONN'

INVALID = 'Error: Invalid request'

# PUBLIC_KEY:port
# REGISTER:(port, public_key)



