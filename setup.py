#-*- coding: utf-8 -*-
import setuptools
import io
with io.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gsdcpython",
    version="0.2.0",
    author="geonmo",
    author_email="geonmo@kisti.re.kr",
    description="Compare CMS DAS DB and site's data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geonmo/XrdRepairV2",
    project_urls={
        "Bug Tracker": "https://github.com/geonmo/XrdRepairV2/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
