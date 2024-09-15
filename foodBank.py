import tkinter as tk
from tkinter import ttk
import tkinter.font as tkF
import webbrowser

# Food bank data
food_banks = {
    "Hayward": {
        'South Hayward Parish': {
            "address": '27287 Patrick Ave, Hayward, CA 94544',
            "website": 'https://www.southhaywardparish.org/'
        },
        'Hope 4 the Heart': {
            'address': '22035 Meekland Ave, Hayward, CA 94541',
            'website': 'https://hope4theheart.org/'
        },
    },

    "San Leandro": {
        'David Street': {
            "address": '3081 Teagarden St, San Leandro, CA 9457',
            "website": 'https://davisstreet.org/basic-needs/'
        },
    },

    'Oakland': {
        'Alameda County COmmunity Food Bank': {
            'address': '7900 Edgewater Dr, Oakland, CA 94621',
            'website': 'https://www.accfb.org/',
        },   
    },
    
    "San Jose": {
        "Second Harvest of Silicon Valley (San Jose)": {
            "address": '4001 N 1st St, San Jose, CA 95134',
            "website": 'https://plannedgiving.shfb.org/contact-us',
        },
        'Second Harvest of Silicon Valley Brennan': {
            "address": '528 Brennan St, San Jose, CA',
            "website": 'https://www.shfb.org/give-help/volunteer/volunteer-urgent/?', 
        },
    },
    
    "San Carlos": {
        'Second Harvest of Silicon Valley (San Carlos)': {
            "address": '1051 Bing St, San Carlos, CA 94070',
            "website": 'https://www.shfb.org/',
        },
    },
    
    "Palo Alto": {
        'South Palo Alto Food Center': {
            "address": '670 E Meadow Dr Ste 9, Palo Alto, CA 94306',
            "website": 'https://www.southpaloaltofoodcloset.com/',
        },
    },
}

# Dictionary for translations
translations = {
    "eng": {
        "title": "Food Banks Locator",
        "choose_city": "Choose your city",
        "search": "Search Food Bank",
        "language": "Language",
        "food_banks_nearby": "Food Banks Nearby",
        "view_website": "View Website",
        "view_map": "View on Map",
        "choose_food_bank": "Choose a food bank to view",
        "no_food_banks": "No food banks found in this area"
    },
    
    "esp": {
        "title": "Localizador de bancos de comida",
        "choose_city": "Escoja su ciudad",
        "search": "Buscar banco de comida",
        "language": "Idioma",
        "food_banks_nearby": "Bancos de comida cercanos",
        "view_website": "Visitar pagina web",
        "view_map": "Ver en mapa",
        "choose_food_bank": "Escoja el banco de comida a visitar",
        "no_food_banks": "No hay bancos de comida cercanos"
    }
}


current_lang = "eng" # Default language
selected_address = None # Store selected address for mapping
food_bank_options = {} # Store name-website-address mapping for dropdown selection

def search_food_banks():
    '''Search and display food banks by city'''
    global selected_address
    selected_city = city.get().strip().title()
    results = food_banks.get(selected_city, None)

    if results:
        result_text = translations[current_lang]["food_banks_nearby"] + ":\n"
        food_bank_options.clear() # Clear previous results
        food_bank_dropdown["values"] = [] # Reset dropdown options

        for name, info in results.items():
            address = info["address"]
            result_text += f"{name}: {address}\n"
            food_bank_options[name] = info # Store name and info (address & website) for selection
        
        result_label.config(text=result_text, fg="black", bg ='white')
    
        # Update food bank dropdown optionss
        food_bank_dropdown["values"] = list(food_bank_options.keys())
        food_bank_dropdown.set("") # Clear previous selection
        food_bank_dropdown.pack(pady=10) # Show dropdown 
        website_button.pack(pady=10) # Show website button
        map_button.pack(pady=10) # Show map button

    else:    
        result_label.config(text=translations[current_lang]["no_food_banks"], fg="red")
        food_bank_dropdown.pack_forget() # Hide dropdown if no results
        website_button.pack_forget() # Hide website button if no results
        map_button.pack_forget() # Hide map button if no results

    
    
    
    

def change_language(event=None):
    '''Change language'''
    global current_lang
    selected_lang = language_dropdown.get()
    
    # Change current language based on selection
    current_lang = "esp" if selected_lang == "Spanish" else "eng"

    # Update text based on language
    root.title(translations[current_lang]["title"])
    city_label.config(text=translations[current_lang]["choose_city"])
    search_button.config(text=translations[current_lang]["search"])
    language_label.config(text=translations[current_lang]["language"])
    website_button.config(text=translations[current_lang]["view_website"])
    map_button.config(text=translations[current_lang]["view_map"])
    food_bank_label.config(text=translations[current_lang]["choose_food_bank"])
    result_label.config(text="") # Clear results when switching language

def view_website(): 
    selected_food_bank = food_bank_dropdown.get()
    if selected_food_bank and selected_food_bank in food_bank_options:
        website_url = food_bank_options[selected_food_bank]["website"]
        webbrowser.open(website_url)

def view_on_map():
   selected_food_bank = food_bank_dropdown.get() 
   if selected_food_bank and selected_food_bank in food_bank_options:
       selected_address = food_bank_options[selected_food_bank]["address"]
       url = f"https://www.openstreetmap.org/search?query={selected_address.replace(' ', '%20')}"
       webbrowser.open(url)






# Main UI Window
root = tk.Tk()
root.title(translations[current_lang]["title"])
root.geometry("400x400")
root.configure(background = 'HotPink4')

# FONT
roman_font = tkF.Font(family = 'Times New Roman', size = 24)

# Language selection label
language_label = tk.Label(root, text=translations[current_lang]["language"], font = roman_font, bg = 'white')
language_label.configure(fg = 'black')
language_label.pack(pady=10)

# Language selection dropdown 
language = tk.StringVar()
language_dropdown = ttk.Combobox(root, textvariable=language, values=["English", "Spanish"], state="readonly")
language_dropdown.set("English") # Set default language to English
language_dropdown.pack(pady=10)
language_dropdown.bind("<<ComboboxSelected>>", change_language)

# City selection label
city_label = tk.Label(root, text=translations[current_lang]["choose_city"], font = roman_font, bg = 'white', fg = 'black')
city_label.pack(pady=10)

# City selection dropdown
city = tk.StringVar()
city_dropdown = ttk.Combobox(root, textvariable=city, values=list(food_banks.keys()), state="readonly")
city_dropdown.pack(pady=10)


# Search button
search_button = tk.Button(root, text=translations[current_lang]["search"], command=search_food_banks, bg = 'white', fg = 'black') # MAKE FUNCTION FOR COMMAND
search_button.pack(pady=10)

# Show search result directly within window
result_label = tk.Label(root, text="", justify="left", wraplength=380)
result_label.pack(pady=10, padx=10)

# Food bank selection label
food_bank_label = tk.Label(root, text=translations[current_lang]["choose_food_bank"], bg = 'white', fg = 'black')
food_bank_label.pack(pady=10)

# Food bank dropdown (initially hidden)
food_bank_dropdown = ttk.Combobox(root, state="read only")
food_bank_dropdown.pack_forget() # Display only after search results

# View website button (initially hidden)
website_button = tk.Button(root, text=translations[current_lang]["view_website"], command = view_website) 
website_button.pack_forget() # Display only after search results

# View map button (initially hidden)
map_button = tk.Button(root, text=translations[current_lang]["view_map"], command=view_on_map) 
map_button.pack_forget() # Display only after search results

root.mainloop()