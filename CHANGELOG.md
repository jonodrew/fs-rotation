# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.1]

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
