#!/usr/bin/env python
from migrate.versioning.shell import main
main(url='postgresql://postgres:password@localhost:5432/gateway', debug='True', repository='.')
