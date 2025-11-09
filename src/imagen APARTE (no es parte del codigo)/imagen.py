import tkinter as tk
from PIL import Image, ImageTk

ventana = tk.Tk()
ventana.title("Imagen")

#aca pon la ruta de mamboooooo
ruta_imagen = r"C:\Users\ralph\Desktop\mambo.jpg"

imagen = Image.open(ruta_imagen)
foto = ImageTk.PhotoImage(imagen)
label = tk.Label(ventana, image=foto)
label.pack()

ventana.mainloop()

