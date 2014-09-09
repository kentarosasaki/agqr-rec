agqr-rec [![Apache License](http://img.shields.io/hexpm/l/plug.svg?style=flat)](https://github.com/kentarosasaki/agqr-rec/blob/master/LICENSE)
===

## Description

`agqr-rec` is the command line and cron job tools to record agqr(超!A&G+) shows.

## Installation

To install, run `git clone`.

```bash
$ git clone
```

## Usage

You just run `record.py` directory or register `timer.py`.

```bash
$ cd agqr
$ python recording.py [-h] [-d] [-a AGQR_STREAMING_URL] [-o OUTPUT] [-l LENGTH]
```

Agqr shows start every 15 minutes.

```bash
$ crontab -e
```

```bash
*/15 * * * * python ${INSTALL_PATH}/timer.py
```

## Requirement

`Python` version is required at least Python 2.7.

Before use this tools, install `ffmpeg` and `rtmpdump`.

```bash
$ sudo apt-get install -y ffmpeg rtmpdump
```
```bash
$ sudo yum install -y ffmpeg rtmpdump
```

## Preparation

When you use `timer.py`, you need to edit `programs.json`.
`path` is path to store output mp4 files.
`title` becomes the base mp4 file name. File name becomes `title`_${datetime}.mp4.
`weekday` is the day of the week as an integer, where Monday is 1 and Sunday is 7.
`showtime` is the start time.
`length` is length of showtime, set by second.


```bash
[
    {
        "path": "/root/agqr",
        "title": "suzakinishi",
        "weekday": "3",
        "showtime": "01:00",
        "length": "1800"
    },
    {
        "path": "/root/agqr",
        "title": "ojikan",
        "weekday": "3",
        "showtime": "23:00",
        "length": "1800"
    }
]
```
