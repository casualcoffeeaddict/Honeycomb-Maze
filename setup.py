import setuptools

print(setuptools.find_packages())
setuptools.setup(
      # package metadata
      name='honeycomb_maze',
      version='0.1.01',
      description="Python Implementation of John O'Keefe's Honeycomb Maze",
      long_description='Please Contact SWC or alif.aziz@icloud.com for implementation',
      long_description_content_type="text/markdown",

      #
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False,

      # source metadata:
      url='https://github.com/casualcoffeeaddict/Honeycomb-Maze',
      author='Alif Ul Aziz',
      author_email='alif.aziz@icloud.com',

      # declare dependencies here:
      # find dependencies on PyPI - default install location: https://pypi.org
      install_requires=[
            'networkx',
            'logging',
            'paramiko',
            'matplotlib'
      ],
)