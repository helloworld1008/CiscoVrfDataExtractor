#! /usr/bin/env python

import re, argparse, os, sys, textwrap

""" Argument parsing """

parser = argparse.ArgumentParser(usage='%(prog)s [options]', formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=textwrap.dedent('''\
                                 description: A utility that extracts all VRF information
                                              from a cisco config file'''), epilog=' ')

parser.add_argument("-f", "--file", help="cisco vrf config file", required=True)

args = parser.parse_args()

input_file = vars(args)['file']

""" Check whether file exists and has read permissions """

if not os.access(input_file, os.F_OK):

	print "The file {0} does not exist\n".format(input_file)

	sys.exit(1)

if not os.access(input_file, os.R_OK):

	print "The file {0} does not have read permissions\n".format(input_file)

	sys.exit(1)


""" Regex objects for pattern matching """

vrf_name_regex_obj = re.compile("^vrf (.*)?$")
vrf_desc_regex_obj = re.compile(" *?description (.*)?$")
addr_family_regex_obj = re.compile(" *?address-family (.*)?$")
import_rt_regex_object = re.compile(" *?import route-target.*$")
export_rt_regex_object = re.compile(" *?export route-target.*$")
extended_comm_regex_object = re.compile("^ *?(\d+\:\d+) *$")
exclamation_regex_object = re.compile("^( *)?(!)( *)?$")



""" Function to initialize vrf dictionary """

def init_vrf_dict():

	global vrf_dict

	vrf_dict = {'vrf_name': '', 'description': '', 'address_family': {'ipv4_unicast': {'import_RTs': [], 'export_RTs': []}, 'ipv6_unicast': {'import_RTs': [], 'export_RTs': []}}}


""" Function to write to file """

def write_to_file():

	global output_file_object, vrf_dict

	output_file_object.write(vrf_dict['vrf_name'] + "," + vrf_dict['description'] + "," + ';'.join(vrf_dict['address_family']['ipv4_unicast']['import_RTs']) + "," + ';'.join(vrf_dict['address_family']['ipv4_unicast']['export_RTs']) + "," + ';'.join(vrf_dict['address_family']['ipv6_unicast']['import_RTs']) + "," + ';'.join(vrf_dict['address_family']['ipv6_unicast']['export_RTs']) + "\n") 

""" Initialize vrf dictionary """

init_vrf_dict()


""" Initialize output file and add first line """

output_file_object = open('/tmp/vrfdata.csv', 'w')
output_file_object.write("vrf_name,vrf_description,ipv4_RT_import,ipv4_RT_export,ipv6_RT_import,ipv6_RT_export\n")

for line in open(input_file):

	if vrf_name_regex_obj.match(line) is not None:

		if vrf_dict['vrf_name'] != '':

			write_to_file()
			init_vrf_dict()


		vrf_dict['vrf_name'] = vrf_name_regex_obj.match(line).group(1)
		continue	

	if vrf_desc_regex_obj.match(line) is not None:

		vrf_dict['description'] = vrf_desc_regex_obj.match(line).group(1)
		continue

	if addr_family_regex_obj.match(line) is not None:

		if addr_family_regex_obj.match(line).group(1) == 'ipv4 unicast':

			ipv4_flag = 1
			ipv6_flag = 0
			continue

		if addr_family_regex_obj.match(line).group(1) == 'ipv6 unicast':

			ipv6_flag = 1
			ipv4_flag = 0
			continue

	if import_rt_regex_object.match(line) is not None:

		import_rt_flag = 1
		export_rt_flag = 0
		continue

	if export_rt_regex_object.match(line) is not None:

		export_rt_flag = 1
		import_rt_flag = 0
		continue

	if extended_comm_regex_object.match(line) is not None:

		if import_rt_flag == 1 & ipv4_flag == 1:

			vrf_dict['address_family']['ipv4_unicast']['import_RTs'].append(extended_comm_regex_object.match(line).group(1))

			continue

		if export_rt_flag == 1 and ipv4_flag == 1:

			vrf_dict['address_family']['ipv4_unicast']['export_RTs'].append(extended_comm_regex_object.match(line).group(1))

			continue

		if import_rt_flag == 1 & ipv6_flag == 1:

			vrf_dict['address_family']['ipv6_unicast']['import_RTs'].append(extended_comm_regex_object.match(line).group(1))
			continue

		if export_rt_flag == 1 and ipv6_flag == 1:

			vrf_dict['address_family']['ipv6_unicast']['export_RTs'].append(extended_comm_regex_object.match(line).group(1))
			continue




write_to_file()

print "\nPlease refer /tmp/vrfdata.csv file for output\n"
