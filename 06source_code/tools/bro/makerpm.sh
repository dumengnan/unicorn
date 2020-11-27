#! /bin/bash

mkdir -p /root/rpmbuild/SPECS
mkdir -p /root/rpmbuild/SOURCES


rpmbuild -ba SPECS/bro.spec --define 'release_version 3.0.11' --define 'release_num 1'