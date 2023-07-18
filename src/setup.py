from setuptools import setup, find_packages

VERSION = '0.0.37'
DESCRIPTION = 'Package for LatticeGeometryLib'
LONG_DESCRIPTION = 'Package for LatticeGeometryLib'

# Setting up
setup(
    # the name must match the folder name 'LatticeGeometryLib'
    name="LatticeGeometryLib",
    author="Dennis Schulz",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'cadquery'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)