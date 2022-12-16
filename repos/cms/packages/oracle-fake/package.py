from spack import *


class OracleFake(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/cms-externals/oracle-fake/archive/6da7ab5b4643b54f57002f9c96c426355a960eb1.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('6da7ab5b4643b54f57002f9c96c426355a960eb1', sha256='8a69c6b49a0db80c86451d389aa824c2f503aa58f74956c67d7298d20e1882cb')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')
