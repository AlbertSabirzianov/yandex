from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()


setup(
  name='yandex-searcher',
  version='0.0.3',
  author='Albert Sabirzianov-Valizer',
  author_email='albertuno@mail.ru',
  description='Библиотека для удобного взаимодействия с поисковой системой Яндекс. Позволяет получать ссылки на изображения и статьи по заданному поисковому запросу.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/AlbertSabirzianov/yandex',
  packages=find_packages(),
  install_requires=['selenium==4.27.1', 'webdriver-manager==4.0.2', 'selenium-stealth==1.0.6'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='search yandexsearcher',
  project_urls={
    'GitHub': 'https://github.com/AlbertSabirzianov/yandex'
  },
  python_requires='>=3.12'
)