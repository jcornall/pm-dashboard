#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-

import sys
from src.tenable.pipeline import tenable

# contains all data extraction pipelines for each patch management tools
pipelines = [tenable]


def main():
    # TODO: multithread this for multiple pipelines
    for pipeline in pipelines:
        pipeline()

    sys.exit(0)


if __name__ == "__main__":
    main()
