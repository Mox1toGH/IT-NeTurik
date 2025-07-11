from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

# Інлайн профілю користувача (відображення на сторінці користувача)
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профіль'
    fk_name = 'user'

# Розширений UserAdmin з профілем
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'get_role', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    inlines = (UserProfileInline,)

    def get_role(self, obj):
        return obj.userprofile.get_role_display() if hasattr(obj, 'userprofile') else '-'
    get_role.short_description = 'Роль'

# Скасування стандартної реєстрації User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Або окремо можна ще зареєструвати UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
