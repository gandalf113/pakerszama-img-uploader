from tkinter import *
from PatchMealWindow import PatchMealWindow

from RequestManager import RequestManager
from ApiBridge import ApiBridge


root = Tk()
root.title('Pakerszama Image Uploader')
root.geometry('800x480')
root.resizable(False, False)
root.attributes('-topmost', 0)

# Connect to API
requests = RequestManager(url='https://api.pakerszama.pl/')
api = ApiBridge(request_manager=requests,
                auth_token='')

meals = api.get_meals()


# Split the meals for those with and without images
meals_without_img = []
meals_with_img = []

for meal in meals:
    if meal.get('image'):
        meals_with_img.append(meal)
    else:
        meals_without_img.append(meal)


def populates_listboxes():
    # Add meals with no image
    for meal in meals_without_img:
        no_img_meals_listbox.insert(END, meal['title'])

    # Add meals with image
    for meal in meals_with_img:
        print(meal)
        img_meals_listbox.insert(END, meal['title'])


# Create Listbox dla meals WITHOUT image
no_img_label = Label(root, text='Do zrobienia')
no_img_label.pack(pady=10)

no_img_meals_listbox = Listbox(root, width=80)
no_img_meals_listbox.pack(pady=15)


def upload_embed_id(embed_id):
    print("EMBED ID:", embed_id)


def onselect(evt):
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)

    popup = PatchMealWindow(root=root, meal=value)
    print('You selected item %d: "%s"' % (index, value))


no_img_meals_listbox.bind('<Double-Button>', onselect)

# Create the Listbox for meals with image
img_label = Label(root, text='Gotowe')
img_label.pack(pady=10)

img_meals_listbox = Listbox(root, width=80)
img_meals_listbox.pack(pady=15)


populates_listboxes()
root.mainloop()
