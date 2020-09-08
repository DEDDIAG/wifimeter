from getpass import getpass

import click
import logging
from .network.threads import UDPSendThread, UDPRecvThread, wait
from .network.udp import UdpSocket
from .util.coder import encode
from .util.model import MeasurementRequest, RelayStateRequest, SysInfoRequest
from .util.output import measurement_output_parser
from .util.setup import tcp_setup
import timeout_decorator


@click.group()
def cli():
    pass


@cli.command()
@click.option('--ip', type=str)
@click.option('--poll', is_flag=True, help="Poll every second")
def info(ip, poll):
    """Ask device for get_sysinfo. If no IP is provided, request is send as broadcast"""

    message_str = SysInfoRequest().to_json()
    udp = UdpSocket()
    if ip is not None:
        udp.send(encode(message_str), ip)
    else:
        udp.send(encode(message_str))
    r = UDPRecvThread(udp)
    s = UDPSendThread(message_str, udp)
    if poll:
        s.start()
        r.start()
        wait((s, r))
    else:
        s.send()
        r.recv()


@cli.command()
@click.option('--state', prompt='State (0=OFF / 1=ON )', type=click.Choice(['0', '1']))
@click.option('--ip', type=str)
def switch(state, ip):
    """
    Switch device ON/OFF
    """
    message_str = RelayStateRequest(int(state)).to_json()

    udp = UdpSocket()
    if ip is not None:
        udp.send(encode(message_str), ip)
    else:
        udp.send(encode(message_str))


@cli.command()
def measure():
    """
    Receives readings every second
    """
    print("alias, timestamp, current, total, power, voltage, err_code")
    message_str = MeasurementRequest(None).to_json()
    socket_object = UdpSocket()
    s = UDPSendThread(message_str, socket_object)
    r = UDPRecvThread(socket_object, measurement_output_parser)
    s.start()
    r.start()

    wait((s, r))


@cli.command()
@click.option('-a', '--alias')
@click.option('-n', '--wlan-name')
@click.option('-p', '--password')
@click.option('-t', '--wlan-type', type=click.Choice(['0', '1', '2', '3']), help='0 = without any security, 2 = WEP, 3 = WPA')
@click.option('-l', '--log-level', default='DEBUG')
@timeout_decorator.timeout(35)
def setup(wlan_type, wlan_name, alias, password, log_level):
    """
    Setup device (alias, WLAN)
    """
    if alias is None:
        alias = click.prompt('Alias')
    if wlan_name is None:
        wlan_name = click.prompt("Wlan_name")
    if wlan_type is None:
        wlan_type = click.prompt("Wlan-type", type=click.Choice(['0', '1', '2', '3']))
    if wlan_type != '0' and password is None:
        password = getpass()
    setup_logging(log_level)
    wlan_type = int(wlan_type)
    tcp_setup(wlan_type, wlan_name, alias, password)


def setup_logging(log_level):
    """
    Set logging level
    :param log_level: possible choices 'DEBUG', 'WARNING', 'INFO'...
    """
    ext_logger = logging.getLogger("py.warnings")
    logging.captureWarnings(True)
    level = getattr(logging, log_level)
    logging.basicConfig(format="[%(asctime)s] %(levelname)s %(filename)s: %(message)s", level=level)
    if level <= logging.DEBUG:
        ext_logger.setLevel(logging.WARNING)
