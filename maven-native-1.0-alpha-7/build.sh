#!/bin/sh
# disable test from build
mvn-rpmbuild -Dmaven.test.skip=true
