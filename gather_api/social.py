from gather_api.models import User

def save_uid(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        print(response)
        print(user)
        user.social_id = response.get('id')
        user.email = response.get('email')
        user.save()
