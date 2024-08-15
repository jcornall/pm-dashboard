#!/usr/bin/env python3.12
#-*- coding: utf-8 -*- 
"""This module defines the abstract APIExport class, from which all other export classes inherit from.
"""

from abc import ABC, abstractmethod


class APIExport:

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set_values(self, response_json):
        pass

    @abstractmethod
    def log_status_code(self, status_code):
        pass