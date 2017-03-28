import platform


def is_linux():
    return get_os_type().startswith('linux')


def is_windows():
    return get_os_type().startswith('windows')


def get_os_type():
    """
    returns 'windows' or 'linux' depending which os you're running.
    """
    return platform.system().lower()
