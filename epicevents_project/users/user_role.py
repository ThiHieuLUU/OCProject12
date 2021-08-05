class UserRole:
    @staticmethod
    def is_seller(user):
        return user.groups.filter(name='Sellers').exists()

    @staticmethod
    def is_supporter(user):
        return user.groups.filter(name='Supporters').exists()

    @staticmethod
    def is_superuser_or_manager(user):
        if user.is_superuser or user.groups.filter(name__in=['Managers']).exists():
            return True

    @classmethod
    def superuser_or_manager_permission(cls, func):
        def inner_func(self, request, *args, **kwargs):
            if cls.is_superuser_or_manager(request.user):
                return True
            return func(self, request, *args, **kwargs)

        return inner_func
