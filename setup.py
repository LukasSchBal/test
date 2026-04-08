from setuptools import setup, find_packages

setup(
    name="process-intelligence",
    version="6.0.0",
    description="A sample process intelligence Python project.",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0"],
    },
)
