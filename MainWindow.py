from tkinter import *
from PatchMealWindow import PatchMealWindow


class MainWindow:
    def __init__(self, api) -> None:
        global root
        root = Tk()
        root.title('Pakerszama Image Uploader')
        root.iconbitmap('favicon.ico')
        root.geometry('800x480')
        root.resizable(False, False)
        root.attributes('-topmost', 0)

        self.api = api

        self.render()

        self.populates_listboxes()
        root.mainloop()

    def get_meals(self):
        # Get the meal list from API
        meals = self.api.get_meals()

        # Split the meals for those with and without images
        meals_without_img = []
        meals_with_img = []

        # Assign each meal to appropriate list
        for meal in meals:
            if meal.get('image'):
                meals_with_img.append(meal)
            else:
                meals_without_img.append(meal)

        return meals_without_img, meals_with_img

    def render(self):
        # Create Listbox dla meals WITHOUT image
        no_img_label = Label(root, text='Do zrobienia')
        no_img_label.pack(pady=10)

        self.no_img_meals_listbox = Listbox(root, width=80)
        self.no_img_meals_listbox.pack(pady=15)

        self.no_img_meals_listbox.bind('<Double-Button>', self.onselect)

        # Create the Listbox for meals with image
        img_label = Label(root, text='Gotowe')
        img_label.pack(pady=10)

        self.img_meals_listbox = Listbox(root, width=80)
        self.img_meals_listbox.pack(pady=15)

        self.img_meals_listbox.bind('<Double-Button>', self.onselect)

    def populates_listboxes(self) -> None:
        meals_without_img, meals_with_img = self.get_meals()

        # First clear the listboxes
        self.no_img_meals_listbox.delete(0, END)
        self.img_meals_listbox.delete(0, END)

        # Add meals with no image
        for meal in meals_without_img:
            self.no_img_meals_listbox.insert(END, self.title_encode(meal))

        # Add meals with image
        for meal in meals_with_img:
            self.img_meals_listbox.insert(END, self.title_encode(meal))

    def title_encode(self, meal: dict) -> str:
        # Encode the title to store both title and id
        # It will look something like this:
        # 1!&& Chicken and Rice

        meal_id = meal['id']
        title = meal['title']

        # !&&   is the string separating id from title
        return f"{meal_id}!& - {title}"

    def onselect(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)

        # Show new window
        return PatchMealWindow(root=root, meal=value,
                                refresh_meals=lambda: self.populates_listboxes())
