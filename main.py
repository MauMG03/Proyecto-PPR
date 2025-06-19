import tkinter as tk
from datetime import timedelta
from pathlib import Path
from tkinter import filedialog, ttk, messagebox

from minizinc import Model, Solver, Instance


class PlanificadorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Planificación de Ensayos")
        self.geometry("400x350")
        self.resizable(False, False)

        self.modelo_version = tk.StringVar()
        self.archivo_path = tk.StringVar()
        self.tiempo_maximo = tk.StringVar(value="5")

        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Label(self, text="Seleccione la versión del modelo:").pack(pady=(10, 0))
        versiones = ["Parte 1", "Parte 2"]
        self.combo_modelo = ttk.Combobox(self, values=versiones, textvariable=self.modelo_version, state="readonly")
        self.combo_modelo.current(0)
        self.combo_modelo.pack()

        ttk.Label(self, text="Seleccione archivo .dzn:").pack(pady=(20, 0))
        ttk.Button(self, text="Cargar archivo", command=self.cargar_archivo).pack()
        self.label_archivo = ttk.Label(self, textvariable=self.archivo_path, wraplength=400, foreground="gray")
        self.label_archivo.pack()

        ttk.Label(self, text="Tiempo máximo de ejecución (minutos):").pack(pady=(20, 0))
        ttk.Entry(self, textvariable=self.tiempo_maximo, width=10).pack()

        ttk.Button(self, text="Ejecutar modelo", command=self.ejecutar_modelo).pack(pady=30)

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo .dzn",
            filetypes=[("MiniZinc data files", "*.dzn")],
            initialdir="./pruebas/campus/"
        )
        if archivo:
            self.archivo_path.set(archivo)

    def ejecutar_modelo(self):
        if not self.modelo_version.get():
            messagebox.showerror("Error", "Debe seleccionar una versión del modelo.")
            return
        if not self.archivo_path.get():
            messagebox.showerror("Error", "Debe seleccionar un archivo de entrada (.dzn).")
            return
        try:
            minutos = int(self.tiempo_maximo.get())
            if minutos <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El tiempo máximo debe ser un número entero positivo.")
            return
        version_modelo = 'p1' if self.modelo_version.get() == 'Parte 1' else 'p2'
        modelo_path = f"./modelos/modelo-{version_modelo}_mmg.mzn"
        modelo = Model(modelo_path)
        archivo_dzn = Path(self.archivo_path.get())

        print(f"Modelo: {modelo_path}")
        print(f"Archivo de entrada: {archivo_dzn}")
        print(f"Tiempo máximo: {minutos} minutos")

        modelo.add_file(archivo_dzn)
        solver = Solver.lookup("gecode")
        instance = Instance(solver, modelo)
        time_limit = timedelta(minutes=minutos)
        output = instance.solve(verbose=True, debug_output=Path("debug_output.txt"), time_limit=time_limit)
        print(output, output["pos"])

        archivo_salida_nombre = archivo_dzn.stem + f"_{version_modelo}_salida.txt"
        archivo_salida = archivo_dzn.with_name(archivo_salida_nombre)
        orden_final = output["pos"]
        costo_total = output["costos"]
        with open(archivo_salida, "w") as f:
            salida = " ".join(map(str, orden_final)) + f" {costo_total}"
            f.write(salida)
        salida += "\n"
        for orden, escena in enumerate(orden_final[:3], start=1):
            salida += f"Escena {escena} en posición {orden}, "
        salida += f"etc. Costo de la solución ${costo_total * 100000:,}."
        messagebox.showinfo("Listo", salida + f"\nArchivo de salida \"{archivo_salida_nombre}\" guardado.")


if __name__ == "__main__":
    app = PlanificadorApp()
    app.mainloop()
