# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from private_messages import get_version


setup(
    name='django-private-messages',
    version=get_version().replace(' ', '-'),
    description=u'Личные сообщения пользователей.',
    license="BSD License",
    author='Aleksandr Zorin (plazix)',
    author_email='plazix@gmail.com',
    url='https://github.com/plazix/django-private-messages',
    download_url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
