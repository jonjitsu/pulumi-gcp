from invoke import task

ORG = "@jonjitsu"
PACKAGES_DIR = "./packages"
EXAMPLES_DIR = "./examples"

@task
def new_package(c, name: str, org: str = ORG, where: str = PACKAGES_DIR):
    """Initialize a new package"""
    c.run(f"npm init --scope {org} --workspace {where}/{name} -y")

@task
def new_example(c, name: str, org: str = ORG, where: str = EXAMPLES_DIR):
    """Initialize a new example"""
    c.run(f"npm init --scope {org} --workspace {where}/{name} -y")

@task
def build_package(c, name: str, where: str = PACKAGES_DIR):
    """Build a package"""
    c.run(f"npm run build --workspace {where}/{name}")


@task
def setup(c):
    """Setup the project"""
    c.run("npm install")


@task
def install_package(
    c, name: str, dest: str, org: str = ORG, packages_dir: str = PACKAGES_DIR
):
    """ Install a packages/ package into a destination workspace. """
    c.run(f"npm install {org}/{name} --workspace {dest}")

@task
def install(c, package: str, dest: str):
    """Install a third party package into a workspace. """
    c.run(f"npm install {package} --workspace {dest}")