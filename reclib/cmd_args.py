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
cmd_args.py: return command arguments
"""


__author__ = "Kentaro Sasaki"
__copyright__ = "Copyright 2014 Kentaro Sasaki"


import logging


def record(agqr_url, length, output_flv):
  """Command line strings.

  Args:
    agqr_stream_url: Target agqr url
    length: Recording length (Sec)
    output: Output flv file

  Returns:
    Strings for running rtmpdump command.
  """
  rtmpdump_list = ["rtmpdump", "-r", str(agqr_url), "--live", "-B",
                   str(length), "-o", str(output_flv)]
  logging.debug("Running command args list: %s" % rtmpdump_list)
  return rtmpdump_list


def encode_to_mp4(input_flv, output_mp4):
  """Command line strings.

  Args:
    input_flv: Target agqr url
    output: Output flv file

  Returns:
    Strings for running rtmpdump command.
  """
  ffmpeg_list = ["ffmpeg", "-y", "-i", str(input_flv),
                 "-vcodec", "copy", "-acodec", "copy", str(output_mp4)]
  logging.debug("Running command args list: %s" % ffmpeg_list)
  return ffmpeg_list
