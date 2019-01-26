from setuptools import setup, Distribution, find_packages


class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True


setup(
    name='comtypes',
    version='0.6.2',
    description='Built wheel',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*']},
    distclass=BinaryDistribution
)
