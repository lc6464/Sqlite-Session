from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
	long_description = f.read()


setup(
	name="Sqlite-Session",
	description="Use SQLite to store session data on the server.",
	version="0.1.0",
	packages=find_packages(),
	url="https://github.com/lc6464/Sqlite-Session",
	license="MIT License",
	long_description=long_description,
	long_description_content_type="text/markdown"
)