import subprocess

def compile_proto():
    command = [
        "python", "-m", "grpc_tools.protoc",
        "-I../protos",  # Directorio de importación
        "--python_out=.",  # Salida de los archivos .py generados
        "--grpc_python_out=.",  # Salida de los archivos .py para gRPC
        "testgrpc.proto"  # Nombre del archivo .proto
    ]


    try:
        subprocess.run(command, check=True)
        print("Archivo .proto compilado exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al compilar el archivo .proto: {e}")

if __name__ == "__main__":
    compile_proto()