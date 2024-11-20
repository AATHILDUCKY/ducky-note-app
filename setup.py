from setuptools import setup, find_packages

setup(
    name="ducky-notes",
    version="1.0.0",
    description="A simple note-taking application with a Tkinter GUI.",
    author="Aathil Ducky",
    author_email="aathilducky@gmail.com",
    url="https://github.com/AATHILDUCKY/ducky-note-app",  # Your GitHub repo or project URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "tkinter",
    ],
    entry_points={
        "console_scripts": [
            "note-app=note_app.app:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
