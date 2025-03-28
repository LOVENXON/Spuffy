import uuid

def get_system_uuid():
    return uuid.UUID(int=uuid.getnode()).hex

uuid_value = get_system_uuid()
print(f"UUID del sistema: {uuid_value}")
