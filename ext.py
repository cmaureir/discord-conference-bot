import tomli


def get_config_data():
    data = None
    with open("config.toml", "rb") as f:
        data = tomli.load(f)['main']
    return data
