#!/usr/bin/env python3.12
#-*- coding: utf-8 -*-
"""This module defines the DataValidator class, used to validate both raw and processed data.
"""

from src.config.transform_config import *
from pathlib import Path
import pandas as pd
import re
import json


class DataValidator():

    def __init__(self):
        pass