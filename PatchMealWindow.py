from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk


class PatchMealWindow:
    def __init__(self, root, meal) -> None:
        global pop
        pop = Toplevel(root)
        pop.title('Dodaj zdjęcie i filmik')
        pop.geometry("400x300")

        self.img = ImageTk.PhotoImage(Image.open("image.jpg"))

        self.popup(window=pop, meal_title=meal)

    def popup(self, window, meal_title):
        # Title section
        heading = Label(window, text=meal_title, bg="light green")
        heading.grid(row=0, column=1)

        # YouTube link section
        yt_link_label = Label(window, text="Link", bg="light green")
        yt_link_field = Entry(window)
        yt_link_label.grid(row=1, column=0)
        yt_link_field.grid(row=1, column=1, ipadx="100")


        # Image section
        image_label = Label(window, text="Zdjęcie", bg="light green")
        image_button = Button(window, text="Otwórz",
                              command=lambda: self.select_image())


        image_label.grid(row=2, column=0)
        image_button.grid(row=2, column=1, ipadx="100")

        # Image preview section
        preview_label = Label(window, text="Podgląd", bg="light green")
        self.img_preview = Label(window, image=self.img)

        self.img_preview.grid(row=3, column=1)
        preview_label.grid(row=3, column=0)

        # Submit section
        submit = Button(
            window, text="Wyślij",
            command=lambda:
            self.upload_to_meal(
                yt_link=yt_link_field.get(),
                image=self.img,
                len_days=69
            )
        )
        submit.grid(row=8, column=1, columnspan=2)

    def upload_to_meal(self, yt_link, image, len_days):
        print("LINK:", yt_link)
        print("IMAGE:", image)
        print("LENGTH DAYS:", len_days)

    def select_image(self):
        f_types = [('Jpg Files', '*.jpg')]
        # Open the file selection dialog
        filename = filedialog.askopenfilename(filetypes=f_types, parent=pop)

        # Get the selected photo
        image = Image.open(filename)

        # Resize the photo
        image = image.resize((320, 180), Image.ANTIALIAS)

        # Set the image in display
        self.img = ImageTk.PhotoImage(image=image)
        self.img_preview.config(image=self.img)

        print(filename)

        # self.img = img
