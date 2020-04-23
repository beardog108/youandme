import stem.process


def launch_tor(control_port="1336", socks_port="1337", data_dir=""):
    control_port = str(control_port)
    socks_port = str(socks_port)
    config = {
        'ControlPort':  control_port,
        'SocksPort': socks_port,
        'Log': [
        'NOTICE stdout'
        ],
    }
    if data_dir:
        config['DataDirectory'] = data_dir
    stem.process.launch_tor_with_config(
    config = config, take_ownership=True)
