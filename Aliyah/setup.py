from setuptools import setup, find_packages

setup(
    name="aliyah-predictor",  # ✅ Unique PyPI name
    version="0.1.2",  # 🔁 Bump this for each new release
    description="Empirical and classical linear predictors with agreement metrics",
    long_description=open("README.md", encoding="utf-8").read(),  # Make sure README.md exists
    long_description_content_type="text/markdown",
    author="Kevin Clarke",
    author_email="your_email@example.com",  # Optional: use a contact email
    url="https://github.com/yourusername/aliyah-predictor",  # Optional: GitHub repo
    packages=find_packages(),  # Automatically finds your package folders
    install_requires=[
        "numpy",
        "scipy"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
