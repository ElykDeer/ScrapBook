#/bin/bash

fatal() {
  echo "$1"
  exit 1
}

BASEDIR=rsync://us.rsync.releases.ubuntu.com/releases/.pool/

# Define where you want the mirror-data to be on your mirror
SAVEDIR=/path/to/save/isos/in

if [ ! -d ${SAVEDIR} ]; then
  fatal "Save destination does no exist"
fi


# Adjust hopw many files we want
FILES=$(rsync --list-only ${BASEDIR}*.04*{server,desktop}*amd64.iso . | sed -n -e 's/^.* \(\S*\)$/\1/p' | sort -n | tail -6)

for FILENAME in ${FILES}
do
  echo ${BASEDIR}${FILENAME}
  rsync --verbose --times --stats --recursive --delete-after -h --progress ${BASEDIR}${FILENAME} ${SAVEDIR} || fatal "Failed to rsync from ${RSYNCSOURCE}."
done

# Ubuntu suggests release mirrors to check every four hours, for example:
# 0 */4 * * * /root/rsync-ubuntu-releases.sh > /root/rsync-ubuntu-releases.log
