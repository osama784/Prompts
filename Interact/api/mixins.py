class UserQuerysetMixin():
    user_field = 'owner'
    allow_staff_view = False

    def get_queryset(self, *args, **kwargs):
        user  = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user.profile
        qs = super().get_queryset(*args, **kwargs)
        if user.is_staff and self.allow_staff_view:
            return qs
        return qs.filter(**lookup_data)