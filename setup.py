from setuptools import setup

package_name = "dynamo-store"

packages = [package_name]

setup(
    name=package_name,
    version='1.0.0',
    description='Client for dynamodb as a keystore',
    url='https://github.com/rajeev1982/pyboot',
    author='Vijay Jain',
    author_email='mnnit.vijay@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords=['dynamo','key-value store'],
    packages=packages,
    install_requires=[
        'boto3>=1.4.3'
    ],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)