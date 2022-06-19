from MainWindow import MainWindow
from RequestManager import RequestManager
from ApiBridge import ApiBridge

# Connect to API
requests = RequestManager(url='http://127.0.0.1:8000/')
api = ApiBridge(request_manager=requests,
                auth_token='d32d5137658b0a1603bbff7ff0e3f72a9a8ba632')

# Create the main window
mainWindow = MainWindow(api=api)
