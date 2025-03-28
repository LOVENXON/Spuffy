import jwt
from datetime import datetime, timedelta, timezone

from exec_files.utils import utils_methods

cod_bagay_la = "lovegalaxibyte1025"

# Método para generar JWT
def generate_jwt(username, email, uuid, days_valid=30, subscription='basic'):
    expiration_date = datetime.now(timezone.utc) + timedelta(days=days_valid)
    payload = {
        "username": username,
        "email": email,
        "uuid": uuid,
        "exp": expiration_date,
        "subscription": subscription
    }

    token = jwt.encode(payload, cod_bagay_la, algorithm="HS256")
    return token

# Método para validar JWT
def validate_jwt(token, uuid_client_param):
    try:
        decoded = jwt.decode(token, cod_bagay_la, algorithms=["HS256"])

        expiration_date = datetime.fromtimestamp(decoded['exp'], tz=timezone.utc)
        remaining_days = (expiration_date - datetime.now(timezone.utc)).days
        uuid_client = decoded['uuid']

        if uuid_client != uuid_client_param:
            return {"is_valid": False, "error": "This Token Not Is Valid For This Device"}

        return {
            "is_valid": True,
            "remaining_days": remaining_days,
            "username": decoded["username"],
            "email": decoded["email"],
            "uuid": decoded["uuid"],
            "subscription": decoded["subscription"]
        }
    except jwt.ExpiredSignatureError:
        return {"is_valid": False, "error": "Expired Token"}
    except jwt.InvalidTokenError:
        return {"is_valid": False, "error": "Invalid Token"}

# Ejemplo de uso
if __name__ == '__main__':
    my_uuid__ = utils_methods.get_system_uuid()
    token = generate_jwt("usuario", "usuario@example.com", my_uuid__, days_valid=3, subscription='premium')
    print(f"Token: {token}")
    # Validar el token generado
    result = validate_jwt(token, my_uuid__)
    print(result)
