from utils.utils_methods import get_system_uuid

code = get_system_uuid()
with open('validate.txt', 'w') as f:
    f.write(code)
