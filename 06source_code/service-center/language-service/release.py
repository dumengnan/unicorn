#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import os.path
import shutil

import sys

current_file_dir = os.path.dirname(__file__)
py_strip_dirs = open(
    os.path.join(current_file_dir, "strip_py.list")).readlines()


def _copytree(src, dst, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    try:
        os.makedirs(dst)
    except:
        pass

    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.isdir(srcname):
                shutil.copytree(srcname, dstname, ignore=ignore)
            else:
                shutil.copy2(srcname, dstname)
        except shutil.Error, err:
            errors.extend(err.args[0])
        except EnvironmentError, why:
            errors.append(srcname, dstname, str(why))

    try:
        shutil.copystat(src, dst)
    except OSError, why:
        if WindowsError is not None and isinstance(why, WindowsError):
            pass
        else:
            errors.extend((src, dst, str(why)))

    if errors:
        raise shutil.Error, errors


def _zip_file(target_dir):
    shutil.make_archive(target_dir, format="gztar",
                        root_dir=target_dir)
    #shutil.move(target_dir + ".zip", target_dir +".egg")


def _strip_py(py_dir):
    for base, dirs, files in os.walk(py_dir):
        for name in files:
            if name.endswith('.py'):
                path = os.path.join(base, name)
                logging.debug("Deleting %s", path)
                os.unlink(path)


def main():
    site_package_dir = sys.argv[2]
    target_dir = sys.argv[3]

    shutil.rmtree(target_dir, ignore_errors=True)
    os.makedirs(target_dir)

    copy_dirs = ['bin', 'etc', 'logs']

    lib_dir = os.path.join(target_dir, 'lib')
    _copytree(site_package_dir, lib_dir)
    
    for dir_name in copy_dirs:
        _copytree(dir_name, os.path.join(target_dir, dir_name))

    for py_dir in py_strip_dirs:
        _strip_py(os.path.join(target_dir, py_dir))

    _zip_file(target_dir)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logging.exception("main except")
        sys.exit(1)