from setuptools import setup


setup(name='revcontent',
      version='0.1',
      description='Python Client for RevContent API',
      author='Ronnie Beltran',
      author_email='rbbeltran.09@gmail.com',
      url='https://github.com/ronbeltran/revcontent',
      packages=['revcontent'],
      include_package_data=True,
      install_requires=[
          'requests>=2.0',
      ])
