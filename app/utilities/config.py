import os

from yamlsettings import YamlSettings

_config = None

project_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '..', '..'
    ))


def retrieve_config():
    defaults_yml = "{}/defaults.yml".format(project_path)
    settings_yml = "{}/settings.yml".format(project_path)

    rv = YamlSettings(
        defaults_yml,
        settings_yml
    ).get_settings('app')
    return rv


def get_config(force=False):
    """Load the configuration settings."""
    global _config
    if _config is not None and not force:
        return _config

    _config = retrieve_config()
    return _config
