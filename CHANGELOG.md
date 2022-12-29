# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.3] - 2022-12-29
### Changed
- in the first round of matching each cohort, departments may only put forwards 80% of their bids for consideration.
  This approach ensures that almost everyone gets at least 80% of their required bids. For following rounds,
  departments put forward (number of bids - number of assigned candidates) bids.
- this approach unfortunately means that some candidates will not get their most suitable role, because it may be
  hidden away as a lower priority. However, as this scheme is funded by departments, we must recognise that their
  priorities come first.

## [0.7.2] - 2022-12-29
### Changed
- `Pair` no longer scores the priority of the role. The priority is used to decide in which order to feed roles into
  the process, but we shouldn't be increasing a role's score just because a department think it's important. Their
  context is not our context

## [0.7.1] - 2022-12-23
### Changed
- the script is updated to print its outputs
- the matching algorithm is reversed, so that it starts by matching the most junior cohort

## [0.7.0] - 2022-12-23
### Added
- a new object, `Process`, is added. This provides an interface for running multiple rounds of matching
- a new `Bid` object is added, which contains the bids for candidates
- We've done this because of a new requirement: often, departments provide more roles than they bid for. Sometimes they
  provide up to 10% more roles than they can afford. The `Process` object takes a `bids` argument.
- Bids should be provided as a CSV file. The department names in both the bids file and the roles file _and_ the
  candidates' previous roles must be the same. This is a fragility in the system I would like to improve in the new year

## [0.6.1] - 2022-11-29
### Changed
- software now matches 'Remote' and 'Available Nationally' as if it were a first_location preference
- fixed bug where leading spaces in locations meant matches were not made correctly

## [0.5.0] - 2022-11-24
### Added
- two new fields added to the Candidate input. These reflect nationality and passport requirements

## [0.4.0] - 2022-11-24
### Added
- a new script has been added. This brings the software closer to version 1.0.0. Although it requires a developer to
  run, the software will now run with the inputs we've defined and will give a clear answer.

## [0.3.0] - 2022-11-24
### Changed
- `Matching.report_pairs` now only returns a list of paired IDs

## [0.2.1] - 2022-11-24
### Added
- Enough code for a proof of concept
