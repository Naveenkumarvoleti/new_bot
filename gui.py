from final_file import*
try:
    from tkinter import *
except ImportError:
    from Tkinter import*
    
import os,glob
##from ConfigParser import SafeConfigParser
##
##config = SafeConfigParser()
##config.read('config.ini')



def raise_frame(frame):
    frame.tkraise()
    
root = Tk()
##root.attributes('-zoomed',True)
root.title('RIKU')
f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)
f5 = Frame(root)
f6 = Frame(root)
f7 = Frame(root)

##LARGE_FONT= config.get('font', 'LARGE_FONT')
##NORM_FONT = config.get('font', 'NORM_FONT')
##SMALL_FONT = config.get('font', 'SMALL_FONT')

for frame in (f1, f2, f3, f4,f5,f6):
    frame.grid(row=0, column=0, sticky='news')
##f7.grid(row=0,column=1,sticky='news')
    
Label(f1, text='Hi..').pack(padx=500)
Button(f1, text="Let's go", command=lambda:raise_frame(f2)).pack()


""" menu options"""
Label(f2, text='Choose your option').pack()
b4 = Button(f2,text ="Select curry", command=lambda:raise_frame(f4))
b5 = Button(f2,text ="cook rice", command=lambda:raise_frame(f3))
b6 = Button(f2,text = "Testing", command=lambda:raise_frame(f6))
b7=Button(f2,text="cook both", command=lambda:raise_frame(f5))
b4.pack(side=TOP,padx= 10,pady=10)
b5.pack(side = TOP,pady=10,padx=10)
b6.pack(side =TOP,padx=10,pady=10)
b7.pack(side =TOP,padx=10,pady=10)

## riceCook ##
l1=Label(f3,text = "choose rice type")
l1.pack()
slct = StringVar(f3)
slct.set("Bhasmati")
choices = {'bhasmati','Brown rice','paraboiled rice','Arborio rice'}
popupmenu = OptionMenu(f3,slct,*choices)
l5 = Label(f3,text = "start after : ")
amt=Scale(f3,from_=1,to= 60,orient=HORIZONTAL,resolution=1)
popupmenu.pack()
amt.pack()
but=Button(f3,text="make")
but.configure(command= lambda :cookRice(100,amt.get()))
but.pack()
back=Button(f3,text="Main menu")
back.pack()
back.configure(command=lambda:raise_frame(f2))

## testing ##
label_1 = Label(f6, text="temperature")
label_3 = Label(f6, text="induction")
label_2 = Label(f6,text="weight scale")
label_1.pack()#grid(row=1,column=2)
but1 = Button(f6, text="test", command= lambda : temperature(f6))#lambda :command(x.get(), slct.get()))
##but.grid(row=2, column=2)
but1.pack()
label_2.pack()#grid(row=3,column=2)
but2 = Button(f6, text="test", command= lambda :weight(f6))#lambda :command(x.get(), slct.get()))
##but.grid(row=4, column=2)
but2.pack()
label_3.pack()#grid(row=5,column=2)
##entry_1.grid(row=2, column=2)
##entry_2.grid(row=4, column=0)
but3 = Button(f6, text="test", command= lambda :induction(f6))#load(2,'weight'))#lambda :command(x.get(), slct.get()))
##but.grid(row=6, column=2)
but3.pack()

back=Button(f6,text="Main menu")
back.pack()#grid(row=7,column=2)
back.configure(command=lambda:raise_frame(f2))
label1 = Label(f6, text="loadcell:  place something on weight scale and press test")
label2 = Label(f6, text="temperature: press test to get current temperature")
label3 = Label(f6, text="induction:  press test button and select temperature")
label1.pack(padx=0.5,pady=2,side=TOP)
label2.pack(padx=0.5,pady=2)
label3.pack(padx=0.5,pady=2)

def induction(frame):
    label=Label(f6,text="induction started :")
    label.pack(padx=5, pady=5, side=TOP)
##    label.grid(row=1,column=10,pady=10)
##    raise_frame(frame)
    
def weight(frame):
    label=Label(f6,text="weighing: ")
    label.pack(padx=5, pady=5, side=TOP)
##    label.grid(row=10,column=11,pady=10)
##    raise_frame(frame)

def temperature(frame):
    label=Label(f6,text="temperature: ")
    label.pack(padx=5, pady=5, side=TOP)
##    label.grid(row=20,column=12,pady=10)
##    raise_frame(frame)

l6=Label(f4,text="Select curry")
l5 = Label(f4,text = "start after : ")
l6.pack()
lb = Listbox(f4,width=15,height=2)
lb.pack(side=TOP,pady=2)
os.chdir(".")
for file in glob.glob("*.json"):
    files=file
    lb.insert(END,files)
b8=Button(f4,text="MAKE....")
amt=Scale(f4,from_=1,to= 60,orient=HORIZONTAL,resolution=1)
b8.configure(command = lambda :readRecipe(lb.get(ACTIVE),amt.get()))
l5.pack
amt.pack()
b8.pack()
back=Button(f4,text="Main menu")
back.pack()
back.configure(command=lambda:raise_frame(f2))

## cook Both ##
l1=Label(f5,text = "choose rice type")
selct=StringVar(f5)
l2=Label(f5,text = "select curry")
l1.pack()#grid(row=1)
lb = Listbox(f5,width=15,height=2)
os.chdir(".")
for file in glob.glob("*.json"):
    files=file
    lb.insert(END,files)
butt = Button(f5,text = "MAKE",command = lambda : startBoth(lb.get(ACTIVE),slct.get()))
slct = StringVar(f5)
slct.set("Bhasmati")
choices = {'Bhasmati','Brown rice','Paraboiled rice','Arborio rice'}
popupmenu = OptionMenu(f5,slct,*choices)
popupmenu.pack()#grid(row=2)
l2.pack()#grid(row=4)
lb.pack()#grid(row=5)
butt.pack()#grid(row=6)
back=Button(f5,text="Main menu")
back.pack()#grid(row=7,column=2)
back.configure(command=lambda:raise_frame(f2))


Label(f7, text='place spice in the pod').pack(pady=10,side=TOP)
Button1 = Button(f7,text='POD1')
Button1.place(relx=0.42, rely=0.05, height=34, width=34)
Button2 = Button(f7,text='POD2')
Button2.place(relx=0.23, rely=0.14, height=34, width=34)
Button3 = Button(f7,text='POD3')
Button3.place(relx=0.61, rely=0.14, height=34, width=34)
Button4 = Button(f7,text='POD4')
Button4.place(relx=0.11, rely=0.37, height=34, width=34)
Button5 = Button(f7,text='POD5')
Button5.place(relx=0.73, rely=0.37, height=34, width=34)        
Button6 = Button(f7,text='POD6')
Button6.place(relx=0.42, rely=0.69, height=34, width=34)
Button7 = Button(f7,text='POD7')
Button7.place(relx=0.61, rely=0.6, height=34, width=34)        
Button8 = Button(f7,text='POD8')
Button8.place(relx=0.23, rely=0.6, height=34, width=34)


def popupmsg(msg,Type=0,st=DISABLED,bT="ok",cmd=None):
    global popup
    popup = Tk()
    popup.wm_title("ERROR")
    label = Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    if Type == 1:
        b1=Button(popup,state=st,text=bT,command = popup.destroy)
        b1.pack()
    else:
        B1 = Button(popup, text="Yes", command = lambda :cmd)
        B1.pack()
        B2 = Button(popup, text="NO", command = popup.destroy)
        B2.pack()


def welcome(message):
    top = Tk()
    top.title('Welcome')
    Message(top, text=message, padx=20, pady=20).pack()
    top.after(2000, top.destroy)


raise_frame(f1)
root.mainloop()

