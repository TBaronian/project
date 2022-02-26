from setuptools import setup

with open("README.md") as infile:
    readme = infile.read()

setup("project_repo", 
      name="Part III Project", 
      version="1.0.0",
      description="A python project for a physics simulation", 
      long_description=readme,
      author="Takvor Baronian",
      author_email="tbaronian@ymail.com",
      url="https://github.com/TBaronian/project")
