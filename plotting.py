

def parse_data_line(line_str):
    """ Parses the data """
    result_list = [int(i) for i in line_str.split() if i.isdigit()]
    return result_list


if __name__ == '__main__':

    numericsFile = open('check_summary_numeric.txt', "r")
    numericsFileLines = numericsFile.readlines()

    data_lst = parse_data_line(numericsFileLines[4])