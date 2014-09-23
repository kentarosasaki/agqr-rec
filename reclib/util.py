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
util.py: utilities of agqr radio recording interface
"""


__author__ = "Kentaro Sasaki"
__copyright__ = "Copyright 2014 Kentaro Sasaki"


import os
import subprocess
import sys


import cmd_args
import exception


def executor(cmd, returncode = 0):
  """Exception handler for running execute function.

  Args:
    cmd: Command arguments
    returncode: Return code of exec command (default: 0)
  """
  try:
    subprocess.check_output(cmd)
    return returncode
  except subprocess.CalledProcessError as exc:
    returncode = int(exc.returncode)
    return returncode


def parent_path(file_path):
  lib_path = os.path.dirname(os.path.realpath(file_path))
  return os.path.split(lib_path)[0]


def recording_util(agqr_url, tmp_flv, output_mp4, length):
  # Define rtmpdump command.
  rtmpdump_cmd = cmd_args.record(agqr_url, length, tmp_flv)

  # Define ffmpeg command.
  ffmpeg_cmd = cmd_args.encode_to_mp4(tmp_flv, output_mp4)

  # Run rtmpdump command.
  returncode = executor(rtmpdump_cmd)

  if returncode is 0:
    # Run ffmpeg command if rtmpdump is successful.
    executor(ffmpeg_cmd)

  if os.path.exists(tmp_flv):
    # Remove existing temporary flv file if exists.
    os.remove(tmp_flv)
