import tkinter as tk
from PIL import Image, ImageTk

ventana = tk.Tk()
ventana.title("Imagen")

# Ruta de tu imagen
ruta_imagen = r"C:\Users\ralph\Desktop\mambo.jpg"

# Cargar y mostrar la imagen
imagen = Image.open(ruta_imagen)
foto = ImageTk.PhotoImage(imagen)
label = tk.Label(ventana, image=foto)
label.pack()

# Iniciar la ventana
ventana.mainloop()
