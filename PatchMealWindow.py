from multiprocessing.dummy import Value
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from ApiBridge import ApiBridge

from RequestManager import RequestManager


class PatchMealWindow:
    def __init__(self, root, meal_title, meal_id) -> None:
        global pop
        pop = Toplevel(root)
        pop.title('Dodaj zdjęcie i filmik')
        pop.geometry("400x350")

        self.load_preview_image('image.jpg')

        self.popup(window=pop, meal_title=meal_title, meal_id=meal_id)

        # Connect to API
        requests = RequestManager(url='http://127.0.0.1:8000/')
        self.api = ApiBridge(request_manager=requests,
                             auth_token='d32d5137658b0a1603bbff7ff0e3f72a9a8ba632')

    def load_preview_image(self, path: str):
        # Set the default preview image
        image = (Image.open(path))

        # Resize the photo for preview
        image = image.resize((320, 180), Image.ANTIALIAS)
        self.preview_image = ImageTk.PhotoImage(image=image)

        return image

    def popup(self, window, meal_title, meal_id):
        # Title section
        title_label = Label(window, text="Tytuł", bg="light green")
        title = Label(window, text=meal_title, bg="light green")
        title_label.grid(row=0, column=0)
        title.grid(row=0, column=1)

        # Length days section
        len_days_label = Label(window, text="Ilość dni", bg="light green")
        len_days_field = Entry(window)

        len_days_label.grid(row=1, column=0, pady=5)
        len_days_field.grid(row=1, column=1, ipadx="100")

        # YouTube link section
        yt_link_label = Label(window, text="Link", bg="light green")
        yt_link_field = Entry(window)
        yt_link_label.grid(row=2, column=0, pady=5)
        yt_link_field.grid(row=2, column=1, ipadx="100")

        # Image section
        image_label = Label(window, text="Zdjęcie", bg="light green")
        image_button = Button(window, text="Otwórz",
                              command=lambda: self.select_image())

        image_label.grid(row=3, column=0)
        image_button.grid(row=3, column=1, ipadx="100")

        # Image preview section
        self.img_preview = Label(window, image=self.preview_image)
        self.img_preview.grid(row=4, column=1, pady=15)

        # Submit section
        submit = Button(
            window,
            text="WYŚLIJ",
            width=40,
            command=lambda:
            self.upload_to_meal(
                yt_link=yt_link_field.get(),
                image=self.image_path,
                len_days=len_days_field.get()
            )
        )
        submit.grid(row=8, column=1)

    def upload_to_meal(self, yt_link, image, len_days):
        print("LINK:", yt_link)
        print("IMAGE:", image)
        print("LENGTH DAYS:", len_days)

        try:
            len_days = int(len_days)
            self.api.upload_image(
                meal_id=287,
                image_path=self.image_path
            )
        except ValueError as error:
            print(error)
        except Exception as error:
            print(error)

    def select_image(self):
        f_types = [('Jpg Files', '*.jpg')]
        # Open the file selection dialog
        filename = filedialog.askopenfilename(filetypes=f_types, parent=pop)

        # Get the selected photo
        # image = Image.open(filename)

        self.load_preview_image(filename)

        # Resize the photo for preview
        # self.preview_image = image.resize((320, 180), Image.ANTIALIAS)
        # self.preview_image = ImageTk.PhotoImage(image=self.preview_image)

        # Set the image in preview display
        self.img_preview.config(image=self.preview_image)

        # Prepare the photo for uploading
        self.image_path = filename
