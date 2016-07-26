#!/bin/bash
function usage()
{
  cat << EOF
  usage: $0 options

  You can use this script to run mySQL / mariadb queries against the database.
  Basically it does the same as mysql_secure_installation, but can be used with parameters.

  OPTIONS:
     -h         show this help screen
     --pw       the password to use for root
     --query    the query to run
     -x         for debugging purposes only

EOF
  exit 0

}

while [ -n "$1" ]; do
case $1 in
  -h)       usage; exit 0 ;;
  --pw)     PW=$2 ; shift 2 ;;
  --query)  QRY=$2 ; shift 2 ;;
  -x)       set -vx ; shift 1 ;;
  *)        echo "invalid parater $1"; usage; exit 1 ;;
esac
done

mysql --password="$PW" -e "$QRY"
