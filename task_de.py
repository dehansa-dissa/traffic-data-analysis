import tkinter as tk
import task_abc as TaskABC

class HistogramApp:
    def __init__(self, traffic_data, date):
        self.traffic_data = {
            "Elm Avenue/Rabbit Road": traffic_data['elm_avenue'],
            "Hanley Highway/Westway": traffic_data['hanley_highway']
        }
        # Format date from DDMMYYYY to DD/MM/YYYY
        self.date = f"{date[:2]}/{date[2:4]}/{date[4:]}"
        self.root = tk.Tk()
        self.root.title('Histogram')
        self.root.geometry('1400x600')
        
        # Define colors as class attribute so it is easy to use it later
        self.colors = {
            "Elm Avenue/Rabbit Road": "lightblue",  
            "Hanley Highway/Westway": "lightgreen"   
        }
        
        self.canvas = None

    def setup_window(self):
        self.canvas = tk.Canvas(self.root, width=1400, height=600, bg="white")
        self.canvas.pack(pady=20, padx=20)
        self.draw_histogram()

    def draw_histogram(self):
        # Constants for drawing  
        bar_width = 20  # Width of each bar
        bar_gap = 2  # Gap between two bars of the same hour
        hour_gap = 10  # Gap between different hours
        start_x = 80
        start_y = 500
        max_value = max(max(hourly_data) for hourly_data in self.traffic_data.values())

        # Draw title
        self.canvas.create_text(600, 30, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", font=("Arial", 14, "bold"))

        # Draw axes
        self.canvas.create_line(start_x, start_y, 1300, start_y, width=1)  # X-axis
        self.canvas.create_line(start_x, start_y, start_x, 50, width=1)    # Y-axis

        # Draw X-axis labels (hours)
        for hour in range(24):
            x = start_x + hour * (2 * bar_width + bar_gap + hour_gap) + bar_width
            self.canvas.create_text(x, start_y + 15, text=f"{hour:02d}", font=("Arial", 8))

        # Add X-axis title
        self.canvas.create_text(600, start_y + 35, text="Hours 00:00 to 24:00", font=("Arial", 10))

        # Draw bars for each junction
        for hour in range(24):
            x_base = start_x + hour * (2 * bar_width + bar_gap + hour_gap)
            
            for idx, (junction, hourly_data) in enumerate(self.traffic_data.items()):
                value = hourly_data[hour]
                bar_height = (value / max_value) * 400 if max_value > 0 else 0
                
                x1 = x_base + idx * bar_width
                y1 = start_y - bar_height
                x2 = x1 + bar_width
                y2 = start_y
                
                # Draw bar
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                          fill=self.colors[junction],
                                          outline="black")
                
                # Add value on top of bar
                if value > 0:  # Only show non-zero values
                    self.canvas.create_text((x1 + x2) / 2, y1 - 10,
                                          text=str(value),
                                          font=("Arial", 8))

        # Draw legend
        self.draw_legend()

    def draw_legend(self):
        legend_y = 70
        legend_x = 100
        
        for idx, (junction_name, color) in enumerate(self.colors.items()):
            # Draw colored rectangle
            self.canvas.create_rectangle(legend_x, legend_y + idx * 25,
                                       legend_x + 20, legend_y + 20 + idx * 25,
                                       fill=color, outline="black")
            # Add junction name
            self.canvas.create_text(legend_x + 25, legend_y + 10 + idx * 25,
                                  text=junction_name, anchor="w",
                                  font=("Arial", 10))

    def run(self):
        try:
            self.setup_window()
            self.root.mainloop()
        except Exception as e:
            print(f"An error occurred while running the Tkinter: {e}")      #[Reference: GeeksForGeeks - https://www.geeksforgeeks.org/python-tkinter-tutorial/]
            

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        outcomes, traffic_data = TaskABC.process_csv_data(file_path) #loads the data processed from the module TaskABC
        if outcomes is None or traffic_data is None: #check if the outcomes and traffic_data is empty
            print(f'File {file_path} not Found')
            return False
        
        self.current_data = (outcomes, traffic_data)
        return True


    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None #clear the data from the previous run by setting the current_data to None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        while True:
            #getting user inputs and validates using the validate_date_input() function 
            day = TaskABC.validate_date_input('Please enter the day of the survey in the format dd: ', 1, 31)
            month = TaskABC.validate_date_input('Please enter the month of the survey in the format MM: ', 1, 12)
            year = TaskABC.validate_date_input('Please enter the year of the survey in the format YYYY: ', 2000, 2024)
            print() ## to add a space after getting inputs

            #format the name to select the traffic data file
            date = str(f'{day:02d}{month:02d}{year}')  #[Reference: PythonTutorial - https://www.pythontutorial.net/python-basics/python-f-strings/]
            file_name = f'traffic_data{date}.csv'
            print('*' * 40) #to look better
            print(f"Data file Selected is: {file_name}")
            print('*' * 40) #to look better

            if not self.load_csv_file(file_name): #to skip if there is no file
                continue

            outcomes, traffic_data = self.current_data #unpacking the tuple
            TaskABC.display_outcomes(outcomes)
            TaskABC.save_results_to_file(outcomes, file_name)
            print() # to add a space after displaying results

            #calling the function to create the histrogram
            histogram_app = HistogramApp(traffic_data, date)
            histogram_app.run()

            if not TaskABC.validate_continue_input(): #this function is to ask from the user if they want to continue or not
                break                            #[Reference: This while loop was taken from my previous taskabc]

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        self.handle_user_interaction() #Callin the handle_user_interaction()


def main(): 
    processor = MultiCSVProcessor()
    processor.process_files()


if __name__ == '__main__':
    main()  #calling the main() function
