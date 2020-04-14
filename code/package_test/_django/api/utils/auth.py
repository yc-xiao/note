def jwt_response_payload_handler(token, user=None, request=None, role=None):
    return {
        "authenticated": True,
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'token': token,
    }
