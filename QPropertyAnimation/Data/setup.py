# from distutils.core import setup, Extension
# 
# from Cython.Distutils import build_ext
# 
# 
# setup(
#     cmdclass={'build_ext': build_ext},
#     ext_modules=[Extension("pointtool", sources=[
#                            "pointtool.pyx"], language="c")]
# )

from distutils.core import setup

from Cython.Build import cythonize

setup(
    ext_modules=cythonize("pointtool.pyx"),
)
