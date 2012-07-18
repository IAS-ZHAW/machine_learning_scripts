from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name='mlscripts',
    version=version,
    description='Machine learning scripts for Atizo.',
    author='Thomas Niederberger',
    author_email='nith@zhaw.ch',
    url='http://github.com/atizo/machine_learning_scripts',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='machine-learning',
    include_package_data=True,
    zip_safe=False,
)
