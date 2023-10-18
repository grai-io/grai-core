from datetime import datetime
from typing import Union

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
from django_otp import devices_for_user, user_has_device, verify_token
from django_otp.plugins.otp_totp.models import TOTPDevice
from strawberry.types import Info

from api.common import IsAuthenticated, get_user
from api.pagination import DataWrapper
from api.types import BasicResult, User
from users.types import Device

from .validation import send_validation_email, verification_generator


@strawberry.type
class DeviceWithUrl(Device):
    config_url: str


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def login(
        self,
        info: Info,
        username: str,
        password: str,
    ) -> Union[User, DataWrapper[Device]]:
        user = await sync_to_async(authenticate)(username=username, password=password)

        if user is None:
            raise Exception("Invalid credentials")

        if await sync_to_async(user_has_device)(user):

            def _fetch(user):
                devices = devices_for_user(user)

                return [Device(id=device.persistent_id, name=device.name) for device in devices]

            devices = await sync_to_async(_fetch)(user)

            return DataWrapper(data=devices)

        await sync_to_async(login)(info.context.request, user)

        return User(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @strawberry.mutation
    async def loginWithToken(
        self,
        info: Info,
        username: str,
        password: str,
        deviceId: strawberry.ID,
        token: str,
    ) -> User:
        user = await sync_to_async(authenticate)(username=username, password=password)

        if user is None:
            raise Exception("Invalid credentials")

        if await sync_to_async(verify_token)(user, deviceId, token) is None:
            raise Exception("Incorrect code")

        await sync_to_async(login)(info.context.request, user)

        return user

    @strawberry.mutation
    async def logout(
        self,
        info: Info,
    ) -> bool:
        def _logout(request):
            from django.contrib.auth.signals import user_logged_out

            """
            Remove the authenticated user's ID from the request and flush their session
            data.
            """
            # Dispatch the signal before the user is logged out so the receivers have a
            # chance to find out *who* logged out.
            user = request.consumer.scope.get("user", None)
            if not getattr(user, "is_authenticated", True):
                user = None
            user_logged_out.send(sender=user.__class__, request=request, user=user)
            request.session.flush()
            if "user" in request.consumer.scope:
                from django.contrib.auth.models import AnonymousUser

                request.consumer.scope["user"] = AnonymousUser()

        await sync_to_async(_logout)(info.context.request)

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

        await sync_to_async(send_validation_email)(user)

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
                "base_url": settings.FRONTEND_URL,
                "uid": user.pk,
                "user": user,
                "token": default_token_generator.make_token(user),
            }
            email_message = render_to_string(email_template_name, c)

            await sync_to_async(send_mail)(
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

            send_validation_email(user)

            return user

        except UserModel.DoesNotExist:
            raise Exception("User not found")

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def verifyEmail(self, info: Info, uid: str, token: str) -> User:
        user = get_user(info)

        if not str(user.pk) == uid:
            raise Exception("Incorrect user")

        if not verification_generator.check_token(user, token):
            raise Exception("Token invalid")

        user.verified_at = datetime.now()
        await sync_to_async(user.save)()

        return user

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createDevice(self, info: Info, name: str) -> DeviceWithUrl:
        def _create(info: Info, name: str) -> DeviceWithUrl:
            user = get_user(info)

            device = TOTPDevice(name=name)
            device.user = user
            device.confirmed = False
            device.save()

            return DeviceWithUrl(id=device.persistent_id, name=device.name, config_url=device.config_url)

        return await sync_to_async(_create)(info, name)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def confirmDevice(self, info: Info, deviceId: strawberry.ID, token: str) -> Device:
        def _confirm(info: Info, deviceId: strawberry.ID, token: str) -> Device:
            user = get_user(info)

            device = verify_token(user, deviceId, token)

            if not device:
                raise Exception("Incorrect code")

            device.confirmed = True
            device.save()

            return Device(id=device.persistent_id, name=device.name)

        return await sync_to_async(_confirm)(info, deviceId, token)
