## Welcome to the FoeHammer DVPN Project! ##

The idea behind this project is let anyone create a VPN server via the medium of a Slack bot.

## Getting Started ##
Well, well, well then. If you've come this far then you probably want to make a VPN server so lets get started. 

1) Create some resources as outlined here (https://github.com/vfanu/dragonvpn-community-Infra)

2) In Slack create an app. In basic info select 'Bots' to create a bot app and call it FoeHammer. Add the new bot user and install 
it in the workspace. In OAuth and Permissions jot down the oauth token.

3) Login to dockerhub or build the docker container.

3) Execute this command and provide real values for aws_secret_key, aws_access_id and slack_token : 
docker run -e "AWS_SECRET_KEY=<my_aws_secret_key>" -e "AWS_ACCESS_ID=<my_access_id>" -e "SLACK_TOKEN=<my_slack_token>" vfa/slack-dvpn:arm64-1.1

4) Enjoy!
