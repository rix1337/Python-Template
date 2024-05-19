#  Python-Template

[![PyPI version](https://badge.fury.io/py/rix-template.svg)](https://badge.fury.io/py/rix-template)
[![Github Sponsorship](https://img.shields.io/badge/support-me-red.svg)](https://github.com/users/rix1337/sponsorship)

Full template for python web projects with Docker, Github Actions, PyPI, and more.

## What to replace on project setup
* `Python-Template` case-sensitive globally, use hyphens for spaces
  * strings in all files 
* `rix_template` case-sensitive globally, use underscores for spaces
  * strings in all files
  * filenames
  * folder names
* `rix-template` case-sensitive globally, must match above but with hyphens (for docker/PyPI)
  * strings in all files
* `A template for my Python projects` case-sensitive globally
  * strings in all files

## Secrets to set up Github Actions
* `DOCKERUSER` dockerhub username
* `DOCKERPASS` dockerhub token
* `PYPI_TOKEN` PyPI token
* `CR_USER` Github username
* `CR_TOKEN` Github token with repo workflow access

# Setup

`pip install rix-template`

# Run

```
rix_template
  --port=8080
  --config=/tmp/config
  --example=test
  ```

# Docker
```
docker run -d \
  --name="Python-Template" \
  -p port:8080 \
  -v /path/to/config/:/config:rw \
  -e 'EXAMPLE'='test'
  rix1337/docker-rix-template:latest
  ```
