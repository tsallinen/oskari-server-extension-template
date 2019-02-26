#!/bin/sh

set -e

RPMBUILD_CMD=/usr/bin/rpmbuild
if [ ! -x $RPMBUILD_CMD ]; then
  echo "$RPMBUILD_CMD not found, skipping rpm packaging."
  exit -1
fi

DIRECTORY=$(cd `dirname $0` && pwd)
RPM_TOPDIR=$DIRECTORY/rpm

POM_VERSION=$(xmlstarlet sel -t -v "/_:project/_:version" $(dirname "$DIRECTORY")/pom.xml)
VERSION=$POM_VERSION
RELEASE=1

# If the maven version ends with SNAPSHOT, replace release version with timestamp
if [[ $VERSION =~ .*-SNAPSHOT ]]; then
   VERSION=${VERSION%"-SNAPSHOT"}
   # Prefix timestamp with 0. to make it always < release versions (1,2,3..)
   RELEASE=0.$(date '+%Y%m%d%H%M%S')
fi

echo "POM version: $POM_VERSION"
echo "RPM version: $VERSION-$RELEASE"

function buildRpm() {
   rpmbuild \
     -bb \
     --define "_topdir $RPM_TOPDIR" \
     --define "ver $VERSION" \
     --define "rel $RELEASE" $RPM_TOPDIR/SPECS/$1
}

buildRpm "oskari-jetty.spec"
buildRpm "oskari-map-webapp.spec"
buildRpm "oskari-transport-webapp.spec"
