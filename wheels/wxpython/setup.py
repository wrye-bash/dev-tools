from setuptools import setup, Distribution, find_packages


class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True


setup(
    name='wxPython',
    version='2.8.12.1',
    description='Built wheel',
    packages=find_packages(),
    py_modules=['wxversion'],
    # package_data={'': ['*'], 'wx': ['locale'],},
    include_package_data=True,
    distclass=BinaryDistribution
)
