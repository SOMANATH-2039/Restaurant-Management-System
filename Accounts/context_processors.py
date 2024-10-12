from . models import Profile

def user_profile_image(request):
    """Context processor to include user's profile image in all templates."""
    if request.user.is_authenticated:
        try:
            # Get the user's profile if they are logged in
            profile = Profile.objects.get(user=request.user)
            return {
                'profile_image': profile.profile_photo.url if profile.profile_photo else None,
            }
        except Profile.DoesNotExist:
            return {'profile_image': None}
    return {'profile_image': None}
