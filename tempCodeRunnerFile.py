import tkinter as tk
import basic
def generate_string():
    input_string = entry.get()
    result,error=basic.run('<stdin>',input_string)
    if error:
        print(error.as_string())
    else:
        output_label.config(text=result)
    

# Create the main window
root = tk.Tk()
root.title("String Generator")

# Create a label and entry widget for input
label = tk.Label(root, text="Enter a string:")
label.pack(pady=10)
entry = tk.Entry(root)
entry.pack(pady=5)

# Create a button to generate the string
generate_button = tk.Button(root, text="Generate", command=generate_string)
generate_button.pack(pady=5)

# Create a label to display the generated string
output_label = tk.Label(root, text="")
output_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
