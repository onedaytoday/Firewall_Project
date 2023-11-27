import csv
import ipaddress
import Layer3Firewall
import io

import Packet


def parse_csv(file):
    output = list(csv.reader(file, delimiter=","))
    return output


def parse_packet(line):
    return Packet.Packet(
        srcport=line[0],
        source_ip=ipaddress.ip_address(line[1]),
        destination_ip=ipaddress.ip_address(line[2]),
        destport=line[3],
        protocol=line[4]
    )


def convert_csv_to_packets(file):
    parsed_file = parse_csv(file)
    output = []
    for line in parsed_file:
        new_packet = parse_packet(line)
        output.append(new_packet)
    return output


def combine_two_list_to_csv(input_file, output_file, col):
    writer = csv.writer(output_file)

    index = 0
    for row in input_file:
        row.append(col[index])
        writer.writerow(row)
        index += 1
    return writer


def check_csv_packet(file, firewall):
    packets = convert_csv_to_packets(file)
    results = firewall.filter_multiple(packets)
    return results

def check_and_add_results_to_csv(input_file, output_file, firewall):
    results = check_csv_packet(input_file, firewall)
    input_file.seek(0)
    combine_two_list_to_csv(input_file, output_file, results)
