#Author: Dehansa Dissanayake
#Date: 24/12/2024
#Student ID: w2119977 (20231524)

import csv

# Task A: Input Validation
def validate_date_input(prompt, minValue=None, maxValue=None): 
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """

    while True:
        user_input = input(prompt)
        try:
            value = int(user_input) #convert the user input to a integer
            #checking if the user input value is in the range
            if minValue is not None and value < minValue: 
                print(f'Out of range - values must be in the range {minValue} and {maxValue}.')
                continue
                
            if maxValue is not None and value > maxValue:
                print(f'Out of range - values must be in the range {minValue} and {maxValue}.')
                continue
            return value
                            
        except ValueError:
            print('Integer required') #if the user input is not an integer this will print
                    


def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """

    while True:
        continue_program = input("Do you want to select another data file for a different date? (Y/N): ").upper() #the upper() will turn all inputs to uppercase
        if continue_program == "Y":
            return True  #if Y, programme will run again
        
        if continue_program == "N":
            print("End of run")
            return False   #if N, programme will end  
        else:
            print('Invalid: Please enter “Y” or “N”')



# Task B: Processed Outcomes
def process_csv_data(file_name):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """

    #initializing the variables
    outcomes = {}
    total_vehicles = 0
    total_trucks = 0
    electric_vehicles = 0
    twoWheeled_vehicles = 0
    busses_leaving_elmAvenue_heading_north = 0
    vehicles_passing_without_turning = 0
    truck_percentage = 0
    total_bicycle = 0
    average_bicycle_perhour = 0
    vehicles_over_speedlimit = 0
    vehicles_through_elmAvenue = 0
    vehicles_through_hanleyhigh = 0
    total_scooters_elmAvenue = 0
    percentage_scooter_elmAvenue = 0
    vehicles_inPeak_hanleyhigh = [0]*24 # creating a list with 24 zeros one for each hour
    peak_hour_index = None
    peak_hour_format = None
    rain_hours = set()
    # creating two lists with 24 zeros for each junction (one for each hour of the day)
    vehicles_per_hour_elm_ave = [0] * 24
    vehicles_per_hour_hanley_high = [0] * 24
    traffic_data = {} #dictionary to save the hourly vehicle info



    try:
        with open(file_name,'r') as csv_file:  #opening the csv file in read mode
            csv_data = csv.DictReader(csv_file)  # csv.dictreader() method used for easier column access using field names beacase it works as a dictionary
                                                 #Reference: GeeksForGeeks - https://www.geeksforgeeks.org/reading-csv-files-in-python/
            # Iterating through each row in the CSV file
            for row in csv_data:  
                #counting total vehicles
                total_vehicles += 1 

                #getting the data from the coloumns
                vehicle_type = row.get('VehicleType','').lower()  # '' used in case if there is a blank space in the VehicleType coloumn
                electricHybrid = row.get('elctricHybrid','').lower() # used get() function to acsess the electricHybrid coloumn                
                junction_name = row.get('JunctionName','').lower()  #used lower function turn all the letters into lowercase so that will be easy to find
                heading_out = row.get('travel_Direction_out','').lower()
                heading_in = row.get('travel_Direction_in','').lower()
                junction_speed = row.get('JunctionSpeedLimit','')
                vehicle_speed = row.get('VehicleSpeed','')
                time_of_day = row.get('timeOfDay','') 
                weather = row.get('Weather_Conditions','').lower()
                time_hour = int((time_of_day).split(':')[0]) #using the split() to get only the hour part and convert the it to integer

                

                #counting trucks
                if vehicle_type == 'truck': 
                    total_trucks += 1

                #Counting electric vehicles
                if electricHybrid == 'true':
                    electric_vehicles += 1

                #Counting two-wheeled vehicles
                if vehicle_type in ['bicycle', 'motorcycle', 'scooter']:
                    twoWheeled_vehicles += 1

                #Counting total busses leaving Elm Avenue/Rabbit Road junction heading north
                if junction_name == 'elm avenue/rabbit road':
                    if vehicle_type == 'buss':
                        if heading_out == 'n':
                            busses_leaving_elmAvenue_heading_north += 1

                #Counting total vehicles passing through both junctions without turning left or right. 
                if heading_in == heading_out :
                    vehicles_passing_without_turning += 1

                #percentage of all vehicles recorded that are Trucks for the selected date (rounded to an integer). 
                truck_percentage = round((total_trucks/total_vehicles)*100)

                #average number Bicycles per hour for the selected date (rounded to an integer).
                if vehicle_type == 'bicycle':
                    total_bicycle += 1
                average_bicycle_perhour = round(total_bicycle/24)

                #total vehicles recorded as over the speed limit for the selected date.
                if int(vehicle_speed) > int(junction_speed):
                    vehicles_over_speedlimit += 1

                #total vehicles recorded through only Elm Avenue/Rabbit Road junction for the selected date. 
                if junction_name == 'elm avenue/rabbit road':
                    vehicles_through_elmAvenue += 1
                    
                #total vehicles recorded through only Hanley Highway/Westway junction for the selected date
                if junction_name == 'hanley highway/westway':
                    vehicles_through_hanleyhigh += 1
                    
                #percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters (rounded to integer)
                if junction_name == 'elm avenue/rabbit road':
                    if vehicle_type == 'scooter':
                        total_scooters_elmAvenue += 1
                percentage_scooter_elmAvenue = int((total_scooters_elmAvenue/vehicles_through_elmAvenue)*100) 
                #vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway.
                if junction_name == 'hanley highway/westway':
                    if 0 < time_hour < 24: #to check time is valid
                        vehicles_inPeak_hanleyhigh[time_hour] += 1 #the vehicle count is added to the correcponding hour in the list                   
                
                get_vehicles_inpeak = max(vehicles_inPeak_hanleyhigh)  #to find the total vehicles in the peak hour from the list    


                #times of the peak traffic hours on Hanley Highway/Westway in the format Between 18:00 and 19:00.  – (note this may be multiple hours). 
                peak_hour_index = vehicles_inPeak_hanleyhigh.index(max(vehicles_inPeak_hanleyhigh))

                peak_hour_format = f'The most vehicles through Hanley Highway/Westway were recorded between {peak_hour_index}:00 and {peak_hour_index+1}:00  '

               
                #total number of hours of rain on the selected date.
                if 'rain' in weather:
                    rain_hours.add(time_hour)
                total_rain_hours = len(rain_hours)


                # Counting the vehicles in each junction
                if 0 <= time_hour < 24:  
                    if junction_name == 'elm avenue/rabbit road':
                        vehicles_per_hour_elm_ave[time_hour] += 1  # Increment for Elm Avenue/Rabbit Road
                    elif junction_name == 'hanley highway/westway':
                        vehicles_per_hour_hanley_high[time_hour] += 1  # Increment for Hanley Highway/Westway


            #dictionary to use the data for draw the histogram
            traffic_data = {
                    'elm_avenue': vehicles_per_hour_elm_ave,
                    'hanley_highway': vehicles_per_hour_hanley_high
            }
        
    

            #creating a dictionary so it is easy to get the outcomes 
            outcomes = {
                "total_vehicles": total_vehicles,
                "total_trucks": total_trucks,
                "electric_vehicles": electric_vehicles,
                "twoWheeled_vehicles": twoWheeled_vehicles,
                "busses_leaving_elmAvenue_heading_north": busses_leaving_elmAvenue_heading_north,
                "vehicles_passing_without_turning": vehicles_passing_without_turning,
                "truck_percentage": truck_percentage,
                "average_bicycle_perhour": average_bicycle_perhour,
                "vehicles_over_speedlimit": vehicles_over_speedlimit,
                "vehicles_through_elmAvenue": vehicles_through_elmAvenue,
                "vehicles_through_hanleyhigh": vehicles_through_hanleyhigh,
                "percentage_scooter_elmAvenue": percentage_scooter_elmAvenue,
                "get_vehicles_inpeak": get_vehicles_inpeak,
                "peak_hour_format": peak_hour_format,
                "total_rain_hours": total_rain_hours
            }

            return outcomes, traffic_data
             

    except FileNotFoundError:
        return None, None  #if the file is not found it returns None so that when Task_de file loads data if its none it prints file not found
       
            

def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    #display the outcomes in the console
    print(f'The total number of vehicles recorded to this date is {outcomes["total_vehicles"]}')
    print(f'The total number of trucks recorded to this date is {outcomes["total_trucks"]}')
    print(f'The total number of electric_vehicles recorded to this date is {outcomes["electric_vehicles"]}')
    print(f'The total number of twoWheeled_vehicles recorded to this date is {outcomes["twoWheeled_vehicles"]}')
    print(f'The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes["busses_leaving_elmAvenue_heading_north"]}')
    print(f'The total number of Vehicles through both junctions not turning left or right is {outcomes["vehicles_passing_without_turning"]}')
    print(f'The percentage of total vehicles recorded that are trucks for this date is {outcomes["truck_percentage"]}%')
    print(f'the average number of Bikes per hour for this date is {outcomes["average_bicycle_perhour"]}')
    print(f'The total number of Vehicles recorded as over the speed limit for this date is {outcomes["vehicles_over_speedlimit"]}') 
    print(f'The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes["vehicles_through_elmAvenue"]}')  
    print(f'The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes["vehicles_through_hanleyhigh"]} ')
    print(f'{outcomes["percentage_scooter_elmAvenue"]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters')
    print(f'The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes["get_vehicles_inpeak"]}')
    print(f'{outcomes["peak_hour_format"]}')
    print(f'The number of hours of rain for this date is {outcomes["total_rain_hours"]}')



# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """

    try: 
        with open('results.txt','a') as file:  #open the file in append mode
            #writing the data into the file
            file.write(f'data file Selected is: {file_name}\n')
            file.write(f'The total number of vehicles recorded to this date is {outcomes["total_vehicles"]}\n')
            file.write(f'The total number of trucks recorded to this date is {outcomes["total_trucks"]}\n')
            file.write(f'The total number of electric vehicles recorded to this date is {outcomes["electric_vehicles"]}\n')
            file.write(f'The total number of two-wheeled vehicles recorded to this date is {outcomes["twoWheeled_vehicles"]}\n')
            file.write(f'The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes["busses_leaving_elmAvenue_heading_north"]}\n')
            file.write(f'The total number of Vehicles through both junctions not turning left or right is {outcomes["vehicles_passing_without_turning"]}\n')
            file.write(f'The percentage of total vehicles recorded that are trucks for this date is {outcomes["truck_percentage"]}%\n')
            file.write(f'the average number of Bikes per hour for this date is {outcomes["average_bicycle_perhour"]}\n')
            file.write(f'The total number of Vehicles recorded as over the speed limit for this date is {outcomes["vehicles_over_speedlimit"]}\n') 
            file.write(f'The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes["vehicles_through_elmAvenue"]}\n')  
            file.write(f'The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes["vehicles_through_hanleyhigh"]}\n')
            file.write(f'{outcomes["percentage_scooter_elmAvenue"]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters\n')
            file.write(f'The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes["get_vehicles_inpeak"]}\n')
            file.write(f'{outcomes["peak_hour_format"]}\n')
            file.write(f'The number of hours of rain for this date is {outcomes["total_rain_hours"]}\n\n')

            file.write(f'*******************************\n\n') #to add a new line so it look better in the text file
        
    except IOError: # Reference: AskPython - https://www.askpython.com/python/examples/handling-ioerrors
        print("Unable to write to the file. Check permissions.")  #The user does not have permission to access the file or File already in use this will printed
        

