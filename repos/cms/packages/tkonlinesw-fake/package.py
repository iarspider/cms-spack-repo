from spack import *


class TkonlineswFake(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/cms-externals/tkonlinesw-fake/archive/97afe74471b299148ac9ccdea21e9cda961ec885.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('97afe74471b299148ac9ccdea21e9cda961ec885', sha256='344f28ce7b6a8b3e1320cb7f6142de0f7410483b054dbf016dbbfffc0c2c1521')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')
