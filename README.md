agqr-rec [![Apache License](http://img.shields.io/hexpm/l/plug.svg?style=flat)](https://github.com/kentarosasaki/agqr-rec/blob/master/LICENSE)
===

## Description

`agqr-rec` is the command line and cron job tools to record agqr(超!A&G+) shows.

`agqr-rec` は、超!A&G+ の番組を録画するためのコマンドラインとcronジョブのツールです。

## Installation

To install, run `git clone`.

```bash
$ git clone https://github.com/kentarosasaki/agqr-rec.git
```

## Usage

You just run `record.py` directory or register `timer.py`.

```bash
$ cd agqr
$ python agrec record [-h] [-o OUTPUT] [-l LENGTH]
```

Agqr shows start every 15 minutes.

```bash
$ crontab -e
```

```bash
*/15 * * * * python ${INSTALL_PATH}/agrec timer
```

## Requirements

`Python` version is required at least Python 2.7.

Before use this tools, install `ffmpeg` and `rtmpdump`.

```bash
$ sudo apt-get install -y ffmpeg rtmpdump
```
```bash
$ sudo yum install -y ffmpeg rtmpdump
```

## Preparation

When you use `agrec timer`, you need to edit `programs.json`.

`path` is path to store output mp4 files.

`title` becomes the base mp4 file name. File name becomes `title`_${datetime}.mp4.

`weekday` is the day of the week as an integer, where Monday is 1 and Sunday is 7.

`showtime` is the start time.

`length` is length of showtime, set by second.


```bash
[
    {
        "path": "/root/agqr-rec",
        "title": "suzakinishi",
        "weekday": "3",
        "showtime": "01:00",
        "length": "1800"
    },
    {
        "path": "/root/agqr-rec",
        "title": "ojikan",
        "weekday": "3",
        "showtime": "23:00",
        "length": "1800"
    }
]
```
