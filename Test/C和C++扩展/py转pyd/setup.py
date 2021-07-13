from distutils.core import setup, Extension

from Cython.Distutils import build_ext

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("pydmod", sources=["pydmod.py"])]
)
