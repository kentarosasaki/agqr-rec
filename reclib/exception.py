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
exception.py: collect exception class
"""


__author__ = "Kentaro Sasaki"
__copyright__ = "Copyright 2014 Kentaro Sasaki"


import logging


class Error(Exception):
  # Base error class
  pass


class UnsupportedPythonVersionError(Error):
  def __init__(self, version):
    """Raised on unsupported Python versions.

    param version: Current Python version
    type version: string
    """
    Error.__init__(
        self, ("Python %s is unsupported, requires "
        "at least Python 2.7") % version)


class JsonFileError(Error):
  def __init__(self, json):
    """Raised on non-existent json file.

    param json: Employed json file
    type json: string
    """
    Error.__init__(self, ("Json File %s is not found!") % json)


class ConfigFileError(Error):
  def __init__(self, config):
    """Raised on non-existent config file.

    param config: Employed config file
    type config: string
    """
    Error.__init__(self, ("Config File %s is not found!") % config)


class CommandFailedError(Error):
  def __init__(self, msg):
    """Raised on command failed.

    param msg: Failed command result
    type msg: string
    """
    Error.__init__(self, ("Command Failed: %s") % msg)


class FileNotExist(Error):
  def __init__(self, exist_file):
    """Raised on non-existent file.

    param exist_file: Employed command binary
    type exist_file: string
    """
    Error.__init__(self, ("File %s is not exist!") % exist_file)


class TimerScheduleIncorrect(Error):
  def __init__(self):
    # Raised when cron is not the time for recording.
    Error.__init__(self, ("Now is not the time for recording."))
