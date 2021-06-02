from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="pgn_to_gif",
    version="0.0.1",
    description="Generate GIFs of chess games from PGN files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/afozk95/pgn-to-gif",
    author="Ahmed Furkan Özkalay",
    author_email="afozk95@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["pgn_to_gif"],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "cairosvg",
        "imageio",
        "python-chess",  
    ],
    entry_points={
        "console_scripts": [
            "pgn2gif=pgn_to_gif.cli:main",
            "pgn-to-gif=pgn_to_gif.cli:main",
        ]
    },
    
    keywords = ["chess", "gif", "pgn"],
)
