from setuptools import setup, find_packages

setup(
    name='pptx-dictation.file.generator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask',  # Your Flask app's dependencies
        'Flask-Mail',
        'Pillow', # Move Pillow to core lib
        'python-dotenv',
        'python-pptx',
        'pytest',
        'werkzeug',
        'core.file.generator @ git+https://github.com/denuca/core.file.generator.git@main#egg=core.file.generator'
    ],
    #dependency_links=[
    #    'git+https://github.com/denuca/core.file.generator.git#egg=core.file.generator',
    #],
)
