from setuptools import setup, Distribution, find_packages


class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True


setup(
    name='py2exe',
    version='0.6.9',
    description='Built wheel',
    packages=find_packages(),
    py_modules=['zipextimporter'],
    include_package_data=True,
    package_data={'py2exe': ['../_memimporter.pyd', '*']},
    distclass=BinaryDistribution
)
