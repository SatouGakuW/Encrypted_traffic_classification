from pathlib import Path

from scapy.layers.dns import DNS
from scapy.layers.inet import TCP
from scapy.packet import Padding
from scapy.utils import PcapReader

# for app identification
PREFIX_TO_APP_ID = {
    # AIM chat
    'vpn_aim_chat1a': 0,
    'vpn_aim_chat1b': 0,
    # Email
    'vpn_email2a': 1,
    'vpn_email2b': 1,
    # Facebook
    'vpn_facebook_audio2': 2,
    # FTPS
    'vpn_ftps_a': 3,
    # Hangouts
    'vpn_hangouts_audio1': 4,
    # ICQ
    'vpn_icq_chat1a': 5,
    'vpn_icq_chat1b': 5,
    # SFTP
    'vpn_sftp_a': 6,
    # Skype
    'vpn_skype_audio1': 7,
    'vpn_skype_chat1a': 7,
    'vpn_skype_chat1b': 7,
    'vpn_skype_files1a': 7,
    'vpn_skype_files1b': 7,
    # Spotify
    'vpn_spotify_a': 8,
    # Tor
    'tortwitter': 9,
    'torvimeo1': 9,
    'toryoutube1': 9,
    'toryoutube2': 9,
    # Voipbuster
    'vpn_voipbuster1b': 10,
    'vpn_voipbuster1a': 10,
    # Vimeo
    'vpn_vimeo_a': 11,
}

ID_TO_APP = {
    0: 'AIM Chat',
    1: 'Email',
    2: 'Facebook',
    3: 'FTPS',
    4: 'Hangouts',
    5: 'ICQ',
    6: 'SFTP',
    7: 'Skype',
    8: 'Spotify',
    9: 'Tor',
    10: 'Voipbuster',
    11: 'Vimeo',
}

# for traffic identification
PREFIX_TO_TRAFFIC_ID = {
    # VPN: Chat 0
    'vpn_aim_chat1a': 0,
    'vpn_aim_chat1b': 0,
    'vpn_icq_chat1a': 0,
    'vpn_icq_chat1b': 0,
    'vpn_skype_chat1a': 0,
    'vpn_skype_chat1b': 0,
    # VPN: File Transfer 1
    'vpn_sftp_a': 1,
    'vpn_ftps_a': 1,
    'vpn_skype_files1a': 1,
    'vpn_skype_files1b': 1,
    # VPN: Email 2
    'vpn_email2a': 2,
    'vpn_email2b': 2,
    # VPN: VoIP 3
    'vpn_hangouts_audio1': 3,
    'vpn_skype_audio1': 3,
    'vpn_voipbuster1a': 3,
    'vpn_voipbuster1b': 3,
    'vpn_facebook_audio2': 3,
    # VPN: Streaming 4
    'vpn_spotify_a': 4,
    'vpn_vimeo_a': 4,
    # Streaming 5
    'toryoutube1': 5,
    'toryoutube2': 5,
    'torvimeo1': 5,
}

ID_TO_TRAFFIC = {
    0: 'VPN: Chat',
    1: 'VPN: File Transfer',
    2: 'VPN: Email',
    3: 'VPN: VoIP',
    4: 'VPN: Streaming',
    5: 'Streaming',
}


def read_pcap(path: Path):
    packets = PcapReader(str(path))

    return packets


def should_omit_packet(packet):
    # SYN, ACK or FIN flags set to 1 and no payload
    if TCP in packet and (packet.flags & 0x13):
        # not payload or contains only padding
        layers = packet[TCP].payload.layers()
        if not layers or (Padding in layers and len(layers) == 1):
            return True

    # DNS segment
    if DNS in packet:
        return True

    return False
