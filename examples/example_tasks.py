from invoke import task
from pathlib import Path

CWD = Path.cwd()
SELF = Path(__file__)
EXAMPLE_DIR = CWD
EXAMPLES_DIR = EXAMPLE_DIR.parent

assert CWD.stem != "examples"

STACK_NAME = f"{CWD.stem}-example"
PULUMI_BACKEND_URL = f"file://{SELF.parent}"
COMMON_ENV = {
	'PULUMI_BACKEND_URL': PULUMI_BACKEND_URL,
	'PULUMI_CONFIG_PASSPHRASE': ''
}

@task
def info(c):
    """Print info"""
    print(f"STACK_NAME: {STACK_NAME}")
    print(f"PULUMI_BACKEND_URL: {PULUMI_BACKEND_URL}")
    print(f"COMMON_ENV: {COMMON_ENV}")
    print(f"EXAMPLE_DIR: {EXAMPLE_DIR}")
    print(f"EXAMPLES_DIR: {EXAMPLES_DIR}")
    print("c.run('pwd'):", end=" ")
    c.run("pwd")
    c.run("env", env=COMMON_ENV)

@task
def init(c):
    """Initialize the project"""
    c.run(f"pulumi stack init -s {STACK_NAME}", env=COMMON_ENV)

@task
def setup(c):
    """Setup the project"""
    c.run("npm install")  

@task
def preview(c):
    """Preview the project"""
    c.run(f"pulumi preview -s {STACK_NAME}", env=COMMON_ENV)

@task
def up(c):
    """Deploy the project"""
    c.run(f"pulumi up -s {STACK_NAME} -y --skip-preview", env=COMMON_ENV)

@task
def destroy(c):
    """Teardown the project"""
    c.run(f"pulumi destroy -s {STACK_NAME} -y", env=COMMON_ENV)

@task(pre=[destroy])
def rm(c):
    """Remove the stack the project"""
    # c.run(f"pulumi stack rm -s {STACK_NAME} -y --preserve-config", env=COMMON_ENV)
    c.run(f"pulumi stack rm -s {STACK_NAME} -y", env=COMMON_ENV)
  
@task(pre=[rm])
def cleanup(c):
    """Cleanup the project"""
    c.run("rm -rf node_modules", warn=True)
    # c.run(f"rm Pulumi.{STACK_NAME}.yaml", warn=True)
    # shutil.rmtree("node_modules", ignore_errors=True)
    # Path(f"Pulumi.{STACK_NAME}.yaml").unlink(missing_ok=True)

@task(pre=[destroy, rm, cleanup])
def clean(c):
    """Clean the project"""

@task(pre=[setup, init, up])
def converge(c):
    """Bring the project into latest state."""

@task(pre=[setup, init, up, destroy, rm, cleanup])
def e2e(c):
    """Run end to end test"""