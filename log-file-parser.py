

import re
import xlsxwriter
import pandas as pd

#Importing direct log file path, along with opening and reading the file
log_file_path = r"C:\Users\walke\Downloads\LogProject\SWA Logs\N8707P_REPORT_LOG-SYSTEM_20220411044727+0000-[PS-WPLSAPLPX01]\N8707P-LOG-SYSTEM-20220411043505\N8707P\LOG\SYSTEM\N8707P-LOG-SYSTEM-20220405-193001\N8707P-LOG-SYSTEM-app-aid-wwu-20220405-193001.log"
log_file = open(log_file_path)

#Adding excel file for data to be imported into
workbook = xlsxwriter.Workbook(r'C:\Users\walke\OneDrive\Desktop\logFILEoutput.xlsx')
# worksheet for all the parsed data
worksheet1 = workbook.add_worksheet('Data')

#adding spreadsheet headings
worksheet1.write(1, 1 , 'Signal Strength (dBm)')
worksheet1.write(1, 2 , 'Up Time (sec)')
worksheet1.write(1, 3 , 'Cell Band (MHz)')
worksheet1.write(1, 4 , 'Airport ID')


#Parse the file into a list of individual lines
lines = log_file.readlines()

#Set strings of what is being looked for
sigStr = "signalStrength"
upTm = "upTime"
cellBND = 'cellBand'
airID = 'airportID'


#create arrays for important variables
signalStrengths = []
upTime = []
cellBand = []
airportID = []
for line in lines:
    if sigStr in line:

        # This messy section of code finds the value of the SIGNAL STRENGTH and only inputs the value into the array rather than random characters as well because the length of value changes (def could be easier by idk)
        index = (line.find(sigStr))
        if line[index+19].isalpha():
            if line[index+18].isalpha():
                if line[index + 17].isalpha():
                    print("lol")
                else:
                    signalStrengths.append(line[index + 15:index + 17])
            else:
                signalStrengths.append(line[index + 15:index + 18])
        else:
            signalStrengths.append(line[index + 15:index + 19])

        #signalStrengths.append(line[index+15:index+18])

        #This messy section of code finds the value of the UP TIMES and only inputs the value into the array rather than random characters as well because the length of value changes (def could be easier by idk)
        index = (line.find(upTm))
        if line[index+11].isalpha():
            if line[index+10].isalpha():
                if line[index+9].isalpha():
                    if line[index+8].isalpha():
                        print('lol')
                    else:
                        upTime.append(line[index + 7:index + 8])
                else:
                    upTime.append(line[index + 7:index + 9])
            else:
                upTime.append(line[index + 7:index + 10])
        else:
            upTime.append(line[index+7:index+11])




        # This messy section of code finds the value of the CELL BANDS and only inputs the value into the array rather than random characters as well because the length of value changes (def could be easier by idk)
        index = (line.find(cellBND))
        if line[index + 13].isalpha():
            if line[index + 12].isalpha():
                if line[index + 11].isalpha():
                    if line[index + 10].isalpha():
                        print('lol')
                    else:
                        cellBand.append(line[index + 9:index + 10])
                else:
                    cellBand.append(line[index + 9:index + 11])
            else:
                cellBand.append(line[index + 9:index + 12])
        else:
            cellBand.append(line[index + 9:index + 13])

    if airID in line:
        # This messy section of code finds the value of the AIRPORT ID and only inputs the value into the array rather than random characters as well because the length of value changes (def could be easier by idk)
        index = (line.find(airID))
        if line[index + 15].isalpha():
            airportID.append(line[index + 12:index + 16])
        else:
            airportID.append(line[index + 12:index + 15])

print("Siganl Strengths:")
print(len(signalStrengths))
print(signalStrengths)
print("Up Times:")
print(len(upTime))
print(upTime)
print("Cell Bands:")
print(len(cellBand))
print(cellBand)
print("Airport ID:")
print(len(airportID))
print(airportID)

#signalStrengths = int(signalStrengths)
# Adding data arrays to spreadsheet
j = 0
values = len(signalStrengths)
airVAL = len(airportID)
while j < values:
    worksheet1.write(j+2, 1 , int(signalStrengths[j]))
    worksheet1.write(j+2, 2 , int(upTime[j]))
    worksheet1.write(j+2, 3 , int(cellBand[j]))
    j += 1
j=0
while j < airVAL:
    worksheet1.write(j+2, 4, airportID[j])
    j += 1

worksheet1.set_column(1,1,20)
worksheet1.set_column(1,2,15)
worksheet1.set_column(1,3,15)
worksheet1.set_column(1,4,15)

#Adding chart object to file, and setting x and y axis titles
chart = workbook.add_chart({'type' : 'scatter' , 'subtype' : 'straight'})
chart.set_x_axis({
    'name': 'Up Time (sec)',
    'name_font': {'size': 14, 'bold': True},
    'num_font':  {'italic': True },
})
chart.set_y_axis({
    'name': 'Signal Strength (dBm)',
    'name_font': {'size': 14, 'bold': True},
    'num_font':  {'italic': True },
})
chart.set_size({'width': 600, 'height': 350})
chart.set_title({'name' : 'Signal Strength Vs. Time'})

j = 0
waypoints = []

#Finding places where the system starts and stops again through finding where Up Time variable restarts its clock
while j < values:
    if int(upTime[j]) < int(upTime[j-1]):
        waypoints.append(j)
    j += 1

print(waypoints)
way_len = len(waypoints)
i = 0

#Creates a series in the graph for each time the AID system turns on/off in the specific log file
while i < way_len:
    if i < way_len-1:
        chart.add_series({
            'categories': ['Data', waypoints[i] + 2, 2, waypoints[i + 1] + 1, 2],
            'values':     ['Data', waypoints[i] + 2, 1, waypoints[i + 1] + 1, 1],
            })
    else:
        chart.add_series({
            'categories': ['Data', waypoints[i] + 2, 2, values + 1, 2],
            'values':     ['Data', waypoints[i] + 2, 1, values + 1, 1],
            })
    i += 1


#Adding chart object to file, and setting x and y axis titles
chart2 = workbook.add_chart({'type' : 'scatter' , 'subtype' : 'straight'})
chart2.set_x_axis({
    'name': 'Up Time (sec)',
    'name_font': {'size': 14, 'bold': True},
    'num_font':  {'italic': True },
})
chart2.set_y_axis({
    'name': 'Cell Band (MHz)',
    'name_font': {'size': 14, 'bold': True},
    'num_font':  {'italic': True },
})
chart2.set_size({'width': 600, 'height': 350})
chart2.set_title({'name' : 'Cell Band Variation'})

i=0
while i < way_len:
    if i < way_len-1:
        chart2.add_series({
            'categories': ['Data', waypoints[i] + 2, 2, waypoints[i + 1] + 1, 2],
            'values':     ['Data', waypoints[i] + 2, 3, waypoints[i + 1] + 1, 3],
            })
    else:
        chart2.add_series({
            'categories': ['Data', waypoints[i] + 2, 2, values + 1, 2],
            'values':     ['Data', waypoints[i] + 2, 3, values + 1, 3],
            })
    i += 1

#Manual entry example
#chart.add_series({'categories' : '=Data!$C$3:$C$32',
#                  'values' : '=Data!$B$3:$B$32'})

# This section using conditional formatting to color code the effectivity of the current cell band configuration
cell_format1 = workbook.add_format()
cell_format2 = workbook.add_format()
cell_format3 = workbook.add_format()
cell_format1.set_bg_color('green')
cell_format2.set_bg_color('red')
cell_format3.set_bg_color('orange')

worksheet1.conditional_format('D3:D160', {'type':     'cell',
                                        'criteria': '>=',
                                        'value':    1800,
                                        'format':   cell_format1})

worksheet1.conditional_format('D3:D160', {'type':     'cell',
                                        'criteria': '<',
                                        'value':    1600,
                                        'format':   cell_format2})

worksheet1.conditional_format('D3:D160', {'type':     'cell',
                                        'criteria': 'between',
                                        'minimum':    1600,
                                        'maximum':    1799,
                                        'format':   cell_format3})

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
worksheet1.insert_chart('G14',chart)
worksheet1.insert_chart('Q14',chart2)
worksheet1.insert_textbox('F2',textbox_text, options)
workbook.close()



