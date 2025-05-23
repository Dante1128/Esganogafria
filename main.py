import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pygame
import numpy as np
import wave
import struct
import os
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Diccionario de frecuencias
frecuencias = {
    'A': 440.00, 'B': 493.88, 'C': 523.25, 'D': 587.33,
    'E': 659.25, 'F': 698.46, 'G': 783.99, 'H': 880.00,
    'I': 987.77, 'J': 1046.50, 'K': 1174.66, 'L': 1318.51,
    'M': 1396.91, 'N': 1567.98, 'O': 1760.00, 'P': 1975.53,
    'Q': 2093.00, 'R': 2349.32, 'S': 2637.02, 'T': 2793.83,
    'U': 3135.96, 'V': 3520.00, 'W': 3951.07, 'X': 4186.01,
    'Y': 4698.63, 'Z': 5274.04
}

def generar_nota(frecuencia, duracion=0.4, volumen=0.5): 
    framerate = 44100
    amplitud = 32767 * volumen
    num_muestras = int(duracion * framerate)
    t = np.linspace(0, duracion, num_muestras, False)
    onda = np.sin(frecuencia * t * 2 * np.pi)
    onda = (amplitud * onda).astype(np.int16)
    return onda

def texto_a_musica(texto, ruta_guardado):
    texto = texto.upper()
    onda_total = []

    for letra in texto:
        if letra in frecuencias:
            onda = generar_nota(frecuencias[letra])
            silencio = np.zeros(int(44100 * 0.1), dtype=np.int16)
            onda_total.extend(onda)
            onda_total.extend(silencio)

    archivo = wave.open(ruta_guardado, "w")
    archivo.setnchannels(1)
    archivo.setsampwidth(2)
    archivo.setframerate(44100)

    for muestra in onda_total:
        archivo.writeframes(struct.pack('<h', muestra))

    archivo.close()

    with open("mensaje.txt", "w") as f:
        f.write(texto)

    audio_a_imagen(ruta_guardado)

def reproducir_musica(nombre_archivo):
    pygame.mixer.init()
    pygame.mixer.music.load(nombre_archivo)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def audio_a_imagen(archivo_wav):
    tasa, data = wavfile.read(archivo_wav)
    if len(data.shape) > 1:
        data = data[:, 0]

    tiempo = np.linspace(0, len(data) / tasa, num=len(data))

    # 🎨 Imagen artística basada en gráfico de barras
    plt.figure(figsize=(10, 5))
    plt.bar(np.arange(len(data)), data, color=np.random.rand(3,), alpha=0.7)
    plt.title("Gráfico de Barras de la Onda", fontsize=16, color='white')
    plt.gca().set_facecolor('black')
    plt.axis('off')
    plt.savefig("grafico_barras.png", bbox_inches='tight', pad_inches=0)
    plt.close()

def generar():
    texto = entry.get()
    if texto.strip() == "":
        messagebox.showwarning("Atención", "Ingresa algún texto.")
        return

    ruta = filedialog.asksaveasfilename(defaultextension=".wav",
                                        filetypes=[("Archivos WAV", "*.wav")],
                                        title="Guardar como")
    if not ruta:
        return

    progress["value"] = 0
    ventana.update_idletasks()

    progress["value"] = 25
    ventana.update_idletasks()

    texto_a_musica(texto, ruta)

    progress["value"] = 75
    ventana.update_idletasks()

    reproducir_musica(ruta)

    progress["value"] = 100
    ventana.update_idletasks()

    messagebox.showinfo("Guardado", "Archivo generado exitosamente y se generaron las imágenes.")
    progress["value"] = 0

def desencriptar():
    try:
        with open("mensaje.txt", "r") as f:
            mensaje = f.read()
    except FileNotFoundError:
        messagebox.showwarning("Error", "No hay ningún mensaje generado aún.")
        return

    ruta = filedialog.askopenfilename(filetypes=[("Archivos WAV", "*.wav")],
                                      title="Selecciona el archivo de audio")
    if not ruta:
        return

    messagebox.showinfo("Texto desencriptado", mensaje)
    reproducir_musica(ruta)

# Interfaz
ventana = tk.Tk()
ventana.title("Texto a Música")
ventana.geometry("400x260")
ventana.configure(bg="#222")

tk.Label(ventana, text="Texto a Música 🎵", font=("Helvetica", 18), fg="white", bg="#222").pack(pady=10)
entry = tk.Entry(ventana, width=40, font=("Helvetica", 12))
entry.pack(pady=5)

# Barra de progreso
progress = ttk.Progressbar(ventana, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

tk.Button(ventana, text="Generar Música", command=generar, bg="green", fg="white", width=20).pack(pady=5)
tk.Button(ventana, text="Desencriptar", command=desencriptar, bg="purple", fg="white", width=20).pack(pady=5)
tk.Button(ventana, text="Salir", command=ventana.destroy, bg="red", fg="white", width=20).pack(pady=5)

ventana.mainloop()
