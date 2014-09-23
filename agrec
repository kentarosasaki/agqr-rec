#!/usr/bin/env python
# coding=utf-8
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
recording_agqr.py: python agqr radio recording command line tool
"""


__author__ = "Kentaro Sasaki"
__copyright__ = "Copyright 2014 Kentaro Sasaki"


import sys


from reclib import agqr
from reclib import exception


# Check Python version
if sys.version_info < (2, 7):
  raise exception.UnsupportedPythonVersionError(sys.version)


def main():
  sys.exit(agqr.run())


if __name__ == '__main__':
  main()
