# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- calculating a score for a role that offers "ALL" skills has changed, and now offers X points


## [0.13.3] - 2023-07-10
### Changed
- separated out matching and specialism packages to more clearly differentiate between the two
- updated README with slightly clearer instructions on extension


## [0.13.2] - 2023-05-11
### Changed
- Candidates with accessibility requirements can't be matched with roles that can't meet those requirements

## [0.13.1] - 2023-04-12
### Changed
- Candidates who've previously relocated are more likely to get their first or second choice of location

## [0.13.0]
### Changed
- the system now shuffles the Candidates and Roles before matching them
- the script `pairing_script` now takes an optional `iterations` argument. I recommend more than 10 to get a really
  good spread of results
-
### Added
- the system generates some management information about the best iteration

## [0.12.2]
### Added
- support for secondments, which are treated as a cohort

### Changed
- roles that are suitable for Y2 are assumed to be suitable as secondments (needs verifying with users)


## [0.10.0] - 2023-02-09
## Added
- This adds support for the particulars of scoring the SEFS specialism

## [0.9.0] - 2023-02-06
### Changed
- so much has changed. The API of `Pair` has changed significantly, but because I've not yet put out a stable
  version I am happy leaving this as a minor version. It will also show me who else is using this library and
  whether they're reading the changelog
- `Pair` no longer takes a candidate and role when instantiated. Instead, those are passed to `score_pair`, which
  renders the name `Pair` slightly moot. This is because naming things is hard.

## [0.8.0] - 2023-01-31
- Welcome back!
### Changed
- inputs to `Candidate` objects must now include args `last_role_main_skill` and `last_role_secondary_skill`
- this supports a change to the scoring mechanism for skills, which disqualifies a match where the main skill would
  be the same as it was in the candidate's previous role
- matches where the secondary skill would be the same as the previous role's secondary skill are also penalised, but
  not disqualified

## [0.7.4] - 2022-12-30
### Changed
- `Pair` now disqualifies scores below 20. This is currently hard-coded but will be altered in a future release

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
