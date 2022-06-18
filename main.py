from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk

from RequestManager import RequestManager
from ApiBridge import ApiBridge


root = Tk()
root.title('Pakerszama Image Uploader')
root.geometry('800x480')
root.resizable(False, False)
root.attributes('-topmost', 0)

# Polacz z API
requests = RequestManager(url='https://api.pakerszama.pl/')
api = ApiBridge(request_manager=requests,
                auth_token='')

meals = api.get_meals()


# Podziel posiłki na te z oraz na te bez zdjęć
meals_without_img = []
meals_with_img = []

for meal in meals:
    if meal.get('image'):
        meals_with_img.append(meal)
    else:
        meals_without_img.append(meal)


def populates_listboxes():
    # Dodaj posiłki bez zdjęć
    for meal in meals_without_img:
        no_img_meals_listbox.insert(END, meal['title'])

    # Dodaj posiłki ze zdjęciem
    for meal in meals_with_img:
        print(meal)
        img_meals_listbox.insert(END, meal['title'])


# Stwórz Listbox dla posiłków bez zdjęcia
no_img_label = Label(root, text='Do zrobienia')
no_img_label.pack(pady=10)

no_img_meals_listbox = Listbox(root, width=80)
no_img_meals_listbox.pack(pady=15)


def upload_embed_id(embed_id):
    print("EMBED ID:", embed_id)


def upload_to_meal(yt_link):
    print(yt_link)

def select_image():
    global img
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = ImageTk.PhotoImage(file=filename)

    return img

def popup(meal_title):
    global pop
    pop = Toplevel(root)
    pop.title('Dodaj zdjęcie i filmik')
    pop.geometry("400x200")

    # create a Form label
    heading = Label(pop, text=meal_title, bg="light green")

    # create a Name label
    yt_link_label = Label(pop, text="Link", bg="light green")

    # create a Course label
    image_label = Label(pop, text="Zdjęcie", bg="light green")

    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    heading.grid(row=0, column=1)
    yt_link_label.grid(row=1, column=0)
    image_label.grid(row=2, column=0)

    # create a text entry box
    # for typing the information
    yt_link_field = Entry(pop)
    image_button = Button(pop, text='Otwórz', command=lambda:select_image())

    yt_link_field.grid(row=1, column=1, ipadx="100")
    image_button.grid(row=2, column=1, ipadx="100")

    submit = Button(pop, text="Wyślij", command=lambda: upload_to_meal(
        yt_link=yt_link_field.get())
    )
    submit.grid(row=8, column=0)


def onselect(evt):
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)

    popup(value)
    print('You selected item %d: "%s"' % (index, value))


no_img_meals_listbox.bind('<Double-Button>', onselect)

# Stwórz Listbox dla posiłków ze zdjęciem
img_label = Label(root, text='Gotowe')
img_label.pack(pady=10)

img_meals_listbox = Listbox(root, width=80)
img_meals_listbox.pack(pady=15)


populates_listboxes()
root.mainloop()
