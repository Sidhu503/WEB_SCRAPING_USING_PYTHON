import csv
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Mapping dictionary for rating levels
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def scrape_website():
    # Get the URL from the user
    url = entry_url.get()

    # Prepare data list
    data = []

    # Iterate over page numbers
    for page_num in range(1, 6):  # Scrape up to 5 pages
        # Construct the URL for each page
        page_url = f"{url}/catalogue/page-{page_num}.html"


        # Send a GET request to the page
        response = requests.get(page_url)

        # Create BeautifulSoup object
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all book containers
        book_containers = soup.find_all("article", class_="product_pod")

        # Extract book information
        for container in book_containers:
            # Extract title
            title = container.h3.a["title"]

            # Extract price
            price = container.find("p", class_="price_color").text.replace("£", "")


            # Extract rating
            rating_class = container.find("p", class_="star-rating")["class"][-1]
            rating = rating_map.get(rating_class)

            # Extract availability
            availability = container.find("p", class_="instock availability").text.strip()

            # Add book data to the list
            data.append((title, price, rating, availability))

    # Sort the data based on the selected sorting option
    sort_option = var_sort_option.get()
    if sort_option == "Price - Lowest to Highest":
        data.sort(key=lambda x: float(x[1]))
    elif sort_option == "Price - Highest to Lowest":
        data.sort(key=lambda x: float(x[1]), reverse=True)
    elif sort_option == "Rating - Lowest to Highest":
        data.sort(key=lambda x: x[2])
    elif sort_option == "Rating - Highest to Lowest":
        data.sort(key=lambda x: x[2], reverse=True)
    elif sort_option == "Availability of Stock":
        data.sort(key=lambda x: x[3])

    # Prompt the user to select a file for saving
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filename:
        # Write data to a CSV file
        with open(filename, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Title", "Price", "Rating", "Availability"])  # Write header row
            writer.writerows(data)  # Write book data rows

        messagebox.showinfo("Success", f"Scraped data saved to {filename}.")
    else:
        messagebox.showinfo("Error", "No file selected.")

# Create the tkinter window
window = tk.Tk()
window.title("Web Scraping Tool")

# Create a label and an entry for URL
label_url = tk.Label(window, text="Enter the URL:")
label_url.pack()
entry_url = tk.Entry(window, width=50)
entry_url.pack()

# Create a frame for sort options
frame_sort_options = tk.LabelFrame(window, text="Sort Options")
frame_sort_options.pack()

# Create a variable to store the selected sort option
var_sort_option = tk.StringVar()
var_sort_option.set("Price - Lowest to Highest")

# Create buttons for sort options
btn_price_asc = tk.Radiobutton(frame_sort_options, text="Price - Lowest to Highest", variable=var_sort_option, value="Price - Lowest to Highest")
btn_price_asc.pack(anchor=tk.W)
btn_price_desc = tk.Radiobutton(frame_sort_options, text="Price - Highest to Lowest", variable=var_sort_option, value="Price - Highest to Lowest")
btn_price_desc.pack(anchor=tk.W)
btn_rating_asc = tk.Radiobutton(frame_sort_options, text="Rating - Lowest to Highest", variable=var_sort_option, value="Rating - Lowest to Highest")
btn_rating_asc.pack(anchor=tk.W)
btn_rating_desc = tk.Radiobutton(frame_sort_options, text="Rating - Highest to Lowest", variable=var_sort_option, value="Rating - Highest to Lowest")
btn_rating_desc.pack(anchor=tk.W)
btn_availability = tk.Radiobutton(frame_sort_options, text="Availability of Stock", variable=var_sort_option, value="Availability of Stock")
btn_availability.pack(anchor=tk.W)

# Create a button to start scraping
btn_scrape = tk.Button(window, text="Scrape", command=scrape_website)
btn_scrape.pack()

# Run the tkinter event loop
window.mainloop()
