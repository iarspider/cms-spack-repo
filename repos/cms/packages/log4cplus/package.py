from spack import *
from spack.pkg.builtin.log4cplus import Log4cplus as BuiltinLog4cplus


class Log4cplus(BuiltinLog4cplus):
    __doc__ = BuiltinLog4cplus.__doc__

    keep_archives = True

    def cmake_args(self):
        args = super().cmake_args()
        args.extend(
            [
                "-DBUILD_SHARED_LIBS:BOOL=OFF",
                "-DLOG4CPLUS_BUILD_TESTING=OFF",
                "-DLOG4CPLUS_BUILD_LOGGINGSERVER=OFF",
            ]
        )

        return args
