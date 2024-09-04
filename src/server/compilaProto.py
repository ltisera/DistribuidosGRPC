import subprocess
import os

def compile_proto():
    proto_dir = "../protos"  # Directorio donde están los archivos .proto
    proto_files = [f for f in os.listdir(proto_dir) if f.endswith(".proto")]  # Encuentra todos los .proto

    for proto in proto_files:
        command = [
            "python", "-m", "grpc_tools.protoc",
            f"-I{proto_dir}",  # Directorio de importación
            "--python_out=../protos",  # Salida de los archivos .py generados
            "--grpc_python_out=../protos",  # Salida de los archivos .py para gRPC
            os.path.join(proto_dir, proto)  # Ruta completa del archivo .proto
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Archivo {proto} compilado exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al compilar el archivo {proto}: {e}")

if __name__ == "__main__":
    compile_proto()