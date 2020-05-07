from setuptools import setup, find_packages


setup(
    name='ansible-locate',
    version='1.0',
    author='alancoding',
    author_email='arominge@redhat.com',
    description='Crawls playbooks, tells you where stuff lives.',
    license='MIT',
    install_requires=['ansible-base'],
    entry_points={
        'console_scripts': [
            'ansible-locate=ansible_locate.cli:main'
        ],
    },
    packages=['ansible_locate'],
)
