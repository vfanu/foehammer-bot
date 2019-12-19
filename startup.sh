#!/bin/sh
echo "Starting vpnbot .... "
printenv
mkdir /root/.aws
echo "[default]" >> /root/.aws/credentials

creds_found="false"

if [[ -n $AWS_ACCESS_ID ]] && [[ -n $AWS_SECRET_KEY ]]; then
  echo "aws_access_key_id = $AWS_ACCESS_ID" >> /root/.aws/credentials
  echo "aws_secret_access_key = $AWS_SECRET_KEY" >> /root/.aws/credentials
  creds_found="true"
fi

if [[ $creds_found == "true" ]]; then

  cd /python
  python vpnbot.py

else
  echo "AWS access creds not found."
fi

