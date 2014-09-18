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


import check_schedule
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


def option():
  parser = argparse.ArgumentParser(description = "AGQR recording interface")
  parser.add_argument("-d", "--debug", action = "store_true", default = False,
                      help = "debug mode if this flag is set")
  parser.add_argument("-a", "--agqr-streaming-url", type = str,
      default = "rtmp://fms-base1.mitene.ad.jp/agqr/aandg2",
      help = "agqr streaming url"
      "(default: rtmp://fms-base1.mitene.ad.jp/agqr/aandg2)")

  subparsers = parser.add_subparsers()

  parser_record = subparsers.add_parser("record", help = "record help")
  parser_record.add_argument("-o", "--output", type = str,
      help = "recording mp4 file"
      "(default: ${installed_path}/${random_uuid}.mp4)")
  parser_record.add_argument("-l", "--length", type = int, default = 10,
                      help = "recording time[sec](default: 10[sec])")
  parser_record.set_defaults(func = record)

  parser_timer = subparsers.add_parser("timer", help = "timer help")
  parser_timer.add_argument("-j", "--json", type = str,
      help = "agqr show info json file"
      "(default: ${installed_path}/programs.json)")
  parser_timer.set_defaults(func = timer)

  return parser.parse_args()


def define_path(file_path):
  lib_path = os.path.dirname(os.path.realpath(file_path))
  return os.path.split(lib_path)[0]


def record(args):
# print(args.output)
  base_path = define_path(__file__)
  logging.debug("Base binary path: %s" % base_path)
  file_uuid = uuid.uuid4()
  tmp_flv = os.path.join(base_path, ".".join([str(file_uuid), "flv"]))
  tmp_mp4 = os.path.join(base_path, ".".join([str(file_uuid), "mp4"]))

  # Define output mp4 file name.
  if args.output is not None:
    output_mp4 = args.output
  else:
    output_mp4 = tmp_mp4
  logging.debug("mp4 file name is %s" % output_mp4)

  # Define recording length.
  length = args.length
  logging.debug("showtime length is %s" % length)

  agqr_url = args.agqr_streaming_url

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


def timer(args):
  # Define json file
  base_path = define_path(__file__)
  logging.debug("Base binary path: %s" % base_path)
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
 #agqr.run(radio_path, json_title, json_length)
  file_uuid = uuid.uuid4()
  tmp_flv = os.path.join(base_path, ".".join([str(file_uuid), "flv"]))
  tmp_mp4 = os.path.join(base_path, ".".join([str(file_uuid), "mp4"]))

  # Define output mp4 file name.
  if (radio_path and json_title):
    output_mp4 = os.path.join(radio_path, ".".join([json_title, "mp4"]))
  else:
    output_mp4 = tmp_mp4
  logging.debug("mp4 file name is %s" % output_mp4)

  # Define recording length.
  length = json_length
  logging.debug("showtime length is %s" % length)

  agqr_url = args.agqr_streaming_url

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


def run(radio_path = None, json_title = None, json_length = None):
  args = option()

  if args.debug:
    logging.basicConfig(level=logging.DEBUG)

  args.func(args)

#  base_path = os.path.dirname(os.path.realpath(__file__))
#  logging.debug("Base binary path: %s" % base_path)
#  file_uuid = uuid.uuid4()
#  tmp_flv = os.path.join(base_path, ".".join([str(file_uuid), "flv"]))
#  tmp_mp4 = os.path.join(base_path, ".".join([str(file_uuid), "mp4"]))
#
#  # Define output mp4 file name.
#  if (args.output is None and radio_path and json_title):
#    output_mp4 = os.path.join(radio_path, ".".join([json_title, "mp4"]))
#  elif args.output is not None:
#    output_mp4 = args.output
#  else:
#    output_mp4 = tmp_mp4
#  logging.debug("mp4 file name is %s" % output_mp4)
#
#  # Define recording length.
#  if json_length is None:
#    length = args.length
#  else:
#    length = json_length
#  logging.debug("showtime length is %s" % length)
#
#  agqr_url = args.agqr_streaming_url
#
#  # Define rtmpdump command.
#  rtmpdump_cmd = cmd_args.record(agqr_url, length, tmp_flv)
#
#  # Define ffmpeg command.
#  ffmpeg_cmd = cmd_args.encode_to_mp4(tmp_flv, output_mp4)
#
#  # Run rtmpdump command.
#  returncode = executor(rtmpdump_cmd)
#
#  if returncode is 0:
#    # Run ffmpeg command if rtmpdump is successful.
#    executor(ffmpeg_cmd)
#
#  if os.path.exists(tmp_flv):
#    # Remove existing temporary flv file if exists.
#    os.remove(tmp_flv)
