import strawberry
from asgiref.sync import sync_to_async
from decouple import config
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string
from strawberry.types import Info

from api.common import IsAuthenticated, get_user
from api.types import BasicResult, User


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def login(
        self,
        info: Info,
        username: str,
        password: str,
    ) -> User:
        user = await sync_to_async(authenticate)(username=username, password=password)

        if user is None:
            raise Exception("Invalid credentials")

        await sync_to_async(login)(info.context.request, user)

        return user

    @strawberry.mutation
    async def logout(
        self,
        info: Info,
    ) -> bool:
        await sync_to_async(logout)(info.context.request)

        return True

    @strawberry.mutation
    async def register(
        self,
        info: Info,
        username: str,
        name: str,
        password: str,
    ) -> User:
        UserModel = get_user_model()

        split_name = name.rpartition(" ")
        user = UserModel(username=username, first_name=split_name[0], last_name=split_name[2])
        user.set_password(password)
        await sync_to_async(user.save)()

        await sync_to_async(login)(info.context.request, user)

        return user

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updateProfile(self, info: Info, first_name: str, last_name: str) -> User:
        user = get_user(info)

        user.first_name = first_name
        user.last_name = last_name

        await sync_to_async(user.save)()

        return user

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updatePassword(self, info: Info, old_password: str, password: str) -> User:
        user = get_user(info)

        if not check_password(old_password, user.password):
            raise PermissionDenied("Old password does not match")

        user.set_password(password)
        await sync_to_async(user.save)()

        return user

    @strawberry.mutation
    async def requestPasswordReset(self, email: str) -> BasicResult:
        UserModel = get_user_model()

        try:
            user = await UserModel.objects.filter(username=email).aget()

            subject = "Grai Password Reset"
            email_template_name = "auth/password_reset_email.txt"
            c = {
                "email": user.username,
                "base_url": config("FRONTEND_URL", "http://localhost:3000"),
                "uid": user.pk,
                "user": user,
                "token": default_token_generator.make_token(user),
            }
            email_message = render_to_string(email_template_name, c)

            send_mail(
                subject,
                email_message,
                settings.EMAIL_FROM,
                [user.username],
                fail_silently=False,
            )

        except UserModel.DoesNotExist:
            print("User not found")

        return BasicResult(success=True)

    @strawberry.mutation
    async def resetPassword(self, token: str, uid: str, password: str) -> User:
        UserModel = get_user_model()

        try:
            user = await UserModel.objects.aget(pk=uid)

            if not default_token_generator.check_token(user, token):
                raise Exception("Token invalid")

            user.set_password(password)
            await sync_to_async(user.save)()
            return user

        except UserModel.DoesNotExist:
            raise Exception("User not found")

    @strawberry.mutation
    async def completeSignup(self, token: str, uid: str, first_name: str, last_name: str, password: str) -> User:
        UserModel = get_user_model()

        try:
            user = await UserModel.objects.aget(pk=uid)

            if not default_token_generator.check_token(user, token):
                raise Exception("Token invalid")

            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            await sync_to_async(user.save)()
            return user

        except UserModel.DoesNotExist:
            raise Exception("User not found")
