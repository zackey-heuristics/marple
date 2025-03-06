import setuptools
from setuptools import setup


setup(
    name="marple-json",
    version="0.1.0",
    author="zackey-heuristics",
    description="Output the results of the Marple analysis in JSON format.",
    url="https://github.com/zackey-heuristics/marple",
    py_modules=["marple", "marple_json_output"],
    install_requires=[
        "aiohttp>=3.8.0",
        "termcolor>=2.0.0",
        "beautifulsoup4>=4.9.0",
        "requests>=2.25.0",
        "yandex-search>=0.3.2",
        "PyPDF2>=2.0.0",
        "socid-extractor>=0.0.1",
        "aiohttp-socks>=0.7.0",
        "tqdm>=4.65.0",
        "google-search-results>=2.4.0",
        "mock>=4.0.0",
        "arabic-reshaper>=2.1.4",
        "maigret @ https://github.com/soxoj/maigret/archive/refs/heads/master.zip",
        "search-engines @ https://github.com/soxoj/Search-Engines-Scraper/archive/refs/heads/master.zip",
    ],
    entry_points={
        "console_scripts": [
            "marple-json=marple_json_output:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
)
