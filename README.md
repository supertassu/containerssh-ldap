# containerssh-ldap

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

[ContainerSSH](https://containerssh.io) (v0.4) authentication server that
authenticates users with SSH keys stored in LDAP.

## Setup

Use the included example config file, suit it to your needs, and mount it on the
container at `/config.yaml` (or use the CONTAINERSSH_LDAP_CONFIG env variable to
change the location). 

## Security

This is very experiemental. I wouldn't use it on a production enviroment.

If you find a security issue, please [contact me](https://taavi.wtf/#contact).
Thank you.
