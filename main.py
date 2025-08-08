import ttkbootstrap as tkb
from src.ui.main_window import MainWindow
import os

if __name__ == "__main__":
    root = tkb.Window(themename="darkly")
    
    # --- Lógica para Cargar el Ícono ---
    try:
        # Construye una ruta absoluta al ícono, sin importar desde dónde se ejecute el script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, 'assets', 'logo.ico')

        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
        else:
            print(f"Advertencia: No se encontró el archivo del ícono en: {icon_path}")
    except Exception as e:
        print(f"Error al cargar el ícono: {e}")
        icon_path = "" # Asegurarse de que la ruta esté vacía si falla

    app = MainWindow(root)
    
    # Guardamos la ruta en el estado de la aplicación para que otras ventanas la usen
    if 'icon_path' in locals():
        app.state.icon_path = icon_path

    root.mainloop()