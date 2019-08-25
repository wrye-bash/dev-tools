from setuptools import setup, Distribution, find_packages


class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True


setup(
    name='wxPython',
    version='3.0.2.0',
    description='Built wheel',
    packages=find_packages(),
    py_modules=['wxversion'],
    include_package_data=True,
    distclass=BinaryDistribution
)
