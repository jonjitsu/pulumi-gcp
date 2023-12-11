# Overview

# Repo Organization

## npm workspaces
The repo uses npm workspaces. There are two separate workspaces:
1. packages/ - where the code lives
2. examples/ - examples that use the code in packages

examples/* needs to be configured in the root package.json:workspaces for this to work.