# CiscoVrfDataExtractor
CiscoVrfDataExtractor is a python-based utility to extract VRF details from a Cisco ASR series router and dump them into a csv file. It extracts the following details:

- VRF name
- VRF description
- RT import values for IPv4 address family
- RT export values for IPv4 address family
- RT import values for IPv6 address family
- RT export values for IPv6 address family

## Requirements
Linux machine with python 2.7 installed

## How to use
Create a file and copy the VRF definition section from the Cisco ASR series router configuration to this file

```
$ touch VrfConfig
```
