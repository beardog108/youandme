import stem.process


def launch_tor(control_port="1338", socks_port="1339"):
    control_port = str(control_port)
    socks_port = str(socks_port)
    stem.process.launch_tor_with_config(
    config = {
        'ControlPort':  control_port,
        'SocksPort': socks_port,
        'Log': [
        'NOTICE stdout'
        ],
    }, take_ownership=True)
