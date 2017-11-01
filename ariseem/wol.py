"""
    ariseem
    ~~~~~~~

    Minimalistic REST API for wake-on-lan

    :copyright: (c) 2017 by Timo Furrer <tuxtimo@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

import socket
import struct

#: Holds the WOL broadcast address
BROADCAST_ADDRESS = 'FFFFFFFFFFFF'


def wake_on_lan(mac):
    """
    Wake-On-LAN the given MAC address

    The MAC address has to be in one of the following formats:
        - AA:BB:CC:DD:EE:FF
        - AABBCCDDEEFF
    """
    if 12 != len(mac) and len(mac) != 12 + 5:
        raise AttributeError(f'The MAC address has to be either 12 or 17 chars long')

    if len(mac) == 12 + 5:
        mac = mac.replace(mac[2], '')

    raw_payload = BROADCAST_ADDRESS + 16 * mac

    # convert raw_payload byte-wise
    payload = b''.join([struct.pack('!B', int(raw_payload[i] + raw_payload[i + 1], 16))
                        for i in range(0, len(raw_payload), 2)])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(payload, ('<broadcast>', 7))
    sock.close()
