from setuptools import setup
import json


with open("metadata.json", encoding="utf-8") as fp:
    metadata = json.load(fp)


setup(
    name="lexibank_zariquieypano",
    version="1.0",
    description=metadata["title"],
    license=metadata.get("license", ""),
    url=metadata.get("url", ""),
    py_modules=["lexibank_zariquieypano"],
    include_package_data=True,
    zip_safe=False,
    entry_points={"lexibank.dataset": ["zariquieypano=lexibank_zariquieypano:Dataset"]},
    install_requires=["beautifulsoup4>=4.7.1", "pylexibank>=3.0"],
    extras_require={"test": ["pytest-cldf"]},
)
