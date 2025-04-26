#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 17:28:11 2024

@author: zacharywen
"""

from flask import Flask

app = Flask("untitled0")

@app.route('/')
def hello_world():
    return "Hello world, this is going to a web browser"

app.run()