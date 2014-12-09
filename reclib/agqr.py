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
import sys
import uuid


import check_schedule
import cmd_args
import exception
import util


def option():
  parser = argparse.ArgumentParser(description = "AGQR recording interface")
  parser.add_argument("-d", "--debug", action = "store_true", default = False,
                      help = "debug mode if this flag is set")
  parser.add_argument("-a", "--agqr-streaming-url", type = str,
      default = "rtmp://fms-base1.mitene.ad.jp/agqr/aandg11",
      help = "agqr streaming url"
      "(default: rtmp://fms-base1.mitene.ad.jp/agqr/aandg11)")

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


def record(args):
  base_path = util.parent_path(__file__)
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

  util.recording_util(agqr_url, tmp_flv, output_mp4, length)


def timer(args):
  # Define json file
  base_path = util.parent_path(__file__)
  logging.debug("Base binary path: %s" % base_path)

  if args.json is not None:
    programs = args.json
  else:
    programs = os.path.join(base_path, "programs.json")

  if not os.path.exists(programs):
    raise exception.JsonFileError(programs)

  target_program = check_schedule.check_target(programs)
  if target_program is None:
    raise exception.TimerScheduleIncorrect()

  today = datetime.datetime.now().strftime("%Y%m%d")

  radio_path = target_program["path"]
  json_title = "_".join([target_program["title"], today])

  file_uuid = uuid.uuid4()
  tmp_flv = os.path.join(base_path, ".".join([str(file_uuid), "flv"]))

  # Define output mp4 file name.
  output_mp4 = os.path.join(radio_path, ".".join([json_title, "mp4"]))
  logging.debug("mp4 file name is %s" % output_mp4)

  # Define recording length.
  length = target_program["length"]
  logging.debug("showtime length is %s" % length)

  agqr_url = args.agqr_streaming_url

  util.recording_util(agqr_url, tmp_flv, output_mp4, length)


def run():
  args = option()

  if args.debug:
    logging.basicConfig(level=logging.DEBUG)

  args.func(args)
