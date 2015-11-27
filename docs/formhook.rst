.. _formhook:

FormHook
========

Creating a hook-point::

    # main_app/formhooks.py

    from hooks.formhook import Hook

    MyFormHook = Hook()
    UserFormHook = Hook(providing_args=['user'])

Adding a hook-point to the main app view::

    # main_app/views.py

    from main_app import formhooks


    # Example 1
    def my_view(request):
        if request.method == 'POST':
            myform = MyForm(data=request.POST)
            hook = formhooks.MyFormHook(data=request.POST)

            if all([myform.is_valid(), hook.is_valid()]):  # Avoid short-circuit
                myform.save()
                hook.save()
                redirect('/')
        else:
            myform = MyForm()
            hook = formhooks.MyFormHook()

        return response({'myform': myform, 'hook_form': hook}) #...


    # Example 2
    def user_profile_update(request):
        if request.method == 'POST':
            user_form = UserForm(data=request.POST, instance=request.user)

            # Hook listeners will receive the user and populate the
            # initial data (or instance if a ModelForm is used) accordingly,
            # or maybe even query the data base.
            hook = formhooks.UserFormHook(user=request.user, data=request.POST)

            if all([user_form.is_valid(), hook.is_valid()]):  # Avoid short-circuit
                new_user = user_form.save()
                hook.save(new_user=new_user)  # They may receive extra parameter when saving
                redirect('/')
        else:
            user_form = MyForm(instance=request.user)
            hook = formhooks.UserFormHook(user=request.user)

        return response({'user_form': user_form, 'hook_form': hook}) #...

Displaying the forms::

    # main_app/templates/my_view.html

    {% extends "main_app/_base.html" %}

    {% block title %}My forms{% endblock %}

    {% block content %}
        <h1 class="headline">My forms</h1>

        <form action="." method="post">
            {% csrf_token %}
            {{ myform }}

            {% for f in hook_form %}
                {{ f }}
            {% endfor %}

            <input type="submit" value="Save" />
        </form>
    {% endblock %}

Creating a hook-listener in a third-party app:

| > Hooks listeners are just regular django forms or model forms

::

    # third_party_app/forms.py

    from django import forms
    from third_party_app.models import MyUserExtension


    class MyUserExtensionForm(forms.ModelForm):

        class Meta:
            model = MyUserExtension
            fields = ("gender", "age", "about")

        def __init__(user=None, *args, **kwargs):
            try:
               instance = MyUserExtension.objects.get(user=user)
            except MyUserExtension.DoesNotExist:
               instance = None

            kwargs['instance'] = instance
            super(MyUserExtensionForm, self).__init__(*args, **kwargs)

        def save(new_user, *args, **kwargs):
            self.instance.user = new_user
            super(MyUserExtensionForm, self).save(*args, **kwargs)


    class MyRegularForm(forms.Form):
        """"""
        # ...

Registering a hook-listener::

    # third_party_app/apps.py

    from django.apps import AppConfig


    class MyAppConfig(AppConfig):

        name = 'myapp'
        verbose_name = 'My App'

        def ready(self):
            from main_app.formhooks import MyFormHook, UserFormHook
            from third_party_app.forms import MyRegularForm, MyUserExtensionForm

            MyFormHook.register(MyRegularForm)
            UserFormHook.register(MyUserExtensionForm)

