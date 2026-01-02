def configure_server(host, port, **metadata):
    print(f"host:{host}")
    print(f"port:{port}")

    if metadata:
        for key,values in metadata.items():
            print(f"{key}:{values}")



configure_server("192.168.10.0",10,environment="productions",version="1.0")
