from multiprocessing.dummy import Value
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo, showerror
from PIL import Image, ImageTk
from ApiBridge import ApiBridge

from RequestManager import RequestManager


class PatchMealWindow:
    def __init__(self, root, meal) -> None:
        global pop
        pop = Toplevel(root)
        pop.title('Zmień przepis')
        pop.iconbitmap('favicon.ico')
        pop.geometry("400x380")
        pop.attributes('-topmost', 1)

        # Load the placeholder for preview
        self.load_preview_image('image.jpg')

        # At first, there is no image to be uploaded
        self.image_path = None

        # Get the title and meal id
        self.meal_id, self.meal_title = self.title_decode(meal)

        self.popup(window=pop)

        # Connect to API
        requests = RequestManager(url='http://127.0.0.1:8000/')
        self.api = ApiBridge(request_manager=requests,
                             auth_token='d32d5137658b0a1603bbff7ff0e3f72a9a8ba632')

    def title_decode(self, encoded_title: str):
        meal_id, title = encoded_title.split('!& - ')
        return meal_id, title

    def load_preview_image(self, path: str):
        # Set the default preview image
        image = (Image.open(path))

        # Resize the photo for preview
        image = image.resize((320, 180), Image.ANTIALIAS)
        self.preview_image = ImageTk.PhotoImage(image=image)

        return image

    def popup(self, window):
        # ID section
        meal_id_label = Label(window, text="ID")
        meal_id = Label(window, text=self.meal_id, bg="light green")
        meal_id_label.grid(row=0, column=0, pady=2, sticky='W')
        meal_id.grid(row=0, column=1, sticky='W')

        # Title section
        title_label = Label(window, text="Tytuł")
        title = Label(window, text=self.meal_title, bg="light green")
        title_label.grid(row=1, column=0, pady=2, sticky='W')
        title.grid(row=1, column=1, sticky='W')

        # Length days section
        len_days_label = Label(window, text="Ilość dni")
        len_days_field = Entry(window)

        len_days_label.grid(row=2, column=0, pady=2, sticky='W')
        len_days_field.grid(row=2, column=1, ipadx="100")

        # YouTube link section
        yt_link_label = Label(window, text="Link")
        yt_link_field = Entry(window)
        yt_link_label.grid(row=3, column=0, pady=5, sticky='W')
        yt_link_field.grid(row=3, column=1, ipadx="100")

        # Image section
        image_label = Label(window, text="Zdjęcie")
        image_button = Button(window, text="Otwórz",
                              command=lambda: self.select_image())

        image_label.grid(row=4, column=0)
        image_button.grid(row=4, column=1, ipadx="100", sticky='W')

        # Image preview section
        self.img_preview = Label(window, image=self.preview_image)
        self.img_preview.grid(row=5, column=1, pady=15)

        # Submit section
        submit = Button(
            window,
            text="WYŚLIJ",
            width=40,
            command=lambda:
            self.upload_to_meal(
                yt_link=yt_link_field.get(),
                len_days=len_days_field.get()
            )
        )
        submit.grid(row=8, column=1)

    def upload_to_meal(self, yt_link, len_days):
        try:
            len_days = int(len_days)
            self.api.upload_image(
                meal_id=self.meal_id,
                image_path=self.image_path
            )

            # Inform of success
            showinfo('Sukces', 'Zaktualizowano przepis')

            # Close the window
            pop.destroy()
            pop.update()
        except ValueError as error:
            showerror('Porażka', 'Długość dni musi być typem int')
        except Exception as error:
            showerror('Porażka', error)

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
