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
check_schedule.py: check correct scheduled show title information
"""


__author__ = "Kentaro Sasaki"
__copyright__ = "Copyright 2014 Kentaro Sasaki"


import datetime
import json
import logging


def _load_json(file_name):
  logging.debug("Open json file: %s" % file_name)
  with open(file_name) as fp:
    return json.load(fp)


def _check_weekday(weekday, now, check = False):
  """
  """
  if int(weekday) == now.isoweekday():
    check = True
  logging.debug("Check correct weekday flag: %s" % check)
  return check


def _check_showtime(showtime, now, check = False):
  """
  """
  if showtime == now.strftime("%H:%M"):
    check = True
  logging.debug("Check correct showtime flag: %s" % check)
  return check


def check_target(programs_json, program = None):
  now = datetime.datetime.now()
  logging.debug("Now is %s" % str(now))
  programs = _load_json(programs_json)
  for i in range(len(programs)):
    weekday = programs[i]["weekday"]
    showtime = programs[i]["showtime"]
    if (_check_weekday(weekday, now) and _check_showtime(showtime, now)):
      program = programs[i]
      return program
