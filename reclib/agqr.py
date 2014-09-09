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
agqr.py: agqr radio recording interface
"""


__author__ = "Kentaro Sasaki"
__copyright__ = "Copyright 2014 Kentaro Sasaki"


import argparse
import datetime
import logging
import os
import subprocess
import sys
import uuid


import cmd_args
import exception


def executor(cmd):
  """Exception handler for running execute function.

  Args:
    cmd: Command arguments
  """
  try:
    ret = subprocess.check_output(cmd)
  except Exception as msg:
    exception.CommandFailedError(str(msg))


def option():
  parser = argparse.ArgumentParser(description = "AGQR recording interface")
  parser.add_argument("-d", "--debug", action = "store_true", default = False,
                      help = "debug mode if this flag is set")
  parser.add_argument("-a", "--agqr-streaming-url", type = str,
      default = "rtmp://fms-base1.mitene.ad.jp/agqr/aandg2",
      help = "agqr streaming url")
  parser.add_argument("-o", "--output", type = str,
                      help = "recording mp4 file")
  parser.add_argument("-l", "--length", type = int, default = 1800,
                      help = "recording time[sec] (default: 1800[sec])")
  return parser.parse_args()


def run(radio_path = None, json_title = None, json_length = None):
  args = option()

  if args.debug:
    logging.basicConfig(level=logging.DEBUG)

  base_path = os.path.dirname(os.path.realpath(__file__))
  logging.debug("Base binary path: %s" % base_path)
  file_uuid = uuid.uuid4()
  tmp_flv = os.path.join(base_path, ".".join([str(file_uuid), "flv"]))
  tmp_mp4 = os.path.join(base_path, ".".join([str(file_uuid), "mp4"]))

  # Define output mp4 file name.
  if (args.output is None and radio_path and json_title):
    output_mp4 = os.path.join(radio_path, ".".join([json_title, "mp4"]))
  elif args.output is not None:
    output_mp4 = args.output
  else:
    output_mp4 = tmp_mp4
  logging.debug("mp4 file name is %s" % output_mp4)

  # Define recording length.
  if json_length is None:
    length = args.length
  else:
    length = json_length
  logging.debug("showtime length is %s" % length)

  agqr_url = args.agqr_streaming_url

  rtmpdump_cmd = cmd_args.record(agqr_url, length, tmp_flv)
  executor(rtmpdump_cmd)
  ffmpeg_cmd = cmd_args.encode_to_mp4(tmp_flv, output_mp4)
  executor(ffmpeg_cmd)
  os.remove(tmp_flv)