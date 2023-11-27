import FileProcessor


class CSVPacketChecker:
    def __init__(self, file_name, dash):
        with open(file_name, 'r') as input_file:
            firewall = dash.get_firewall()
            results = FileProcessor.check_csv_packet(input_file, firewall)
            input_file.seek(0)
            input_file = FileProcessor.parse_csv(input_file)
            with open(file_name, 'w') as output_file:
                FileProcessor.combine_two_list_to_csv(input_file, output_file, results)
                output_file.close()
