from datetime import datetime, timedelta, timezone

import pytz
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    """Expiring Token base class."""

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted'))

        # This is required for the time comparison
        utc_now = datetime.now(timezone.utc)
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - timedelta(days=settings.TOKEN_EXPIRATION_DAYS):
            token.delete()  # ADDED THIS LINE SO THAT EXPIRED TOKEN IS DELETED, LOGIN CREATES NEW ONE
            raise AuthenticationFailed(_('Token has expired'))
        token.created = utc_now  # THIS WILL SET THE token.created TO CURRENT TIME WITH EVERY REQUEST
        token.save()  # SAVE THE TOKEN

        return token.user, token
