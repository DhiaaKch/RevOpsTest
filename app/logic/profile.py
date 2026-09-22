from app.db import get_user

def get_display_name(user_id: int) -> str:
    user = get_user(user_id)
    # BUG: user can be None, this will raise AttributeError
    return user.display_name.strip()
