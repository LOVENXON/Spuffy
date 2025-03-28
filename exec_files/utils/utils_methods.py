import uuid
import os
import subprocess



# open executable file
def open_executable(executable_path, executable_name):
    try:
        # Verificar si el archivo existe
        full_path = os.path.join(executable_path, executable_name)
        if not os.path.isfile(full_path):
            print(f"El archivo '{full_path}' no existe.")
            return

        # Abrir el ejecutable
        subprocess.Popen(full_path, shell=True)
        print(f"Ejecutable '{executable_name}' abierto exitosamente.")
    except Exception as e:
        print(f"Ocurrió un error al intentar abrir el ejecutable: {e}")


# force tasks killed
def kill_task_async(task_name):
    try:
        # Ejecutar el comando en un nuevo proceso, sin bloquear la ejecución principal
        subprocess.Popen(
            ["taskkill", "/F", "/IM", task_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
    except Exception:
        # No hacer nada en caso de error
        pass


# system UUID getting function
def get_system_uuid():
    return uuid.UUID(int=uuid.getnode()).hex


