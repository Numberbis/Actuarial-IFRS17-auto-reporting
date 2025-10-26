from setuptools import setup, find_packages

setup(
    name="ifrs17-reporting",
    version="0.1.0",
    description="Automated IFRS 17 Actuarial Reporting System",
    author="Actuarial Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
    ],
    python_requires=">=3.9",
)
