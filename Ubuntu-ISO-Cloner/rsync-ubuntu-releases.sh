#/bin/bash

fatal() {
  echo "$1"
  exit 1
}

warn() {
  echo "$1"
}

# Define where you want the mirror-data to be on your mirror
BASEDIR=/path/to/save/isos

if [ ! -d ${BASEDIR} ]; then
  fatal "Save destination does not exist"
fi

rsync --verbose --times --stats --recursive --delete-after -h rsync://us.rsync.releases.ubuntu.com/releases/.pool/*.04*{server,desktop}*amd64.iso ${BASEDIR} || fatal "Failed to rsync from ${RSYNCSOURCE}."

# Ubuntu suggests release mirrors to check every four hours, for example:
# 0 */4 * * * "/path/to/rsync-ubuntu-releases.sh" > /dev/null
