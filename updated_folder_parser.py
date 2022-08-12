#This file will be able to take a file with many text files in it and go through each of them and parse their info


import os
import xlsxwriter
#import pandas as pd
import re

# This section can be un-commented for more optimized path
#AID PATH
#AWLU PATH
#path = r"Logs"
AWLU_path = r"AWLULogs"
AID_path = r"AIDLogs"
name = r"logFILEoutput.xlsx"

#Direct Paths for testing purposes
#path = "/Users/walkerbb2/Desktop/AWLU-Logs"
#path = r"C:\Users\walke\OneDrive\Desktop\new-txt-files"
#work_path = "/Users/walkerbb2/Desktop/"

#Moves the current working directory to the Logs folder in this case
#os.chdir(path)

#Adding excel file for data to be imported into
workbook = xlsxwriter.Workbook(name)
#workbook = xlsxwriter.Workbook("/Users/walkerbb2/Desktop/AWLU-export.xlsx")
#workbook = xlsxwriter.Workbook(r"C:\Users\walke\OneDrive\Desktop\logFILEoutput.xlsx")
# worksheet for all the parsed data
worksheet1 = workbook.add_worksheet('Data')

# create arrays for AID important variables
AID_signalStrengths = []
AID_upTime = []
AID_cellBand = []
AID_airportID = []
AID_tail_ID = []
AID_LRU_type = []
AID_average = []

# create arrays for AWLU important variables
AWLU_signalStrengths = []
AWLU_upTime = []
AWLU_cellBand = []
AWLU_airportID = []
AWLU_tail_ID = []
AWLU_LRU_type = []
AWLU_average = []

#Function that opens and prints file
def AID_parse(file_path):
    print("AID File Detected")
    # adding spreadsheet headings
    worksheet1.write(0, 1, 'AID DATA')
    worksheet1.write(1, 1, 'Signal Strength (dBm)')
    worksheet1.write(1, 2, 'Up Time (sec)')
    worksheet1.write(1, 3, 'Cell Band (MHz)')
    worksheet1.write(1, 5, 'Airport ID')
    worksheet1.write(1, 6, 'Tail ID')
    worksheet1.write(1, 7, 'Averages')

    # Set strings of what is being looked for
    AID_sigStr = "signalStrength"
    upTm = "upTime"
    cellBND = 'cellBand'
    sigIN = 'bytesRX'
    airID = 'airportID'

    with open(file_path, 'r') as log_file:
        lines = log_file.readlines()

        for line in lines:
            if AID_sigStr in line:
                # This messy section of code finds the value of the SIGNAL STRENGTH and only inputs the value into the array rather than random characters as well because the length of value changes (def could be easier by idk)
                index = (line.find(AID_sigStr))
                if line[index + 19].isalpha():
                    if line[index + 18].isalpha():
                        if line[index + 17].isalpha():
                            print("Not Found")
                        else:
                            AID_signalStrengths.append(line[index + 15:index + 17])
                    else:
                        AID_signalStrengths.append(line[index + 15:index + 18])
                else:
                    AID_signalStrengths.append(line[index + 15:index + 19])

                # signalStrengths.append(line[index+15:index+18])

                # This messy section of code finds the value of the UP TIMES and only inputs the value into the array rather than random characters as well because the length of value changes (def could be easier by idk)
                index = (line.find(upTm))
                if line[index + 11].isalpha():
                    if line[index + 10].isalpha():
                        if line[index + 9].isalpha():
                            if line[index + 8].isalpha():
                                print('Not Found')
                            else:
                                AID_upTime.append(line[index + 7:index + 8])
                        else:
                            AID_upTime.append(line[index + 7:index + 9])
                    else:
                        AID_upTime.append(line[index + 7:index + 10])
                else:
                    AID_upTime.append(line[index + 7:index + 11])

                # This messy section of code finds the value of the CELL BANDS and only inputs the value into the array rather than random characters as well because the length of value changes (def could be easier by idk)
                index = (line.find(cellBND))
                if line[index + 13].isalpha():
                    if line[index + 12].isalpha():
                        if line[index + 11].isalpha():
                            if line[index + 10].isalpha():
                                print('Not Found')
                            else:
                                AID_cellBand.append(line[index + 9:index + 10])
                        else:
                            AID_cellBand.append(line[index + 9:index + 11])
                    else:
                        AID_cellBand.append(line[index + 9:index + 12])
                else:
                    AID_cellBand.append(line[index + 9:index + 13])
                """
                # This messy section of code finds the value of the Tranfer Speed IN and only inputs the value into the array rather than random characters as well because the length of value changes (def could be easier by idk)
                index = (line.find(sigIN))
                if line[index + 13].isalpha():
                    if line[index + 12].isalpha():
                        if line[index + 11].isalpha():
                            if line[index + 10].isalpha():
                                print('Not Found')
                            else:
                                AID_cellBand.append(line[index + 9:index + 10])
                        else:
                            AID_cellBand.append(line[index + 9:index + 11])
                    else:
                        AID_cellBand.append(line[index + 9:index + 12])
                else:
                    AID_cellBand.append(line[index + 9:index + 13])
                """
            if airID in line:
                # This messy section of code finds the value of the AIRPORT ID and only inputs the value into the array rather than random characters as well because the length of value changes (def could be easier by idk)
                index = (line.find(airID))
                if line[index + 15].isalpha():
                    AID_airportID.append(line[index + 12:index + 16])
                else:
                    AID_airportID.append(line[index + 12:index + 15])

    AID_file_sum = 0
    # Finding the sum of the signal strengths for one specific file. Part of finding the file average
    j = 0
    AID_sig_len = len(AID_signalStrengths)
    while j < AID_sig_len:
        AID_file_sum += int(AID_signalStrengths[j])
        j += 1

    if len(AID_signalStrengths) > 0:
        AID_average.append(AID_file_sum / len(AID_signalStrengths))
    #print(AWLU_average)

#Function that opens and prints file
def AWLU_parse(file_path):
    print("AWLU Detected")

    # Set strings of what is being looked for
    sigStr = "Signal Strength"
    airID = 'airportID'
    AWLU_up = []
    AWLU_file_sum = 0

    with open(file_path, 'r') as log_file:
        lines = log_file.readlines()

        for line in lines:
            if sigStr in line:
                # This messy section of code finds the value of the SIGNAL STRENGTH and only inputs the value into the array rather than random characters as well because the length of value changes (def could be easier by idk)
                index = (line.find(sigStr))
                if line[index + 16:index + 19] == "N/A":
                    continue

                if line[index + 19].isalpha():
                    if line[index + 18].isalpha():
                        if line[index + 17].isalpha():
                            print("Not Found")
                        else:
                            AWLU_signalStrengths.append(line[index + 16:index + 17])
                    else:
                        AWLU_signalStrengths.append(line[index + 16:index + 18])
                else:
                    AWLU_signalStrengths.append(line[index + 16:index + 19])

                #Time appears to be in HH:MM:SS Time format
                seconds = 0
                line_split = line.split("-")
                time = line_split[2][3:11]
                #print(time)
                hours = int(time[0:2])
                minutes = int(time[3:5])
                seconds = int(time[6:9])
                #print(hours)
                #print(minutes)
                #print(seconds)
                ticker = hours * 3600 + minutes * 60 + seconds
                AWLU_up.append(ticker)
                #print(ticker)
    #print(AWLU_up)

    # Finding the sum of the signal strengths for one specific file. Part of finding the file average
    j = 0
    sig_len = len(AWLU_signalStrengths)
    while j < sig_len:
        #if AWLU_indicator_array[j] > AWLU_indicator_array[j-1]:
        #    file_sum = 0
        if AWLU_signalStrengths[j] != ",":
            AWLU_file_sum += int(AWLU_signalStrengths[j])
        j += 1

    if len(AWLU_signalStrengths) != 0:
        AWLU_average.append(AWLU_file_sum / len(AWLU_signalStrengths))


#This function formats and creates all of the graphs for the excel spreadsheet
def AID_excel_formatting():

    # Adding data arrays to spreadsheet
    j = 0
    AID_values = len(AID_signalStrengths)
    AID_airVAL = len(AID_airportID)
    AID_ID_len = len(AID_tail_ID)
    AID_average_len = len(AID_average)
    while j < AID_values:
        worksheet1.write(j + 2, 1, int(AID_signalStrengths[j]))
        worksheet1.write(j + 2, 2, int(AID_upTime[j]))
        worksheet1.write(j + 2, 3, int(AID_cellBand[j]))
        j += 1
    j = 0
    while j < AID_airVAL:
        worksheet1.write(j + 2, 5, AID_airportID[j])
        j += 1
    j = 0
    while j < AID_ID_len:
        worksheet1.write(j + 2,6, AID_tail_ID[j])
        j += 1
    j=0
    while j < AID_average_len:
        worksheet1.write(j + 2, 7, AID_average[j])
        j += 1

    worksheet1.set_column('B:B', 20)
    worksheet1.set_column('C:C', 12.43)
    worksheet1.set_column('D:D', 14.5)
    worksheet1.set_column('F:F', 8.65)

    # Adding chart object to file, and setting x and y axis titles
    chart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
    chart.set_x_axis({
        'name': 'Up Time (sec)',
        'name_font': {'size': 14, 'bold': True},
        'num_font': {'italic': True},
    })
    chart.set_y_axis({
        'name': 'Signal Strength (dBm)',
        'name_font': {'size': 14, 'bold': True},
        'num_font': {'italic': True},
    })
    chart.set_size({'width': 600, 'height': 350})
    chart.set_title({'name': 'AID Signal Strength Variation'})

    j = 0
    AID_waypoints = []

    # Finding places where the system starts and stops again through finding where Up Time variable restarts its clock
    while j < AID_values:
        if int(AID_upTime[j]) < int(AID_upTime[j - 1]):
            AID_waypoints.append(j)
        j += 1

    j = 0

    #print(waypoints)
    way_len = len(AID_waypoints)
    i = 0

    # Creates a series in the graph for each time the AID system turns on/off in the specific log file
    while i < way_len:
        if i < way_len - 1:
            chart.add_series({
                'categories': ['Data', AID_waypoints[i] + 2, 2, AID_waypoints[i + 1] + 1, 2],
                'values': ['Data', AID_waypoints[i] + 2, 1, AID_waypoints[i + 1] + 1, 1],
            })
        else:
            chart.add_series({
                'categories': ['Data', AID_waypoints[i] + 2, 2, AID_values + 1, 2],
                'values': ['Data', AID_waypoints[i] + 2, 1, AID_values + 1, 1],
            })
        i += 1

    # Adding chart object to file, and setting x and y axis titles
    chart2 = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
    chart2.set_x_axis({
        'name': 'Up Time (sec)',
        'name_font': {'size': 14, 'bold': True},
        'num_font': {'italic': True},
    })
    chart2.set_y_axis({
        'name': 'Cell Band (MHz)',
        'name_font': {'size': 14, 'bold': True},
        'num_font': {'italic': True},
    })
    chart2.set_size({'width': 600, 'height': 350})
    chart2.set_title({'name': 'AID Cell Band Variation'})

    i = 0
    while i < way_len:
        if i < way_len - 1:
            chart2.add_series({
                'categories': ['Data', AID_waypoints[i] + 2, 2, AID_waypoints[i + 1] + 1, 2],
                'values': ['Data', AID_waypoints[i] + 2, 3, AID_waypoints[i + 1] + 1, 3],
            })
        else:
            chart2.add_series({
                'categories': ['Data', AID_waypoints[i] + 2, 2, AID_values + 1, 2],
                'values': ['Data', AID_waypoints[i] + 2, 3, AID_values + 1, 3],
            })
        i += 1

    # Manual entry example
    # chart.add_series({'categories' : '=Data!$C$3:$C$32',
    #                  'values' : '=Data!$B$3:$B$32'})

    # This section using conditional formatting to color code the effectivity of the current cell band configuration
    cell_format1 = workbook.add_format()
    cell_format2 = workbook.add_format()
    cell_format3 = workbook.add_format()
    cell_format1.set_bg_color('green')
    cell_format2.set_bg_color('red')
    cell_format3.set_bg_color('orange')

    worksheet1.conditional_format('D3:D' + str(AID_values+2), {'type': 'cell',
                                              'criteria': '>=',
                                              'value': 1800,
                                              'format': cell_format1})

    worksheet1.conditional_format('D3:D' + str(AID_values+2), {'type': 'cell',
                                              'criteria': '<',
                                              'value': 1600,
                                              'format': cell_format2})

    worksheet1.conditional_format('D3:D' + str(AID_values+2), {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum': 1600,
                                              'maximum': 1799,
                                              'format': cell_format3})

    textbox_text = 'Cell Band Info: \n' \
                   '~700 MHz: Usally a quite slow, 5 MHz for Download, 0 MHz for Upload (5x0) \n' \
                   '~1700 MHz: Can vary between 5x5, and 10x10 MHz \n' \
                   '~1900 MHz: Mostly stays between 20x20 MHz \n'

    options = {
        'width': 500,
        'height': 150,
        'x_offset': 10,
        'y_offset': 10,

        'font': {'color': 'black',
                 'size': 14},
        'align': {'vertical': 'middle',
                  'horizontal': 'center'
                  },

    }
    #Adding charts to file
    worksheet1.insert_chart('P11',chart)
    worksheet1.insert_chart('Z11',chart2)
    worksheet1.insert_textbox('P2',textbox_text, options)
    workbook.close()


def AWLU_excel_formatting():
    # adding spreadsheet headings
    worksheet1.write(0, 10, 'AWLU DATA')
    worksheet1.write(1, 10, 'Signal Strength (dBm)')
    worksheet1.write(1, 11, 'Data Points')
    worksheet1.write(1, 12, 'Averages (dBm)')

    # Set strings of what is being looked for
    sigStr = "Signal Strength"
    airID = 'airportID'
    AWLU_waypoints = []
    file_sum = 0


    # Adding data arrays to spreadsheet
    j = 0
    AWLU_values = len(AWLU_signalStrengths)
    AWLU_average_len = len(AWLU_average)
#Doesnt work, place holder for conversation
    while j < AWLU_values:
        if AWLU_signalStrengths[j] != "," and AWLU_signalStrengths[j - 1] != "," and int(AWLU_signalStrengths[j]) < int(AWLU_signalStrengths[j - 1]):
            AWLU_waypoints.append(j)

        j += 1
    j=1

    j=0
    while j < AWLU_average_len:

        worksheet1.write(j + 2, 12, AWLU_average[j])
        j += 1

    while j < len(AWLU_waypoints):
#This doesnt help at all, signal strength getting lower doesn't mean that the signal has reset
        #series_len = AWLU_waypoints[j]-AID_waypoints[j-1]
        #series_averages.append(series_len)
        j += 1



    #Yikes, need to figure out uptime
    # airVAL = len(airportID)
    # ID_len = len(tail_ID)
    # LRU_len = len(LRU_type)
    j = 0
    while j < AWLU_values:
        if AWLU_signalStrengths[j] != ",":
            worksheet1.write(j + 2, 10, int(AWLU_signalStrengths[j]))
            worksheet1.write(j + 2, 11, j)
        j += 1

    worksheet1.set_column('K:K', 20)
    worksheet1.set_column('L:L', 10.29)
    worksheet1.set_column('M:M', 13.91)


    # Adding chart object to file, and setting x and y axis titles
    chart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
    chart.set_x_axis({
        'name': 'Data Points',
        'name_font': {'size': 14, 'bold': True},
        'num_font': {'italic': True},
    })
    chart.set_y_axis({
        'name': 'Signal Strength (dBm)',
        'name_font': {'size': 14, 'bold': True},
        'num_font': {'italic': True},
    })
    chart.set_size({'width': 600, 'height': 350})
    chart.set_title({'name': 'AWLU Signal Strength Variation'})

    i = 0
    # Creates a series in the graph for each time the AID system turns on/off in the specific log file
    AWLU_Sig_len = len(AWLU_signalStrengths)

    chart.add_series({
        'categories': ['Data', 2, 11, AWLU_Sig_len + 1, 11],
        'values': ['Data', i + 2, 10, AWLU_Sig_len + 1, 10],
    })

    AWLU_ID_len = len(AWLU_tail_ID)
    AWLU_LRU_len = len(AWLU_LRU_type)
    #print(len(signalStrengths))
    #print(len(upTime))
    j = 0
    while j < AWLU_ID_len:
        worksheet1.write(j + 2, 4, AWLU_tail_ID[j])
        j += 1
    j = 0
    while j < AWLU_LRU_len:
        worksheet1.write(j + 2, 5, AWLU_LRU_type[j])
        j += 1

    worksheet1.insert_chart('P30', chart)
    worksheet1.insert_chart('Z30', chart3)

AID_indicator = 0
AID_indicator_array = [0]
AWLU_indicator = 0
AWLU_indicator_array = [0]

os.chdir(AID_path)
#input1 = input("Are the log files AID or AWLU? (Type AID or AWLU): ")
for file in os.listdir():
    # Goes through every file in the current working directory, create the filepath of particular file
    file_path = f"{AID_path}/{file}"
    AID_file_sum = 0
    AID_parse(file)
    AID_indicator += 1
    AID_indicator_array.append(AID_indicator)

os.chdir('..')
os.chdir(AWLU_path)
for file in os.listdir():
    # Goes through every file in the current working directory, create the filepath of particular file
    file_path = f"{AWLU_path}/{file}"
    AWLU_file_sum = 0
    AWLU_parse(file)
    AWLU_indicator += 1
    AWLU_indicator_array.append(AWLU_indicator)
os.chdir('..')

AWLU_average_len = len(AWLU_average)
AID_average_len = len(AID_average)
# Adding chart object to file, and setting x and y axis titles
chart3 = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
chart3.set_x_axis({
    'name': 'Data Points',
    'name_font': {'size': 14, 'bold': True},
    'num_font': {'italic': True},
})
chart3.set_y_axis({
    'name': 'Average Signal Strength (dBm)',
    'name_font': {'size': 14, 'bold': True},
    'num_font': {'italic': True},
})
chart3.set_size({'width': 600, 'height': 350})
chart3.set_title({'name': 'Average Signal Strengths'})


chart3.add_series({
    'name': 'AWLU',
    'categories': ['Data', 2, 11, AWLU_average_len + 1, 11],
    'values': ['Data', 2, 12, AWLU_average_len + 1, 12],
})
chart3.add_series({
    'name': 'AID',
    'categories': ['Data', 2, 11, AID_average_len + 1, 11],
    'values': ['Data', 2, 7, AID_average_len + 1, 7],
})


AWLU_excel_formatting()
AID_excel_formatting()
#Moves the current working directory back by 1 ('..' does this) so the excel file
#Is created in the original directory
os.chdir('..')





print(AWLU_average)
print(AID_average)
