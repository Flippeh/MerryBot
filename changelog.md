# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 2021-12-12
### Changed
- Moved "bingus" images to images/bingus/
- Fixed start.sh virtual environment creation
- Reworked bingus command to pull random file from images/bingus/
- on_message body changed significantly. Most was changing order to allow prefixed commands to execute
- Updated project file
- Added line in readme to new contributing guide
- Updated venv.sh to install 3.10.1
- Updated this file to reflect changes since [0.0.2]

### Added
- Created issue templates for bug reporting and feature request
- Wrote contributing.md files
- Github workflows should now work for pylint and pytest
- Incorporated pylintrc file for pylint
- Testing folder with dummy pytest file for now. This will be further added to in a later code rewrites.

### Removed
- Removed "hi-ya" and "hallo" from interjections
- Removed duplicate project file.

## [0.0.3-dev] - 2021-10-22
### Changed
- Moved "bingus" images to images/bingus/
- Fixed start.sh virtual environment creation
- Reworked bingus command to pull random file from images/bingus/
- on_message body changed significantly. Most was changing order to allow prefixed commands to execute

### Added
- Client now handles and signs out when sigint is sent to the process
- Added command not found error exception handling
- Added new_bingus command to allow admins to add images from discord message attachments
- Added power command, preface to fill power cycle functions. reboot not yet supported

### Removed
- Removed "hi-ya" and "hallo" from interjections

## [0.0.2] - 2021-10-14
### Changed
- Restructured project to organize images, code, and project config files

### Added
- Created .gitignore
- Created changelog.md
- Created readme.md
- Added GNU GPLv3 license -> license.md
- Added requirements.txt

## [0.0.1] - 2021-10-14
### Init
- Branch created from main
