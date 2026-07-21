from allauth.socialaccount.models import SocialAccount
def google_profile(request):
    """Makes google_avatar and google_name available in every template."""
    if request.user.is_authenticated:
        try:
            account = SocialAccount.objects.get(user=request.user, provider='google')
            return {
                'google_avatar': account.extra_data.get('picture'),
                'google_name': account.extra_data.get('name'),
            }
        except SocialAccount.DoesNotExist:
            # user signed up with email/password, not Google — no avatar available
            return {
                'google_avatar': None,
                'google_name': request.user.email,
            }
    return {}