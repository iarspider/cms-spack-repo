# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PythonTools(BundlePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/cms-sw/cmsdist"

    version('3.0')

    depends_on("root+python")
    depends_on("curl")
    depends_on("python")
    depends_on("xrootd")
    depends_on("llvm")
    depends_on("hdf5")
    depends_on("mxnet-predict")
    depends_on("yoda")
    depends_on("opencv")
    depends_on("professor")
    depends_on("rivet")
    depends_on("frontier-client")
    depends_on("py-onnx-runtime")
    depends_on("openldap")

    depends_on("py-anyio")
    depends_on("py-sniffio")
    depends_on("py-scipy")
    depends_on("py-keras")
    depends_on("py-theano")
    depends_on("py-scikit-learn")

    depends_on("py-tensorflow")
    depends_on("py-cmsml")
    depends_on("py-law")
    depends_on("py-protobuf")

    depends_on("py-tables")
    depends_on("py-numexpr")
    depends_on("py-histogrammar")
    depends_on("py-pandas")
    depends_on("py-bottleneck")
    depends_on("py-downhill")
    depends_on("py-xgboost")
    depends_on("py-llvmlite")
    depends_on("py-numba")
    depends_on("py-hep-ml")
    depends_on("py-uncertainties")
    depends_on("py-seaborn")
    depends_on("py-h5py")
    depends_on("py-uproot")
    depends_on("py-vector")
    depends_on("py-opt-einsum")
    depends_on("py-joblib")

    depends_on("py-xrootdpyfs")

    depends_on("py-entrypoints")
    depends_on("py-psutil")
    depends_on("py-repoze-lru")
    depends_on("py-pygments")
    depends_on("py-appdirs")
    depends_on("py-argparse")
    depends_on("py-bleach")
    depends_on("py-certifi")
    depends_on("py-decorator")
    depends_on("py-html5lib")
    depends_on("py-ipykernel")
    depends_on("py-ipython")
    depends_on("py-ipython-genutils")
    depends_on("py-ipywidgets")
    depends_on("py-jsonschema")
    depends_on("py-jupyter-client")
    depends_on("py-jupyter-console")
    depends_on("py-jupyter-core")
    depends_on("py-mistune")
    depends_on("py-nbconvert")
    depends_on("py-nbformat")
    depends_on("py-notebook")
    depends_on("py-packaging")
    depends_on("py-pandocfilters")
    depends_on("py-pathlib2")
    depends_on("py-pexpect")
    depends_on("py-pickleshare")
    depends_on("py-prompt-toolkit")
    depends_on("py-ptyprocess")
    depends_on("py-pyparsing")
    depends_on("py-pyzmq")
    depends_on("py-scandir")
    depends_on("py-setuptools")
    depends_on("py-simplegeneric")
    depends_on("py-singledispatch")
    depends_on("py-six")
    depends_on("py-terminado")
    depends_on("py-testpath")
    depends_on("py-tornado")
    depends_on("py-traitlets")
    depends_on("py-webencodings")
    depends_on("py-widgetsnbextension")
    depends_on("py-cycler")
    depends_on("py-docopt")
    depends_on("py-networkx")
    depends_on("py-prettytable")
    depends_on("py-pycurl")
    depends_on("py-pytz")
    depends_on("py-requests")
    depends_on("py-schema")
    depends_on("py-python-dateutil")
    depends_on("py-mock")
    depends_on("py-pbr")
    depends_on("py-mpmath")
    depends_on("py-sympy")
    depends_on("py-tqdm")
    depends_on("py-funcsigs")
    depends_on("py-pkgconfig")
    depends_on("py-click")
    depends_on("py-jsonpickle")
    depends_on("py-prwlock")
    depends_on("py-virtualenv")
    depends_on("py-virtualenvwrapper")
    depends_on("py-urllib3")
    depends_on("py-chardet")
    depends_on("py-idna")
    depends_on("py-werkzeug")
    depends_on("py-pytest")
    depends_on("py-avro")
    depends_on("py-fs")
    depends_on("py-lizard")
    depends_on("py-flawfinder")
    depends_on("py-python-ldap")
    depends_on("py-plac")

    depends_on("py-matplotlib")
    depends_on("py-numpy")
    depends_on("py-sqlalchemy")
    depends_on("py-pygithub")
    # TODO depends_on("py-dxr")
    depends_on("py-pyyaml")
    depends_on("py-pylint")
    depends_on("py-pip")
    depends_on("py-cx-oracle")
    depends_on("py-cython")
    depends_on("py-pybind11")
    depends_on("py-histbook")
    depends_on("py-flake8")
    depends_on("py-autopep8")
    depends_on("py-pycodestyle")
    depends_on("py-lz4")
    depends_on("py-ply")
    depends_on("py-py")
    depends_on("py-defusedxml")
    depends_on("py-atomicwrites")
    depends_on("py-attrs")
    depends_on("py-onnx")
    depends_on("py-onnxmltools")
    depends_on("py-colorama")
    depends_on("py-lxml")
    depends_on("py-beautifulsoup4")
    depends_on("py-gitpython")
    depends_on("py-send2trash")
    depends_on("py-ipaddress")
    depends_on("py-mccabe")
    depends_on("py-more-itertools")
    depends_on("py-pluggy")
    depends_on("py-pyasn1-modules")
    depends_on("py-pyasn1")
    depends_on("py-pyflakes")
    depends_on("py-stevedore")
    depends_on("py-typing-extensions")
    depends_on("py-virtualenv-clone")
    depends_on("py-asn1crypto")
    depends_on("py-backcall")
    depends_on("py-cffi")
    depends_on("py-jedi")
    depends_on("py-parso")
    depends_on("py-pycparser")
    depends_on("py-absl-py")
    depends_on("py-gast")
    depends_on("py-grpcio")
    depends_on("py-grpcio-tools")
    depends_on("py-markdown")
    depends_on("py-subprocess32")
    depends_on("py-kiwisolver")
    depends_on("py-pillow")
    depends_on("py-pydot")

    depends_on("py-astroid")
    depends_on("py-hepdata-lib")
    depends_on("py-isort")
    depends_on("py-lazy-object-proxy")
    depends_on("py-pytest-cov")
    depends_on("py-wrapt")

    depends_on("py-distlib")
    depends_on("py-filelock")
    depends_on("py-gitdb")
    depends_on("py-importlib-resources")
    depends_on("py-smmap")
    depends_on("py-zipp")

    depends_on("py-pycuda")

    depends_on("py-boost-histogram")
    depends_on("py-hist")
    depends_on("py-histoprint")
    depends_on("py-mplhep")
    depends_on("py-correctionlib")