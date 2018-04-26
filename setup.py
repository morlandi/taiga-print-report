from setuptools import setup

requirements = [
    # 'requests>2.11',
    # 'six>=1.9',
    # 'python-dateutil>=2.4',
    # 'pyjwkest>=1.0',
    'python-taiga',
]


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='taiga-print-report',
      version='1.0.0',
      description='A simple script to extract an HTML report from a Taiga project',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Internet',
      ],
      keywords='taiga',
      url='https://github.com/morlandi/taiga-print-report.git',
      author='Mario Orlandi',
      author_email='morlandi@brainstorm.it',
      license='MIT',
      scripts=['bin/taiga_print_report'],
      packages=[
        'taiga_print_report'
      ],
      install_requires=requirements,
      dependency_links=[
          # why is this ignored ?
          'git+https://github.com/morlandi/python-taiga.git',
      ],
      include_package_data=False,
      zip_safe=False)
