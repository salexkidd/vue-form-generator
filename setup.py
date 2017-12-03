from setuptools import setup, find_packages
import vue_form_generator

try:
    with open("README.md") as f:
        long_description = f.read()

except Exception as e:
    long_description = ""

setup(
    name='restframework-vue-form-generator',
    author = "salexkidd",
    author_email = "salexkidd@gmail.com",
    url = "",
    description='restframework-vue-form-generator',
    long_description=long_description,
    keywords = ["django", "restframework", "serializer", "vuejs"],
    version=vue_form_generator.__VERSION__,
    packages=find_packages(
        exclude=[
            "*.tests", "*.tests.*", "tests.*", "tests",
        ]
    ),
    package_data={},
    license="MIT",
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
