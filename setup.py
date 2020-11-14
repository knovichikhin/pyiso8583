from setuptools import setup, find_packages
from iso8583 import __version__

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

if __name__ == "__main__":

    with open("README.rst", "r", encoding="utf-8") as f:
        readme = f.read()

    setup(
        name="pyiso8583",
        version=__version__,
        author="Konstantin Novichikhin",
        author_email="konstantin.novichikhin@gmail.com",
        description="A serializer and deserializer of ISO8583 data.",
        long_description=readme,
        long_description_content_type="text/x-rst",
        license="MIT",
        url="https://github.com/knovichikhin/pyiso8583",
        packages=find_packages(exclude=["tests"]),
        package_data={"iso8583": ["py.typed"]},
        zip_safe=False,
        classifiers=classifiers,
        python_requires=">=3.6",
        keywords="iso8583 8583 banking protocol library",
    )
