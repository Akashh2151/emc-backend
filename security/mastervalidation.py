


def validate_unauthorized_access(user_id_from_header):
    """
    Validate unauthorized access.
    """
    if not user_id_from_header:
        return False, 'Unauthorized access: User ID is required in the header'
    
    # You can add more checks if needed

    return True, None



def validate_user_found(user):
    """
    Validate if the user is found.
    """
    if not user:
        return False, 'Unauthorized access: User not found'

    # You can add more checks if needed

    return True, None



def validate_no_blank_spaces(updated_master):
    """
    Validate for blank spaces in keys and values.
    """
    if any(k.strip() == '' or v and isinstance(v, str) and v.strip() == '' for k, v in updated_master.items()):
        return False, 'Keys or values cannot have blank spaces'

    # You can add more checks if needed

    return True, None



def validate_no_blank_space_keys_dict(updated_master):
    """
    Validate for blank spaces in keys of a dictionary.
    """
    if any(key.strip() == '' for key in updated_master):
        return False, 'Keys cannot have blank spaces'

    # You can add more checks if needed

    return True, None

 



def validate_no_blank_space_values(updated_master):
    """
    Validate for blank spaces in string values.
    """
    
    for key, value in updated_master.items():
        # Skip the validation for the key "values"
        if key == "values":
            continue
        if isinstance(value, str) and value.strip() == '':
            return False, f'Value for key "{key}" cannot be blank'

        # You can add more checks if needed

    return True, None



def validate_status_not_default(updated_master):
    """
    Validate that the status value is not 'default'.
    """
    status_value = updated_master.get('status', '').lower()
    if status_value == 'default':
        return False, 'You cannot update with status as default'

    # You can add more checks if needed

    return True, None



def validate_is_active_boolean(updated_master):
    """
    Validate that 'isActive' is a boolean.
    """
    is_active_value = updated_master.get('isActive')
    if not isinstance(is_active_value, bool):
        return False, "'isActive' must be a boolean"

    # You can add more checks if needed

    return True, None