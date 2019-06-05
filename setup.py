from setuptools import setup


setup(name='ecflow_cloudwatch',
      version='1.0.0',
      packages=['ecflow_cloudwatch'],
      entry_points={
          'console_scripts': [
              'ecflow_cloudwatch = ecflow_cloudwatch.__main__:main'
              ]
      },
      install_requires=['boto3>=1.7.79'],
      zip_safe=False
      )