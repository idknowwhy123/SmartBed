from tkinter import *
from tkinter import ttk
# Create object
root = Tk()

# Define the geometry of the window
root.geometry("400x300")

#define title
root.title("Countdown timer")

# set backgrou  nd color
root.config(bg='#345')
  
# declaration of variables
hour1=StringVar()
minute1=StringVar()
second1=StringVar()
  
# setting the default value as 0
hour1.set("00")
minute1.set("00")
second1.set("00")
  
# Using Entry class to take input from the user
hour_box1= Entry(
	root, 
	width=3, 
	font=("Arial",18,""),
	textvariable=hour1
	)

hour_box1.place(x=80,y=20)
  
mins_box1 = Entry(
	root, 
	width=3, 
	font=("Arial",18,""),
	textvariable=minute1)

mins_box1.place(x=130,y=20)
  
sec_box1 = Entry(
	root, 
	width=3, 
	font=("Arial",18,""),
	textvariable=second1)

sec_box1.place(x=180,y=20)
  
  
def countdowntimer():
    try:
        # store the user input
        user_input = int(hour1.get())*3600 + int(minute1.get())*60 + int(second1.get())
    except:
        messagebox.showwarning('', 'Invalid Input!')
    while user_input >-1:
         
        # divmod(firstvalue = user_input//60, secondvalue = user_input%60)
        mins,secs = divmod(user_input,60)
  
        # Converting the input entered in mins or secs to hours,
        hours=0
        if mins >60:

            hours, mins = divmod(mins, 60)
         
        # store the value up to two decimal places
        # using the format() method
        hour.set("{0:2d}".format(hours))
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))
  
        # updating the GUI window 
        root.update()
        time.sleep(1)
  
        # if user_input value = 0, then a messagebox pop's up
        # with a message
        if (user_input == 0):
            messagebox.showinfo("Time Countdown", "Time Over")
         
        # decresing the value of temp 
        # after every one sec by one
        user_input -= 1
 
# button widget
btn = Button(root, text='Start', bd='5',
            command= countdowntimer)
btn.place(x = 80,y = 120)
if(hour1 == 0 and minute1 == 0 and second1 == 0):
    messageNotify("ถึงเวลารับประทานยาแล้วครับ")
    stickerNotify("10551380","6136")
root.mainloop()