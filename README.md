# Fast Stream Rotations

This code outlines how to match Fast Streamers with their next role. It is currently in development.

## Installation
Download this software with `git`. You will need [poetry](https://python-poetry.org/docs/) to run it effectively.

## Rules
The rules for matching are being codified in the `Pair` class. The weightings are still subject to change, and at some
point I'll need to find a way for users to make these changes.

## Script
There is a script in the `fast_stream_22.scripts` path. You can run it with

```commandline
> poetry run pairing_script --candidates path/to/candidates.csv --roles path/to/roles.csv
```
Your CSV files will need to be aligned to the expectations of the software. I'll upload examples soon, but
unfortunately all of mine currently have real data in!

## License
This work is licenced under MIT.
