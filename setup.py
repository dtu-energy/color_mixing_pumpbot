from setuptools import setup, find_packages

setup(
    name = 'pump_controller',
    author = 'K. Gambhir, L. Nyeland, R. Ziskason - DTU Energy',
    version = '1.0',
    description = '',
    license = 'MPL-2.0',
    packages = find_packages(),
    python_requires = '>=3.9.6',
    install_requires = [
        'pyserial',
        'numpy',
        'pandas',
        'matplotlib',
        'datetime',
        'botorch',
        'scipy',
        'torch',
        'IPython'
    ]
)