"""
Setup script for labellerr-alo package.

This allows the package to be installed via pip and uploaded to PyPI.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="labellerr-alo",
    version="0.2.0",
    author="Labellerr Team",
    author_email="support@labellerr.com",
    description="Agentic Labeling Orchestrator - Intelligent labeling pipelines powered by AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1sarthakbhardawaj/labellerr-alo",
    project_urls={
        "Bug Tracker": "https://github.com/1sarthakbhardawaj/labellerr-alo/issues",
        "Documentation": "https://github.com/1sarthakbhardawaj/labellerr-alo/blob/main/README.md",
        "Source Code": "https://github.com/1sarthakbhardawaj/labellerr-alo",
        "Changelog": "https://github.com/1sarthakbhardawaj/labellerr-alo/releases",
    },
    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: CrewAI",
    ],
    python_requires=">=3.8",
    install_requires=[
        "labellerr-sdk>=1.0.0",
        "pyyaml>=6.0",
        "pydantic>=2.0.0",
        "requests>=2.28.0",
        "tqdm>=4.65.0",
        "python-dotenv>=1.0.0",
        "numpy>=1.21.0",
        "pillow>=9.0.0",
        "crewai>=0.11.0",
        "crewai-tools>=0.2.0",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.5",
        "langchain-anthropic>=0.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
            "pre-commit>=3.0.0",
        ],
        "agents": [
            "openai>=1.0.0",
            "anthropic>=0.18.0",
            "transformers>=4.30.0",
            "torch>=2.0.0",
            "ultralytics>=8.0.0",
        ],
        "all": [
            "labellerr-alo[dev,agents]",
        ],
    },
    entry_points={
        "console_scripts": [
            "alo=alo.cli:main",
        ],
    },
    keywords=[
        "machine-learning",
        "computer-vision",
        "data-labeling",
        "annotation",
        "ai-agents",
        "active-learning",
        "mlops",
        "labellerr",
        "crewai",
        "autonomous-ai",
    ],
    include_package_data=True,
    zip_safe=False,
)
