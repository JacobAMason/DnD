#DND game gui map
from tkinter import *

class MapGui:

    def __init__(self):


        """
        declaration of variables to be used
        """
        self.main_window = Tk(className='Map')
        self.empty = PhotoImage(file='dvd.pgm')
        self.full = PhotoImage(file='creeper.pgm')
        #declaration of gui items

        self.c0_0 = Canvas(self.main_window, height=70, width=70)
        self.c0_0.grid(column=0,row=0)
        self.c0_0.create_image(0, 0, anchor='nw',image=self.empty)
        self.c0_0.image = self.empty

        self.c0_1 = Canvas(self.main_window, height=70, width=70)
        self.c0_1.grid(column=0, row=1)
        self.c0_1.create_image(0, 0, anchor='nw', image=self.empty)
        self.c0_1.image = self.empty

        self.c1_0 = Canvas(self.main_window, height=70, width=70)
        self.c1_0.grid(column=1, row=0)
        self.c1_0.create_image(0, 0, anchor='nw', image=self.empty)
        self.c1_0.image = self.empty


        self.c0_2 = Canvas(self.main_window, height=70, width=70)
        self.c0_2.grid(column=0, row=2)
        self.c0_2.create_image(0, 0, anchor='nw', image=self.empty)
        self.c0_2.image = self.full

        self.button = Button(self.main_window, text = 'Move', command=(self.move_character()))
        self.button.grid(column=3, row=3)

        #row1 picture boxes

        mainloop()

    def move_character(self):
        self.empty = PhotoImage(file='creeper.pgm')



test = MapGui()
