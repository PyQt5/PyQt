from distutils.core import setup, Extension

module = Extension('pydext', sources=['pydext.c'])

setup(name='pydext',
      version='1.0.0',
      description='This is pydext',
      ext_modules=[module])
