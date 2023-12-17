from ..KeyServer import KeyServer
from ..KeyServerHeader import *


def test_register_client():
    """
    Test registering a client: A register request is sent to the key server,
    and the key server responds with a PublicKey type.
    """
    key_server = KeyServer()

    port = 12345
    public_key: PublicKeyType = (456, 12, 356)
    register_request: RegisterType = (port, public_key)
    key_server.register_client(register_request)
    assert key_server.get_public_key(port) == public_key


def test_non_existing_client():
    """
    Test getting the public key of a non-existing client
    """
    key_server = KeyServer()

    port = 12345
    assert key_server.get_public_key(port) is None


def test_update_client():
    """
    Test updating a client: A register request is sent to the key server,
    and the key server responds with a PublicKey type.
    """
    key_server = KeyServer()

    port = 12345
    public_key: PublicKeyType = (456, 12, 356)
    register_request: RegisterType = (port, public_key)
    key_server.register_client(register_request)
    assert key_server.get_public_key(port) == public_key

    # Change the public key
    new_public_key: PublicKeyType = (123, 456, 789)
    register_request: RegisterType = (port, new_public_key)
    key_server.register_client(register_request)
    assert key_server.get_public_key(port) == new_public_key
