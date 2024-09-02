from terminal_menu import display_menu, clean_screen

def upload_data():
    print("Uploading data...")
    print("Data uploaded successfully!")

def display_data():
    print("Displaying the new data...")
        
    print("Data displayed successfully!")

def main():

    products.to_csv('products.csv')




    # Loading options
    options = {
        "Upload data": upload_data,
        "Display data": display_data,
    }

    
    # while True:
    #     try:
    #         display_menu(options=options)
    #     except SystemExit:
    #         break

if __name__ == '__main__':
    main()
