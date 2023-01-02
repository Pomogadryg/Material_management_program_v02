from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from datetime import date, timedelta




class classMain(tk.Tk):
	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)

		self.list_of_reagents_fromDB=["PERG SM", "n-PrI", "NMP", "NaHCO3", "CaCl2", "NaBH4", 
		"NaOH", "2-ME", "MeOH", "NaEDTA", "NaCl", "EtOAc", "Et3N", "MsCl","NH4OH", "H20", "MeSNa", "NaClO", "MSA","MeOH_PhEur",  "iPrOH", "Darco" ]

		self.processes={}

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
		self.add_entry = tk.Entry(data_base_frame, width=20)
		self.add_entry.grid(row=0, column=0, sticky=W)

		# Create a button for adding reagents to the data base
		add_button = tk.Button(data_base_frame, text="Add", command=self.add_reagent)
		add_button.grid(row=0, column=1, sticky=W)

		delete_button = tk.Button(data_base_frame, text="Delete", command=self.delete_reagent)
		delete_button.grid(row=0, column=1, sticky=E)

		# Create the text widget for displaying the data base
		self.data_base_text = tk.Text(data_base_frame, width=30, height=50)
		self.data_base_text.config(bg="lightblue")
		self.data_base_text.grid(row=1, column=0, columnspan=2)
		self.initiate_reag_db()
		self.initiate_process_db()


		self.visualization_frame = tk.Frame(main_frame, width=50, height=int(self.winfo_screenheight()))
		self.visualization_frame.pack(side="right", fill="y")

		# Create a list of calendar dates starting 2 days before today and continuing for 40 days
		calendar_dates = [date.today() - timedelta(days=2) + timedelta(days=i) for i in range(40)]

		# Create the labels for calendar and position them using the grid method
		for i in range(1):
			for j in range(2,40):
				self.calendar_label = tk.Label(self.visualization_frame, text=calendar_dates[j].strftime("%d/%m"))
				# label = tk.Label(self.visualization_frame, text=calendar_dates[j].strftime("%d/%m/%Y"))
				self.calendar_label.grid(row=i, column=j)
		


		# Create the list_elements for processes and position them using the grid method
		for i in range(2, 11):
			for j in range(2,40):
				self.my_list = ttk.Combobox(self.visualization_frame, width=7)
				self.my_list["values"]=("Stage1","Stage2", "Stage3")
				self.my_list.grid(row=i, column=j)
				self.processes[(i,j)]=self.my_list
				self.my_list.bind("<<ComboboxSelected>>", lambda event, row=i, col=j: self.save_process_in_db(event, row, col))

		# Create the labels for names for used reagents and position them using the grid method
		range_=len(self.list_of_reagents_fromDB)
		for i in range(11, 11+range_):
			for j in range(1):
				label = tk.Label(self.visualization_frame, text=(self.list_of_reagents_fromDB[i-11]))
				label.grid(row=i, column=j)


		# Create the labels for used reagents and position them using the grid method
		for i in range(11, 11+range_):
			for j in range(2,40):
				label = tk.Label(self.visualization_frame, text='reag.')
				label.grid(row=i, column=j)


	def initiate_reag_db(self):
		conn=sqlite3.connect("reagents.db")
		cursor=conn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS reagent_from_text_widget(WH_code TEXT, amount REAL(5,2))")
		conn.commit()
		conn.close()
		self.fill_up_textW_from_db()

	def initiate_process_db(self):
		conn=sqlite3.connect("process.db")
		cursor=conn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS process(day TEXT, stage TEXT, color TEXT)")
		conn.commit()
		conn.close()

	def save_process_in_db(self,event, row, col):
		# conn=sqlite3.connect("process.db")
		# cursor=conn.cursor()
		# cursor.execute("INSERT INTO process(WH_code,amount) VALUES(?,?)",(wh_c,am))
		# conn.commit()
		# conn.close()
		temp_=str(self.processes[(row,col)]).split(".")		
		# Find the Combobox widget with the desired name
		for widget in self.visualization_frame.winfo_children():
			if widget.winfo_class() == 'TCombobox' and widget.winfo_name() == '%s'%temp_[-1]:
				selected_item = widget.get()
				print(selected_item)
				print(row,col)
				print(self.calendar_label.get())



	def fill_up_textW_from_db(self):
		self.data_base_text.delete("1.0","end")
		conn=sqlite3.connect("reagents.db")
		cursor=conn.cursor()
		cursor.execute("SELECT * FROM reagent_from_text_widget")
		data=(cursor.fetchall())
		for d in data:
			d_code=d[0]
			d_amount=d[1]
			print(d_code,' ', d_amount)
			self.data_base_text.insert("end", "\n%s=%.2f"%(d_code,d_amount))
		print(cursor.fetchall())
		conn.commit()
		conn.close()

	
	def add_reagent(self):
		input_text=self.add_entry.get()
		if input_text:
			if "=" in input_text:
				self.data_base_text.insert("end", "\n%s"%input_text)
				input_text=input_text.split("=")
				wh_c=input_text[0]
				am=input_text[1]
				conn=sqlite3.connect("reagents.db")
				cursor=conn.cursor()
				cursor.execute("INSERT INTO reagent_from_text_widget(WH_code,amount) VALUES(?,?)",(wh_c,am))
				conn.commit()
				conn.close()
			else:
				print("Not correct format of input. Correct format is XXX=yyy")
		else:
			print("No input")

	def delete_reagent(self):
		input_text=self.add_entry.get()
		print(input_text)
		conn=sqlite3.connect("reagents.db")
		cursor=conn.cursor()
		cursor.execute("DELETE FROM reagent_from_text_widget WHERE WH_code=?",(input_text,))
		conn.commit()
		conn.close()
		self.fill_up_textW_from_db()



# Create an instance of the classMain class
app = classMain()

# Run the Tkinter event loop

app.mainloop()
