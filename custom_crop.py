from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageGrab, ImageDraw
import glob
import os

## Functions

# def click(event):
#     print("Mouse position: (%s %s)" % (event.x, event.y))

#     return


# # GUI
# root = Tk()

# image_window = Canvas(root, width=800, height=800)
# image_window.pack()

# img = Image.open('/Users/ethanlee/Desktop/me.jpg')
# render = ImageTk.PhotoImage(img)

# image_window.create_image(800,800,image=render)
# image_window.bind("<Button-1>", click)
# # img1 = Label(root, image=render)
# # img1.

# frm = ttk.Frame(root, padding=10)
# frm.pack()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# root.mainloop()


class Crop(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)

        self.pack(expand=YES, fill=BOTH)
        #parent.title("Image classification cropper.")

        ## TODO ##
        ## look for save file. If exists then load into list of images, else do nothing
        ## prevent load_dir if save file exists

        ## add buttons to allow user to choose save path/directory
        
                
        #GUI
        #self.root = Tk()
        self.rect = None

        self.image_window = Canvas(self, width=500, height=300, relief=SUNKEN)
        #self.image_window.pack()

        # self.img = Image.open('/Users/ethanlee/Desktop/me.jpg')
        # self.render = ImageTk.PhotoImage(self.img)

        #self.image_window.create_image(800,800,image=self.render)
        self.image_window.bind("<Button-1>", self.click)
        # img1 = Label(root, image=render)
        # img1.

        self.image_counter = 0

        self.frm = ttk.Frame(self, padding=10)
        self.frm.pack()
        self.hbar = ttk.Scrollbar(self, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)#.grid(column=1, row=0)
        #self.hbar.grid(column=1, row=0)
        self.vbar = ttk.Scrollbar(self, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)#.grid(column=2, row=0)
        #self.vbar.grid(column=2, row=0)
        # self.hbar.config(command=self.image_window.xview)
        # self.vbar.config(command=self.image_window.yview)
        #self.image_window.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        #self.image_window.config(scrollregion=self.image_window.bbox(ALL))
        #self.label = Label(self.frm, text="Hello World!").grid(column=0, row=0)
        self.label = ttk.Label(self.frm, text="Hello World!")
        self.label.grid(column=0, row=0)
        self.button = ttk.Button(self.frm, text="Save image", command=self.save_img).grid(column=1, row=1)
        self.load_dir = ttk.Button(self.frm, text="Load directory", command=self.load_directory).grid(column=2, row=1)
        self.next = ttk.Button(self.frm, text="Next image", command=self.next_img).grid(column=4, row=0)
        self.save_and_exit = ttk.Button(self.frm, text="Save progress and exit", command=self.save_exit).grid(column=3, row=1)
        self.delete_save = ttk.Button(self.frm, text="Delete save file", command=self.delete_save_file).grid(column=4, row=1)
        self.select_save_path = ttk.Button(self.frm, text="Select save path", command=self.save_path).grid(column=5, row=1)
    

        if os.path.isfile("/home/ethanlee/Desktop/crop_tool_saved_list.txt"):
            # load contents of saved image list into self.image_list
            with open("/home/ethanlee/Desktop/crop_tool_saved_list.txt", "r") as g:
                self.image_list = g.read().splitlines()
                print(self.image_list)
                self.label.configure(text="Save file loaded into memory.")

                self.img = Image.open(self.image_list[self.image_counter])
                self.render = ImageTk.PhotoImage(self.img)

                width,height=self.img.size
                print("DDDDDDD", self.render.width(), self.render.height())
                self.image_window.config(scrollregion=(0,0,self.render.width(),self.render.height()))
                
                ## create image on canvas
                self.hbar.config(command=self.image_window.xview)
                self.vbar.config(command=self.image_window.yview)
                self.image_window.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
                self.image_window.pack(side=LEFT, expand=YES, fill=BOTH)
                self.created_image = self.image_window.create_image(0,0,anchor='nw', image=self.render)

    def click(self, event):
        if not self.rect:
            x0 = self.image_window.canvasx(event.x) - 75
            y0 = self.image_window.canvasy(event.y) - 75
            x1 = self.image_window.canvasx(event.x) + 75
            y1 = self.image_window.canvasy(event.y) + 75
            #print(self.image_window.canvasx(event.x), event.x)
            self.dimensions = (int(x0),int(y0),int(x1),int(y1))
            self.rect = self.image_window.create_rectangle(x1, y1, x0, y0, fill="", outline="red")
            print(self.dimensions)
        else:
            self.image_window.delete(self.rect)
            self.rect = None
            #return
    def save_img(self):
        new_img = self.img.crop(self.dimensions)
        out_index = self.image_list[self.image_counter].rindex("Salvadorperu-")
        print(self.image_list[self.image_counter][out_index:])
        #new_img.save(self.save_img_path + "/" + str(self.image_counter) + ".png")
        # if not self.save_img_path:
        #     print("ok")
        print(self.save_img_path + "/" + self.image_list[self.image_counter][out_index:])
        try:
            new_img.save(self.save_img_path + "/" + "fallen_" + self.image_list[self.image_counter][out_index:])
        except AttributeError:
            self.label.configure(text="No save path is configured. Please do so now.")

    def next_img(self):
        ## No more images in directory. Reached the end.
        ## TODO save image counter into save file and load into memory upon opening
        if self.image_counter > len(self.image_list):
            self.label.configure(text="No more images. You have reached the end.")
            return
        print(self.image_list[self.image_counter])
        self.image_counter += 1
        self.img = Image.open(self.image_list[self.image_counter])
        self.render = ImageTk.PhotoImage(self.img)
        self.image_window.create_image(0,0,anchor="nw", image=self.render)
        pass
    def load_directory(self):
        self.image_directory = filedialog.askdirectory()
        #print(image_directory)
        #print(glob.glob(self.image_directory + "/*.jpg"))
        self.image_list = sorted(glob.glob(self.image_directory + "/*.png"))
        print(self.image_directory)
        print(self.image_list)
        print(self.image_counter)
        self.img = Image.open(self.image_list[self.image_counter])
        self.render = ImageTk.PhotoImage(self.img)

        width,height=self.img.size
        print("DDDDDDD", self.render.width(), self.render.height())
        self.image_window.config(scrollregion=(0,0,self.render.width(),self.render.height()))
        
        ## create image on canvas
        self.hbar.config(command=self.image_window.xview)
        self.vbar.config(command=self.image_window.yview)
        self.image_window.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.image_window.pack(side=LEFT, expand=YES, fill=BOTH)
        self.created_image = self.image_window.create_image(0,0,anchor='nw', image=self.render)

    def save_path(self):
        self.save_img_path = filedialog.askdirectory()
        print(self.save_img_path + "/" + str(self.image_counter) + ".png")

    def save_exit(self):
        # slice list of images to make new list
        # save new list to text file
        
        if os.path.isfile("/home/ethanlee/Desktop/crop_tool_saved_list.txt"):
            self.label.configure(text="save file already exists")
            #self.label['text'] = "save file already exists"
            return
        self.image_list = self.image_list[self.image_counter:]
        with open('/home/ethanlee/Desktop/crop_tool_saved_list.txt', 'w+') as f:
            for i in self.image_list:
                f.write(f"{i}\n")

    def delete_save_file(self):
        if os.path.isfile("/home/ethanlee/Desktop/crop_tool_saved_list.txt"):
            os.remove("/home/ethanlee/Desktop/crop_tool_saved_list.txt")
        else:
            self.label.configure(text="No save file to delete. Please create one.")
            return



if __name__ == "__main__":
    app = Tk()
    app.title("Image classification cropper")
    crop = Crop(parent=app)
    crop.mainloop()