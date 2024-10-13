from setuptools import setup, find_packages

setup(
    name='pptx-dictation.file.generator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask',  # Your Flask app's dependencies
        'Flask-Mail',
        'python-dotenv',
        'pytest',
    ],
    dependency_links=[
        'git+https://github.com/denuca/core.file.generator.git#egg=core.file.generator',
    ],
)
