ModelHook
=========

Before getting into ``ModelHooks`` lets take a quick view at
model mixins and why they are important.

Model mixins are a way to re-use fields and
methods across many models by doing multiple inheritance,
if you have ever used class-view mixins, it's pretty similar.

::

    # Models mixin example

    class TimeMixin(models.Model):

        created_at = models.DateTimeField(default=timezone.now)
        updated_at = models.DateTimeField(default=timezone.now)

        class Meta:
            abstract = True

        def save(self, *args, **kwargs):
            updated_at = timezone.now()
            super(MyTimeMixin, self).save(*args, **kwargs)


    class MyBook(TimeMixin, models.Model):

        author = models.CharField(max_length=75)

If you didn't know this was possible, don't go rewrite your models this way,
multiple inheritance tends to go out of hands and adds complexity
(as in code really hard to follow) pretty quickly. If you can avoid it, do it.

So, this is important because it's exactly how ``ModelHooks`` works.
Except the inheritance part is dynamic, the concrete model inherits
all of its plugins.

Because of this all plugin's model fields should have a ``default`` value,
since the main app won't know how to populate the fields when creating
a new record (ie: ``MyModel.objects.create(...)``).

Creating a hook-point::

    # main_app/hooks.py

    from hooks.modelhook import ModelHook


    MyModelHook = ModelHook()

Adding a hook-point to the main app::

    # main_app/models.py

    from django.db import models

    from .hooks import MyModelHook


    class MyAppModel(MyModelHook.plugins, models.Model):

        title = models.CharField(max_length=75)

Registering a plugin (AKA hook-listener in other parts of the docs)::

    # third_party_app/models.py

    from django.db import models

    from main_app.hooks import MyModelHook


    class MyPlugin(models.Model):

        my_plugin_subtitle = models.CharField(max_length=75, default='')

        class Meta:
            abstract = True

    MyModelHook.register(MyPlugin)

.. Tip:: Always prefix your plugin fields and custom methods
         with the name of the plugin to avoid clashes

.. Tip:: Always set a default field value, when this is not possible
         you may want to consider extending the main model in the
         regular way: using a ``OneToOneField`` instead.

Installing the plugin::

    # settings.py

    INSTALLED_APPS = (
        'hooks',
        'third_party_app',
        'main_app',
    )

.. Tip:: Plugins must be placed before the main app

Working with ModelForms
-----------------------

To include the plugin's model fields into a ``ModelForm``,
the plugin must define the available fields, and the form
must include them within the form.

Defining form fields::

    # third_party_app/models.py

    class MyPlugin(models.Model):

        my_plugin_subtitle = models.CharField(max_length=75, default='')
        my_plugin_description = models.CharField(max_length=255, default='')

        FULL_FORM_FIELDS = ['my_plugin_subtitle', 'my_plugin_description']
        SIMPLE_FORM_FIELDS = ['my_plugin_subtitle']

        class Meta:
            abstract = True

Include the fields::

    # main_app/forms.py

    from django import forms

    from .models import MyAppModel
    from .hooks import MyModelHook


    class MyAppForm(forms.ModelForm):

        class Meta:
            model = MyAppModel
            fields = ["title"] + MyModelHook.fields_for('FULL_FORM_FIELDS')

