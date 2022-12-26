import tkinter as tk

class ExampleFrame(tk.Tk):
    def __init__(self, *args, **kwargs):

        self.db_list=[]
        tk.Tk.__init__(self, *args, **kwargs)

        # Set the window title and size
        self.title("Frame Example")
        self.geometry("{}x{}".format(int(self.winfo_screenwidth() * 0.8), int(self.winfo_screenheight() * 0.7)))

        # Create a frame with the desired size
        main_frame = tk.Frame(self, width=int(self.winfo_screenwidth() * 0.8), height=int(self.winfo_screenheight() * 0.7))
        main_frame.pack(fill="both", expand=True)

        # Create a frame for the data base
        data_base_frame = tk.Frame(main_frame, width=50, height=int(self.winfo_screenheight()))
        data_base_frame.pack(side="left", fill="y")

        # Create an entry field for adding reagents
        self.add_entry = tk.Entry(data_base_frame, width=50)
        self.add_entry.grid(row=0, column=0)

        # Create a button for adding reagents to the data base
        add_button = tk.Button(data_base_frame, text="Add", command=self.add_reagent)
        add_button.grid(row=0, column=1)

        # Create the text widget for displaying the data base
        self.data_base_text = tk.Text(data_base_frame, width=50, height=50)
        self.data_base_text.config(bg="lightblue")
        self.data_base_text.grid(row=1, column=0, columnspan=2)
    
    def add_reagent(self):
        input_text=self.add_entry.get()
        print(input_text)


# Create an instance of the ExampleFrame class
app = ExampleFrame()

# Run the Tkinter event loop

app.mainloop()
