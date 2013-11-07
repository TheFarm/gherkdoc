from setuptools import setup

setup(
    name='gherkdoc',
    version='0.1.0',
    author='Pontus Jensen Karlsson',
    author_email='pontus@thefarm.se',
    packages=['gherk_doc'],
    package_data={'gherk_doc' : ['templates/*/*.min.*', 'templates/index.html']},
    scripts=['bin/gherkdoc'],
    license='LICENSE.txt',
    description='A documentation generator for gherkin-feature files.',
    #long_description=open('README.txt').read(),
    install_requires=[
        "Jinja2 == 2.7.1",
        "behave == 1.2.3",
    ],
)