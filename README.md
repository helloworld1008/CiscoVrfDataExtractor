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
$ cat VrfConfig
vrf Customer_A
 description **VRF for customer A - Platinum**  
 address-family ipv4 unicast
  import route-target
   10101:15003
   10101:16102
   10101:16106
   10101:16109
  !
  export route-target
   10101:15003
  !
 !
!

vrf Customer_B
 description "VRF for customer B - Gold"
 address-family ipv6 unicast
  import route-target
   10101:17138
  !
  export route-target
   10101:17138
  !
 !
!

vrf Customer_C
 description "VRF for customer C - Silver"
 address-family ipv4 unicast
  import route-target
   10101:12629
  !
  export route-target
   10101:12629
  !
 !
 address-family ipv6 unicast
  import route-target
   10101:12629
  !
  export route-target
   10101:12629
  !
 !
!
$

```
Download this script to your system and give it execute permissions
```
$ chmod 755 CiscoVrfDataExtractor.py
```
