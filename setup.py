from setuptools import setup, find_packages

setup(
    name="ducky-notes",
    version="1.0.0",
    author="Aathil Ducky",
    author_email="aathilducky@gmail.com",
    description="A simple note-taking app for ethical hackers to store, organize, and quickly access commands and important notes efficiently.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AATHILDUCKY/ducky-note-app",
    packages=find_packages(),
    include_package_data=True,  # Includes files specified in MANIFEST.in
    install_requires=[
        "PyQt5",
        "sqlite3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "notetakingapp=notetakingapp.app:main",  # Add main entry point
        ],
    },
)
