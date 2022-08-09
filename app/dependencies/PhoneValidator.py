import re as RegExp

def validate_phone(phone : str) -> bool:

    if len(phone) != 14 : return False

    result = RegExp.match(
        pattern= "\(([0-9]{3})\)[0-9]{4}-[0-9]{4}",
        string = phone
    )
    if result == None : return False
    
    return True






