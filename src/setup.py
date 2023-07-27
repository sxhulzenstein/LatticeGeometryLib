from setuptools import setup, find_packages

DESCRIPTION = 'Package for generating periodic truss based lattices'

# Setting up
setup(
    # the name must match the folder name 'latticegeometrylib'
    name="latticegeometrylib",
    author="Dennis Schulz",
    version='0.0.19',
    description=DESCRIPTION,
    long_description=open('README.rst').read(),
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