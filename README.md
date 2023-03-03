# Fast Stream Rotations

This code outlines how to match Fast Streamers with their next role. It is currently in development.

## Background
The Fast Stream is the UK's [best graduate programme](https://www.highfliers.co.uk/download/2022/awards/The-Times-Graduate-Recruitment-Awards-2022.pdf).
Every year, hundreds of graduates and in-service candidates join the scheme. Over the course of three years, they
will experience a wide variety of work: from policy in a ministerial private office to the sharp end of operations
in a JobCentre. Organising these placements, and pairing people off so that they get the best experience possible,
is a huge and complex task.

This software serves to automate that process, eliminate bias, and free up staff time. It does this by:

- quantifying, with the service owners, what a 'good' pairing of candidate and role looks like
- identifying disqualifying factors, such as candidates who cannot relocate
- forming a grid of every potential pairing's score
- finding the grid configuration that enables the highest overall score

As a result, there will never be a pairing where a candidate could find a free role they'd be more suited for.

This solution reduces staff time by 99.997%

## Business process
For this system to work, organisations bid for candidates. They also offer roles for candidates to be put into. For
the system to process these things effectively there must be some slack in the system - that is, the number of roles
must be greater than the number of bids, which must be greater than the number of candidates.

> Roles > Bids > Candidates

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
