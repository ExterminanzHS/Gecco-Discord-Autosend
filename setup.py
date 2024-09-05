from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gecco-discord-autosend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "nextcord==2.5.0",
        "Pillow==9.5.0",
        "python-dotenv==1.0.0",        
        "numpy==1.24.3",
    ],
    author="ExterminanzHS",
    author_email="cyberlich@protonmail.com",  # Replace with your email
    description="Custom nodes for ComfyUI to send images to Discord channels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ExterminanzHS/Gecco-Discord-Autosend",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)