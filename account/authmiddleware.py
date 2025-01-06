import jwt
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        token = parse_qs(query_string).get("token", [None])[0]

        if token:
            try:
                # Validate the token
                UntypedToken(token)
                decoded_token = jwt.decode(token, options={"verify_signature": False})
                user_id = decoded_token.get("user_id")

                # Use a synchronous function with sync_to_async
                scope["user"] = await database_sync_to_async(self.get_user)(user_id)
            except (InvalidToken, jwt.ExpiredSignatureError, jwt.DecodeError):
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        # Pass the updated scope to the inner application
        return await self.inner(scope, receive, send)

    @staticmethod
    def get_user(user_id):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
