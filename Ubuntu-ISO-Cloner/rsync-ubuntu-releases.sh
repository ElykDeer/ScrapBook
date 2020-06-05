#/bin/bash

fatal() {
  echo "$1"
  exit 1
}

BASEDIR=rsync://us.rsync.releases.ubuntu.com/releases/.pool/

# Define where you want the mirror-data to be on your mirror
SAVEDIR=/path/to/save/dir

if [ ! -d ${SAVEDIR} ]; then
  fatal "Save destination does no exist"
fi

# Adjust per however many ISOs/versions you want
FILES=$(rsync --list-only ${BASEDIR}*.04*{server,desktop}*amd64.iso . | sed -n -e 's/^.* \(\S*\)$/\1/p' | sort -n | tail -6)

for FILENAME in ${FILES}
do
  # echo ${BASEDIR}${FILENAME}
  rsync --verbose --times --stats --recursive --delete-after -h --progress ${BASEDIR}${FILENAME} ${SAVEDIR} || fatal "Failed to rsync from ${RSYNCSOURCE}."
  echo ${SAVEDIR}${FILENAME} >> /tmp/rsync-ubuntu-releases.list
done

echo ""
echo "Removing old ISOs"
echo ""

for i in $SAVEDIR*; do
  if [[ $i == *ubuntu* ]] && ! grep -qxFe "$i" /tmp/rsync-ubuntu-releases.list; then
    echo "Deleting: $i"
    rm "$i"
    echo ""
  fi
done
rm /tmp/rsync-ubuntu-releases.list

echo "Done"

# Ubuntu suggests release mirrors to check every four hours, for example:
# 0 */4 * * * /path/to/rsync-ubuntu-releases.sh > /path/to/rsync-ubuntu-releases.log
