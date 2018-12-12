#!/usr/bin/env python
# encoding: utf-8

from flask import Flask

app = Flask(__name__)


def main():
    app.run(host='0.0.0.0', port=8001, debug=True)


if __name__ == '__main__':
    main()
