import itertools
import functools
import operator
import os
import re
import stat

from llnl.util.filesystem import join_path, force_remove


chmod_regex = re.compile(r"(?P<who>[uoga]?)(?P<op>[+\-=])(?P<value>[ugo]|[rwx]*)")
stat_bit_prefix = dict(u="USR", g="GRP", o="OTH")


def chmod(entry, perms, recursive=False):
    """Implement the bash chown function
    Arguments:
        entry (str): path to change
        perms (str or int): permissions. Can be either a number,
            or a symbolic description
        recursive (bool): if chmod should be performed recursively
    The format of description is
        * an optional letter in o, g, u, a (no letter means a)
        * an operator in +, -, =
        * a sequence of letters in r, w, x, or a single letter in o, g, u
    Notice: [+-]X is not supported
    """
    if entry.rstrip('/').endswith('.spack'):
        # Should be fine already
        continue

    if not os.path.isdir(entry):
        recursive = False

    chmod_f = _chmod_one_s if isinstance(perms, str) else _chmod_one_o

    chmod_f(entry, perms)
    if recursive:
        for root, dirs, files in os.walk(entry):
            for entry in itertools.chain(dirs, files):
                chmod_f(join_path(root, entry), perms)


def _chmod_one_o(entry, perms):
    try:
        os.chmod(entry, perms)
    except PermissionError:
        pass


def _chmod_one_s(entry, perms):
    # Adapted from here: https://www.daniweb.com/programming/software-development/code/243659/change-file-permissions-symbolically-linux
    def stat_bit(who, letter):
        if who == "a":
            return stat_bit("o", letter) | stat_bit("g", letter) | stat_bit("u", letter)
        return getattr(stat, "S_I%s%s" % (letter.upper(), stat_bit_prefix[who]))

    def ors(sequence, initial=0):
        return functools.reduce(operator.__or__, sequence, initial)

    mo = chmod_regex.match(perms)
    who, op, value = mo.group("who"), mo.group("op"), mo.group("value")
    if not who:
        who = "a"
    mode = os.stat(entry)[stat.ST_MODE]
    if value in ("o", "g", "u"):
        mask = ors((stat_bit(who, z) for z in "rwx" if (mode & stat_bit(value, z))))
    else:
        mask = ors((stat_bit(who, z) for z in value))
    if op == "=":
        mode &= ~ ors((stat_bit(who, z) for z in "rwx"))
    mode = (mode & ~mask) if (op == "-") else (mode | mask)
    try:
        os.chmod(entry, perms)
    except PermissionError:
        pass


def post_install(spec): 
    prefix = spec.prefix
    chmod(str(prefix), 'o+r', True)
    if os.path.exists(prefix.bin):
        chmod(str(prefix.bin), 'a+x', True)
