#!/usr/bin/env python

import setuptools
import subprocess
import os.path
import sys

branch = "unknown"
commit_id = "unknown"
version_file = os.path.join(os.path.dirname(__file__), "jose_oidc", "_version.py")
if os.path.exists(version_file):
    d={}
    execfile(version_file, d)
    branch, commit_id = d['version']
try:
    try:
        branch = subprocess.check_output(["git", "symbolic-ref", "HEAD"]).strip()
        if branch.startswith("refs/heads/"):
            branch = branch[len("refs/heads/"):]
    except:
        pass
    commit_id = subprocess.check_output(["git", "log", "-1", "--pretty=format:'%H'"]).strip("'")
    with open(version_file, "w") as f:
        f.write("version=('%s', '%s')\n" % (branch, commit_id))
except Exception as e:
    pass

setuptools.setup(name='jose-oidc',
      version='%s-%s' % (branch, commit_id),
      description='Lightweight OpenID Connect JWS/JWT token verifier on top of Jose',
      author='Egil Moeller',
      author_email='egil@innovationgarage.no',
      url='https://github.com/innovationgarage/jose-oidc',
      packages=setuptools.find_packages(),
      install_requires=[
          'requests',
          'jose'
      ],
      include_package_data=True
  )
