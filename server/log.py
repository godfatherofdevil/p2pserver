import sys


def logger(s, *args):
    """
    simple stderr logger: not thread safe
    :param s:
    :param args:
    :return:
    """
    sys.stdout.flush()
    s += '\n'
    if args:
        sys.stderr.write(s % args)
    else:
        sys.stderr.write(s)
    sys.stderr.flush()
