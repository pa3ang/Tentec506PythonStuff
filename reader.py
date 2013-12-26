# Python 3.3 source!
# created on windows for TEN-TEC Rebel Model 506 in conjunction with RebelAllianceMod firmaware
# PA3ANG, Johan van Dijk  december 26, 2013   v0.1


from serial import *
from tkinter import *
from tkinter import ttk

serialPort = "COM13"    # change to you COM port or on Linux /dev/ttyUSB0 or similar
                        # check for param which could be comm port
for arg in sys.argv[1:]:
    serialPort=arg
baudRate = 115200       # in correspondence with Rebel firmware setting
ser = Serial(serialPort , baudRate, timeout=0, writeTimeout=0) #ensure non-blocking

#make a TkInter Window
root = Tk()
root.wm_title("TEN-TEC Rebel Model 506 - "+serialPort+" : "+str(baudRate)+" Bd")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="OPEN SOURCE QRP | DISPLAY", font=('Arial', 20, 'bold'), width=30).grid(column=2, row=2, sticky=(W, E))
ttk.Label(mainframe, text="v0.1 pyComm", font=('Arial', 20, 'bold')).grid(column=3, row=2)
ttk.Label(mainframe, text="Re-starting the Rebel....", font=('Arial', 20, 'bold')).grid(column=2, row=3,sticky=(W, E))
ttk.Label(mainframe, text="Works with RebelAllianceMod v1.1 and higher!", font=('Arial', 14, 'bold'), foreground='red').grid(column=2, row=4, sticky=(W, E))

label = ttk.Label(mainframe)
image = PhotoImage(file='rebel.gif')
label['image'] = image
label.grid(column=3, row=3)

serBuffer = ""
Line = 3

def readSerial():
    # get the buffer from outside of this function
    global serBuffer
    global Line
    while True:
        receivedChar = ser.read() # attempt to read a character from Serial
        receivedChar = receivedChar.decode("ascii")
        
        #was anything read?
        if len(receivedChar) == 0:
            break
        
        # get the buffer from outside of this function
        global serBuffer
       
        # check if character is a delimeter
        if receivedChar == '\r':
            receivedChar = '' # don't want returns. chuck it
            
        if receivedChar == '\n':
          
            if Line == 3 :
                color = 'black'
                if serBuffer[0:1] == "T":   #transmit state
                    color = 'red'
                ttk.Label(mainframe, text=serBuffer, font=('Arial', 30, 'bold'), foreground=color).grid(column=2, row=Line, sticky=(W,E))
            if Line == 4 :
                if serBuffer[1:2] == "A":   # credits line
                    ttk.Label(mainframe, text="Credits: "+serBuffer, font=('Arial', 16, 'bold')).grid(column=2, row=Line, sticky=(W,E))
                else:                       # search values and display
                    Bandwidth = serBuffer[0:1]
                    Step = serBuffer[2:5]
                    cwSpeed = serBuffer[6:8]
                    Volt = serBuffer[16:21]
                    ttk.Label(mainframe, text="Bw: "+Bandwidth+", Step: "+Step+", Keyer: "+cwSpeed+"wpm, Vcc: "+Volt, font=('Arial', 16, 'bold')).grid(column=2, row=Line, sticky=(W,E))
             
                    meterSource = serBuffer[11:12]    # make S(P)-meter bar
                    Bar = ""
                    i = 1
                    if (serBuffer[13:14] >= "0" and serBuffer[13:14] <= "9"):
                        Svalue = int(serBuffer[13:14])
                        while (i <= Svalue):
                            Bar = Bar + "»"
                            if i == 3:
                                Bar = Bar + "3"
                            if i == 5:
                                Bar = Bar + "5"
                            if i == 7:
                                Bar = Bar + "7"
                            if i == 9:
                                Bar = Bar + "9"
                            i = i + 1
                    if Svalue == 0:
                        Bar = "-"

                
                    ttk.Label(mainframe, text=meterSource+" "+Bar, font=('Arial', 16, 'bold')).grid(column=3, row=Line, sticky=(W,E))
                
            Line = Line + 1
            serBuffer = ""              # empty the buffer
        else:
            serBuffer += receivedChar   # add to the buffer
    
    root.after(10, readSerial)          # check serial again soon
    if Line > 4:
        Line = 2
 	
# after initializing serial, an arduino may need a bit of time to reset
root.after(100, readSerial)
root.mainloop()
