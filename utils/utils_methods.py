import uuid
import os
import subprocess

import psutil


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
        # Iterar sobre todos los procesos activos
        for proc in psutil.process_iter(attrs=["name"]):
            # Verificar si el nombre del proceso coincide
            if proc.info["name"] and proc.info["name"].lower() == task_name.lower():
                # Forzar el cierre del proceso
                proc.kill()
                print(f"Proceso {task_name} forzado a cerrarse.")
    except psutil.NoSuchProcess:
        print(f"El proceso {task_name} no existe.")
    except Exception as e:
        print(f"Ocurrió un error al intentar terminar el proceso {task_name}: {e}")

# system UUID getting function
def get_system_uuid():
    return uuid.UUID(int=uuid.getnode()).hex


