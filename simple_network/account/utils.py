menu = [
    {'title': 'Мой профиль', 'url_name': 'profile'},
    {'title': 'Мой профиль', 'url_name': 'search'},
    {'title': 'Мой профиль', 'url_name': 'exit'},
    {'title': 'Мой профиль', 'url_name': 'login'},
    {'title': 'Мой профиль', 'url_name': 'register'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        if 'selected_menu' not in context:
            context['selected_menu'] = 'profile'
        return context
