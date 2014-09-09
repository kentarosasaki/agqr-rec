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
timer_recording_agrec.py: recording timer by using cron
"""


__author__ = "Kentaro Sasaki"
__copyright__ = "Copyright 2014 Kentaro Sasaki"


import datetime
import os
import sys


from reclib import agqr
from reclib import check_schedule
from reclib import cmd_args
from reclib import exception


# Check Python version
if sys.version_info < (2, 7):
  raise exception.UnsupportedPythonVersionError(sys.version)


def main():
  # Define json file
  base_path = os.path.dirname(os.path.realpath(__file__))
  programs = os.path.join(base_path, "programs.json")
  if not os.path.exists(programs):
    raise exception.JsonFileError(programs)

  target_program = check_schedule.check_target(programs)
  if target_program is None:
    raise exception.TimerScheduleIncorrect()

  today = datetime.datetime.now().strftime("%Y%m%d")

  radio_path = target_program["path"]
  json_title = "_".join([target_program["title"], today])
  json_length = target_program["length"]
  agqr.run(radio_path, json_title, json_length)


if __name__ == '__main__':
  main()
