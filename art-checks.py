#!/usr/local/bin/python3

# This is a script to process ARTRollOut data to compare against the care continuum data for Miami:
# HIV INTEGRATED EPIDEMIOLOGICAL PROFILE, Florida, 2019

import sys
import os

# For numerical computation
import numpy as np

# Plotting requirements!
import matplotlib.pyplot as plt


class QoI:
    """ QoI is a generic class for quantities of interest such as: Number of Infected, Number of Detected, ...

     QoI structure:                        | Gender  | Orientation  | Ethnicity                |
     Corresponding indices from QoI_data:  | [0],[1] | [2],[3],[4]  | [5],[6],[7],[8],[9],[10] |
    """

    def __init__(self, QoI_data):
        self.__gender = Genders(QoI_data[0:2])
        self.__orientation = Orientations(QoI_data[2:5])
        self.__ethnicity = Ethnicities(QoI_data[5:11])

    # Public methods!:
    def get_total_number(self):
        """ Get total number of people in this QoI which is the sum of its gender stratification """
        return self.__gender.sum()

    # Getters methods:
    def get_gender(self):
        """ Returns the gender: list[2] """
        return self.__gender

    def get_orientation(self):
        """ Returns the orientations: list[3] """
        return self.__orientation

    def get_ethnicities(self):
        """ Returns the ethnicities: list[6] """
        return self.__ethnicity

    def get_demographic(self, demographic):
        """ This is a user selected method to output a given demographic data """
        if demographic == "WHITE":
            return self.__ethnicity.get_whites()
        elif demographic == "BLACK":
            return self.__ethnicity.get_blacks()
        elif demographic == "HISPANIC":
            return self.__ethnicity.get_hispanics()
        elif demographic == "OTHER":
            return self.__ethnicity.get_other_races()
        elif demographic == "TOTAL":
            return self.__gender.sum()  # This is same as get_total_number() function in this class
        else:
            print('Demographic name ', demographic, ' is not defined! \n')
            return


class Genders:
    """ Basic class for genders that initialize with a list of two element
    Gender Structure: | Male | Females |
    """

    def __init__(self, gender_data):
        assert (len(gender_data) == 2)  # Confirm the size
        self.males = gender_data[0]
        self.females = gender_data[1]

    # Getters public methods!
    def get_males(self):
        return self.males

    def get_females(self):
        return self.females

    def sum(self):
        """ Sum of males and females = total numbers """
        return self.males + self.females


class Orientations:
    """ Basic class for Orientations that initialize with a list of three elements
    Orientations Structure: | male:MSM | male:MSMW | male:MSW |"""

    def __init__(self, orientation_data):
        assert (len(orientation_data) == 3)  # Confirm the size
        self.__MSM = orientation_data[0]
        self.__MSMW = orientation_data[1]
        self.__MSW = orientation_data[2]

    # Getters methods
    def get_MSM(self):
        """ return number of Males have sex with biological males (MSM) """
        return self.__MSM

    def get_MSMW(self):
        """ return number of males have sex with both biological genders (MSMW) """
        return self.__MSMW

    def get_MSW(self):
        """ return number of males have sex with biological females (MSW) """
        return self.__MSW


class Ethnicities:
    """ # Basic class for Ethnicities that initialize with a list of six elements
    Orientations Structure: | BLACK:NON_HISPANIC | BLACK:HISPANIC| WHITE:NON_HISPANIC | WHITE:HISPANIC | OTHER:NON_HISPANIC | OTHER:HISPANIC |
    """

    def __init__(self, ethnicity_data):
        assert (len(ethnicity_data) == 6)  # Confirm the size
        self.__BLACK_NON_HISPANIC = ethnicity_data[0]
        self.__BLACK_HISPANIC = ethnicity_data[1]
        self.__WHITE_NON_HISPANIC = ethnicity_data[2]
        self.__WHITE_HISPANIC = ethnicity_data[3]
        self.__OTHER_NON_HISPANIC = ethnicity_data[4]
        self.__OTHER_HISPANIC = ethnicity_data[5]

    # Getters methods
    def get_whites(self):
        """ Get the numbers for population of whites """
        return self.__WHITE_NON_HISPANIC

    def get_blacks(self):
        """ Get the numbers for population of blacks """
        return self.__BLACK_NON_HISPANIC

    def get_other_races(self):
        """ Get the numbers for other population """
        return self.__OTHER_NON_HISPANIC

    def get_hispanics(self):
        """ Get the numbers for population of hispanics """
        return self.__BLACK_HISPANIC + self.__WHITE_HISPANIC + self.__OTHER_HISPANIC


class Node:
    """ This is a class stores data of each row (by month) in ARTRollout file
        Right now outputs to be considered: 1) Number of Infected 2) Number of Detected
                                            3) Number In Care     4) Number of New Diagnosis
                                            5) Number with Suppressed VL

    NOTE: Anytime there is a new output this class has to be modified
    """

    def __init__(self, row_month_data):
        # Construct the object with row data
        self.__time = row_month_data[0]  # This is the time step = one month!
        self.population = row_month_data[1]
        self.infected = QoI(row_month_data[6:17])
        self.detected = QoI(row_month_data[17:28])
        self.in_care = QoI(row_month_data[28:39])
        self.new_diagnosis = QoI(row_month_data[39:50])
        self.enrolled_in_30 = QoI(row_month_data[50:61])
        self.suppresed_VL = QoI(row_month_data[61:72])

    # Getters methods
    def get_year_of_month(self, time):
        """ Get this Node's year count """
        return int(time / 12)

    def isItDecember(self):
        """ Check whether if this Node is the end of calender year """
        return self.get_time_in_year() == self.__time / 12.0

    def get_time_in_year(self):
        """ Returns the time as the year: (e.g. end of month 12th = Year 1, end of month 24th = Year 2, ...) """
        return int(self.__time / 12)

    def get_year(self, year, month):
        """  Returns the calender year given a time step (month) and the year
        Example: If the year 1990 is 600th time step (month) therefore this should return end of 12th time step as year
        1941, and end of 24th month as 1942, ...
        """
        return year - (self.get_year_of_month(month) - self.get_time_in_year())


class NodeYearly:
    """This is a similar class to the Node class instead it stores yearly aggregated data (in each row). """

    def __init__(self, year, infected, detected, in_care, new_diagnosis, enrolled_in_30, suppresed_VL):
        self.year = year  # this year!
        self.infected = infected
        self.detected = detected
        self.in_care = in_care
        self.new_diagnosis = new_diagnosis
        self.enrolled_in_30 = enrolled_in_30
        self.suppresed_VL = suppresed_VL

    # Getters methods:
    def get_precent_incare(self):
        """ Returns the percentage of people in care this year """
        return self.in_care / self.detected

    def get_precent_suppressed(self):
        """ Returns the percentage of people with suppressed VL this year """
        return self.suppresed_VL / self.detected

    def get_precent_care_within30(self):
        """ Returns the percentage of people in care within 30 days this year """
        return self.enrolled_in_30 / (self.new_diagnosis + 0.0001)


# Global functions:
def parse_data_line(line_str):
    """ Parses the data """
    result_list = [int(i) for i in line_str.split() if i.isdigit()]
    return result_list


def reduce_digits(float_num):
    """ This is it to roundup float numbers to two floating digits """
    return format(round(float_num, 2), '.2f')  # First round up and then return a STRING!


def compare(simulated, baseline):
    """ Compare the simulated to the baseline reported values
    anything between the baseline +/- 10% of baseline is accepted
    """
    if baseline + 0.1 * baseline > simulated > baseline - 0.1 * baseline:
        return True
    else:
        return False


def perform_all_checks(nodal_table_element, year_baselines):
    """
    This functions perform checks by taking the simulated data of a year and compare to the baseline data
    :param nodal_table_element: table of nodal elements per year
    :param year_baselines: table of baselines
    :return: [str (PASS/FAIL),  numerics]
    """
    # Check number in care
    if compare(nodal_table_element.get_precent_incare(), year_baselines[0]):
        in_care_check = ["PASS", nodal_table_element.get_precent_incare()]
    else:
        in_care_check = ["FAIL", nodal_table_element.get_precent_incare()]

    # Check number with suppressed VL
    if compare(nodal_table_element.get_precent_suppressed(), year_baselines[1]):
        suppressed_VL_check = ["PASS", nodal_table_element.get_precent_suppressed()]
    else:
        suppressed_VL_check = ["FAIL", nodal_table_element.get_precent_suppressed()]

    # Check number in care within 30 days
    if compare(nodal_table_element.get_precent_care_within30(), year_baselines[2]):
        within_30_check = ["PASS", nodal_table_element.get_precent_care_within30()]
    else:
        within_30_check = ["FAIL", nodal_table_element.get_precent_care_within30()]

    # Return the outcome both PASS/FAIL and numerics (the simulated numbers)
    # Eeach element of this list contains list of two elements [0] is a string: PASS or FAIL [1] is the simulated
    return [in_care_check, suppressed_VL_check, within_30_check]


def plotting(all_data, filename, file_format, x_label, y_label):
    """ Plotting all the runs in a single plot"""
    years = np.array([2014, 2015, 2016, 2017, 2018, 2019])
    fig = plt.figure()
    for i in range(0, len(all_data) - 1):  # Loop through all the simulated data
        year_data = all_data[i][0:6]  # for 2014 to 2019 data stored
        plt.plot(years, year_data, '--', linewidth=0.5, color='tab:gray')

    # Make the Numpy array out of list for creating confidence intervals
    baseline_arr = np.array(all_data[len(all_data) - 1][0:6])
    baseline_upper_interval = baseline_arr * (1.1)  # 10% percent upper interval
    baseline_lower_interval = baseline_arr * (0.9)  # 10% percent lower interval

    # The last in the data list is the baseline so plot it with different coloring!
    plt.plot(years, all_data[len(all_data) - 1][0:6], 'bo-', linewidth=1.5)
    # Fill the plots between upper and lower intervals!
    plt.fill_between(years, baseline_upper_interval, baseline_lower_interval, color='tab:blue', alpha=0.1)

    # Put the axis the labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # Save it in a file!
    plt.savefig(filename + '.' + file_format, format=file_format, dpi=1200)


# Care Continuum (baseline) data from 2014 to 2019 for total population
#
# year    in_care    suppressed_VL    in_care_within_30
# 2014     0.67           0.52            0.64
# 2015     0.68           0.57            0.68
# 2016     0.70           0.59            0.70
# 2017     0.71           0.60            0.79
# 2018     0.72           0.62            0.84
# 2019     0.73           0.62            0.85
#
# Note: The these numbers are entered manually in the following check procedure
year_2014 = [0.67, 0.52, 0.64]
year_2015 = [0.68, 0.57, 0.68]
year_2016 = [0.70, 0.59, 0.70]
year_2017 = [0.71, 0.60, 0.79]
year_2018 = [0.72, 0.62, 0.84]
year_2019 = [0.73, 0.62, 0.85]

# Main Program!
if __name__ == '__main__':

    # Command arguments:
    # Variables have "arg_" prefix showing the values are taken from the command line arguments:
    #
    # ~$: python3 ARTCheckAnalysis <arg_year> <arg_month> <arg_path_to_batch> <arg_demographics>
    #
    #   first: arg_year) is the year and the (e.g. 1990)
    #   second: arg_month) is the time step that corresponds to that year (e.g. 600)
    #   third: arg_path_to_batch) is path to the batch results giving the current path (e.g results/)
    #   fourth: arg_demographics) is a string to show the specific demographic: WHITE, BLACK, HISPANIC, OTHER, TOTAL
    # Default arguments if nothing entered
    arg_year = int(sys.argv[1])
    arg_month = int(sys.argv[2])
    arg_path_to_batch = sys.argv[3]
    arg_demographics = sys.argv[4]
    if len(sys.argv) != 5:
        print("Err: Not enough command argument!")
    if arg_demographics != "WHITE" or arg_demographics != "BLACK" or \
            arg_demographics != "HISPANIC" or arg_demographics != 'OTHER':
        print("Err: Wrong demographics!")
    if arg_demographics != 'TOTAL':
        print("WARNING: The Pass/Fail checks are only done against total numbers:")
        print("TO BE IMPLEMENTED BASED ON DEMOGRAPHICS LATER")

    # Creating the check summary files
    passfail_filename_str = 'check_summary_passfail_'+arg_demographics+'.txt'
    numerics_filename_str = 'check_summary_numerics_'+arg_demographics+'.txt'
    f1 = open(passfail_filename_str, 'w')
    f2 = open(numerics_filename_str, 'w')

    # Containers for plotting
    all_checks_incare = []
    all_checks_suppvl = []
    all_checks_thirty = []

    # These loops walk through all directories finding ARTRollout files starting from wherever this script is saved
    for root, dirs, files in os.walk(arg_path_to_batch):
        for file in files:

            # This condition makes sure it only takes ARTRollout excel files
            if file.endswith('.xls') and file.__contains__("ARTRollout"):
                file_name_with_path = os.path.join(root, file)

                print('Extracting data from file:', file_name_with_path)

                # FIRST: print out the corresponding filename
                f1.write(file + "\n")  # Pass/Fail outputs
                f2.write(file + "\n")  # Numerics outputs

                # The excel file is being read as a text file. (Due to errors during opening with 'xlrd' and 'openpyxl')
                fileArtRoll = open(file_name_with_path, "r")
                fileLines = fileArtRoll.readlines()

                # Initialize the structure
                nodal_data = []

                # start reading through the file line by line
                line_count = 0
                for line in fileLines:

                    # Take the first line of data
                    if line_count == 4:
                        all_data = parse_data_line(line.strip())
                        nodal_data.append(Node(all_data))

                    # Add rows and complete the dataset
                    elif line_count > 4:
                        row_data = parse_data_line(line.strip())
                        all_data = np.vstack([row_data, row_data])
                        nodal_data.append(Node(row_data))

                    # Go to next line!
                    line_count += 1

                # Initialize the lists and variables for yearly data table
                nodal_table = []
                newdiag = 0
                newenroll = 0

                # Create the yearly data table
                # TODO: It discounts the last two months of simulation
                for i in range(0, len(nodal_data) - 4):  # Forgets the last two months of the simulation

                    # Keep adding new diagnosis and enrolled within 30 days until year ends
                    newdiag = newdiag + nodal_data[i].new_diagnosis.get_demographic(arg_demographics)
                    newenroll = newenroll + nodal_data[i].enrolled_in_30.get_demographic(arg_demographics)

                    # if it's the end of the year push data
                    if nodal_data[i].isItDecember():
                        # if it's december continue for the next two months (End of Feb) but save it for this year
                        # Have to do it manually for new diagnosis and new enrollement (within 30 days)
                        for j in range(1, 3):
                            newdiag = newdiag + nodal_data[i + j].new_diagnosis.get_demographic(arg_demographics)
                            newenroll = newenroll + nodal_data[i + j].enrolled_in_30.get_demographic(arg_demographics)

                        # And can easily call i+2 of the nodal_data
                        nodal_table.append(
                            NodeYearly(nodal_data[i + 2].get_year(arg_year, arg_month),
                                       nodal_data[i + 2].infected.get_demographic(arg_demographics),
                                       nodal_data[i + 2].detected.get_demographic(arg_demographics),
                                       nodal_data[i + 2].in_care.get_demographic(arg_demographics),
                                       newdiag, newenroll, nodal_data[i + 2].suppresed_VL.get_demographic(arg_demographics)))

                        # reset new diagnosis and enrolled in 30 days for next year
                        newdiag = 0
                        newenroll = 0

                #  Write out the header!
                f1.write('Year\t In Care%\t Suppr. VL%\t In Care in 30 days% \n')
                f2.write('Year\t In Care%\t Suppr. VL%\t In Care in 30 days% \n')

                # Only checks against years 2014, 2015, 2016, 2017, 2018 and 2019
                checks_2014 = []
                checks_2015 = []
                checks_2016 = []
                checks_2017 = []
                checks_2018 = []
                checks_2019 = []

                # First loop through all of the yearly data!
                for i in range(0, len(nodal_table)):
                    # Perform Checks!

                    # 2014 Checks!
                    if nodal_table[i].year == 2014:
                        checks_2014 = perform_all_checks(nodal_table[i], year_2014)

                        # First outputs the Pass/Fail outputs
                        f1.write("2014:\t " + checks_2014[0][0] + "\t\t" + checks_2014[1][0] + "\t\t" +
                                 checks_2014[2][0] + "\n")

                        # Then outputs the numerics
                        f2.write("2014:\t " + reduce_digits(checks_2014[0][1]) + "\t\t" +
                                 reduce_digits(checks_2014[1][1]) + "\t\t" + reduce_digits(checks_2014[2][1]) + "\n")

                    # 2015 Checks!
                    if nodal_table[i].year == 2015:
                        checks_2015 = perform_all_checks(nodal_table[i], year_2015)

                        # First outputs the Pass/Fail outputs
                        f1.write("2015:\t " + checks_2015[0][0] + "\t\t" + checks_2015[1][0] + "\t\t" +
                                 checks_2015[2][0] + "\n")

                        # Then outputs the numerics
                        f2.write("2015:\t " + reduce_digits(checks_2015[0][1]) + "\t\t" +
                                 reduce_digits(checks_2015[1][1]) + "\t\t" + reduce_digits(checks_2015[2][1]) + "\n")

                    # 2016 Checks!
                    if nodal_table[i].year == 2016:
                        checks_2016 = perform_all_checks(nodal_table[i], year_2016)

                        # First outputs the Pass/Fail outputs
                        f1.write("2016:\t " + checks_2016[0][0] + "\t\t" + checks_2016[1][0] + "\t\t" +
                                 checks_2016[2][0] + "\n")

                        # Then outputs the numerics
                        f2.write("2016:\t " + reduce_digits(checks_2016[0][1]) + "\t\t" +
                                 reduce_digits(checks_2016[1][1]) + "\t\t" + reduce_digits(checks_2016[2][1]) + "\n")

                    # 2017 Checks!
                    if nodal_table[i].year == 2017:
                        checks_2017 = perform_all_checks(nodal_table[i], year_2017)

                        # First outputs the Pass/Fail outputs
                        f1.write("2017:\t " + checks_2017[0][0] + "\t\t" + checks_2017[1][0] + "\t\t" +
                                 checks_2017[2][0] + "\n")

                        # Then outputs the numerics
                        f2.write("2017:\t " + reduce_digits(checks_2017[0][1]) + "\t\t" +
                                 reduce_digits(checks_2017[1][1]) + "\t\t" +
                                 reduce_digits(checks_2017[2][1]) + "\n")

                    # 2018 Checks!
                    if nodal_table[i].year == 2018:
                        checks_2018 = perform_all_checks(nodal_table[i], year_2018)

                        # First outputs the Pass/Fail outputs
                        f1.write("2018:\t " + checks_2018[0][0] + "\t\t" + checks_2018[1][0] + "\t\t" +
                                 checks_2018[2][0] + "\n")

                        # Then outputs the numerics
                        f2.write("2018:\t " + reduce_digits(checks_2018[0][1]) + "\t\t" +
                                 reduce_digits(checks_2018[1][1]) + "\t\t" + reduce_digits(checks_2018[2][1]) + "\n")

                    # 2019 Checks!
                    if nodal_table[i].year == 2019:
                        checks_2019 = perform_all_checks(nodal_table[i], year_2019)

                        # First outputs the Pass/Fail outputs
                        f1.write("2019:\t " + checks_2019[0][0] + "\t\t" + checks_2019[1][0] + "\t\t" +
                                 checks_2019[2][0] + "\n")

                        # Then outputs the numerics
                        f2.write("2019:\t " + reduce_digits(checks_2019[0][1]) + "\t\t" +
                                 reduce_digits(checks_2019[1][1]) + "\t\t" + reduce_digits(checks_2019[2][1]) + "\n")

                # Appending numerics for plotting
                all_checks_incare.append([checks_2014[0][1], checks_2015[0][1],
                                          checks_2016[0][1], checks_2017[0][1],
                                          checks_2018[0][1], checks_2019[0][1], file])

                all_checks_suppvl.append([checks_2014[1][1], checks_2015[1][1],
                                          checks_2016[1][1], checks_2017[1][1],
                                          checks_2018[1][1], checks_2019[1][1], file])

                all_checks_thirty.append([checks_2014[2][1], checks_2015[2][1],
                                          checks_2016[2][1], checks_2017[2][1],
                                          checks_2018[2][1], checks_2019[2][1], file])

                # End of loop through yearly data

                f1.write("\n")  # Next line for next result's file data (PASS/FAIL)
                f2.write("\n")  # Next line for next result's file data (Numerics)

            # End of IF condition to check whether it finds ART file!

        # End of loop through ART Excel files

    f1.close()  # End of file (PASS/FAIL)
    print("Pass/Fail file created!")

    f2.close()  # End of file (Numerics)
    print("Numerics file created!")

    # Plotting all of the simulated data

    # Adding (the last item in the list) the base line to all of data before sending for plotting
    all_thirty = all_checks_thirty
    all_thirty.append([year_2014[2], year_2015[2], year_2016[2], year_2017[2], year_2018[2], year_2019[2]])
    all_incare = all_checks_incare
    all_incare.append([year_2014[0], year_2015[0], year_2016[0], year_2017[0], year_2018[0], year_2019[0]])
    all_suppvl = all_checks_suppvl
    all_suppvl.append([year_2014[1], year_2015[1], year_2016[1], year_2017[1], year_2018[1], year_2019[1]])

    # Now sending for plotting specifying filename, format, xlabel, ylabel
    print("Generating plots...")

    plotting(all_thirty, 'in_care_within30', 'pdf', 'Year', 'In Care Within 30 Days%')
    plotting(all_incare, 'in_care', 'pdf', 'Year', 'In Care%')
    plotting(all_suppvl, 'supp_vl', 'pdf', 'Year', 'Suppressed Vl%')

    # Finishing!
    print("Done!")
