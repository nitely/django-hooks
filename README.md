# django-hooks[![Build Status](https://travis-ci.org/nitely/django-hooks.png)](https://travis-ci.org/nitely/django-hooks) [![Coverage Status](https://coveralls.io/repos/nitely/django-hooks/badge.png?branch=master)](https://coveralls.io/r/nitely/django-hooks?branch=master)

A modular plugin system for django apps.

There are 3 kinds of hooks:

* TemplateHook: Third-party apps will be able to insert their own code (text/html) into an app template.
* ViewHook: Third-party apps will be able to insert Forms in an app view.
* SignalHook: Connect or emit a signal by its name/id. This is the same as Django signals
except that they don't need to be pre-defined.

**Tested** in Django 1.7, 1.8 LTS; Python 2.7, 3.4, 3.5

## Why?

Let's say we want to render contextual information beside a record allocated in `my_main_app`.
This extra information can be provided by some third-party application: Notes, Attachments,
Comments, Followers, etc.

Adding an `{% include %}` tag to our `my_record.html` is not possible cause we don't know what
to render beforehand (a note? a list of comments?) or even if any of those applications is
installed for our case/customer/project.

We can create a TemplateHook `{% hook 'my_contextual_info' %}` where we delegate the rendering and
content retrieval to the hooked app(s). By doing so, `my_record.html` doesn't need to be touched anymore,
no need to add more templatetags to `{% load %}` and we also make it easily reusable.

## Configuration

1. Add `hooks` to your *INSTALLED_APPS*. This is required by `TemplateHook`.

## Usage

### TemplateHook

Adding a hook-point in `main_app`'s template:

```html
# my_main_app/templates/_base.html

{% load hooks_tags %}

<!DOCTYPE html>
<html>
  <head>
    #...
    
    {% hook 'within_head' %}
   
    #...
  </head>
</html>
```

> Here we are adding a *hook-point* called `within_head` where *third-party*
> apps will be able to insert their code.

Creating a hook listener in a `third_party_app`:

```python
# third_party_app/template_hooks.py

from django.template.loader import render_to_string
from django.utils.html import mark_safe, format_html


# Example 1
def css_resources(context, *args, **kwargs):
    return mark_safe(u'<link rel="stylesheet" href="%s/app_hook/styles.css">' % settings.STATIC_URL)


# Example 2
def user_about_info(context, *args, **kwargs):
    user = context['request'].user
    return format_html(
        "<b>{name}</b> {last_name}: {about}",
        name=user.first_name,
        last_name=user.last_name,
        about=mark_safe(user.profile.about_html_field)  # Some safe (sanitized) html data.
    )


# Example 3
def a_more_complex_hook(context, *args, **kwargs):
    # If you are doing this a lot, make sure to keep your templates in memory (google: django.template.loaders.cached.Loader)
    return render_to_string(
        template_name='templates/app_hook/head_resources.html',
        context_instance=context
    )


# Example 4
def an_even_more_complex_hook(context, *args, **kwargs):
    articles = Article.objects.all()
    return render_to_string(
        template_name='templates/app_hook/my_articles.html',
        dictionary={'articles': articles, },
        context_instance=context
    )
```

Registering a hook listener in a `third_party_app`:

```python
# third_party_app/urls.py

from hooks.templatehook import hook

from third_party_app.template_hooks import css_resources


hook.register("within_head", css_resources)
```

> Where to register your hooks:
> 
> Use `AppConfig.ready()`,
> [docs](https://docs.djangoproject.com/en/1.8/ref/applications/#django.apps.AppConfig.ready),
> [example](http://chriskief.com/2014/02/28/django-1-7-signals-appconfig/)

### ViewHook

Creating a hook-point:

```python
# main_app/viewhooks.py

from hooks.viewhook import Hook

myview = Hook()
```

Adding a hook-point to the main app view:

```python
# main_app/views.py

from main_app import viewhooks


def myview(request):
    # ...
    hook = hooks.myview(request)
    hook.dispatch()

    if is_post:
        # ...
        hook.post()

        if all([hook.is_valid(), other.is_valid()]):  # Avoid short-circuit evaluation (and)
            # ...
            hook.save()
            redirect('/')
    else:
        # ...
        hook.get()

    context = {'foo': foobar, }
    context.update(hook.context)

    return response(context)  # ...
```

Creating a hook-listener in a third-party app:

```python
# third_party_app/viewhooks.py

from hooks.viewhook import HookBase


class MyHook(HookBase):
    def dispatch(*args, **kwargs):
        # do something useful
    
    def post(*args, **kwargs):
        form = MyForm(data=self.request.POST)
        self.context['myhookform'] = form
    
    def is_valid():
        return self.context['myhookform'].is_valid()
    
    def save(*args, **kwargs):
        self.context['myhookform'].save()
    
    def get(*args, **kwargs):
        form = MyForm()
        self.context['myhookform'] = form
```

Registering a hook-listener:

```python
# third_party_app/urls.py

from third_party_app.viewhooks import MyHook
from main_app import viewhooks

viewhooks.myview.register(MyHook)
```

### SignalHook

> Best practices:
> * Always *document* the signals the app will send, include the parameters the receiver should handle.
> * Send signals from views, only.
> * Avoid sending signals from plugins.
> * Try to avoid signal-hell in general. It's better to be *explicit* and call the
> functions that would've handle the signal otherwise. Of course, this won't be
> possible when there are plugins involved.

Connecting a hook-listener:

```python
# third_party_app/urls.py

from third_party_app.viewhooks import myhandler
from hooks import signalhook

signalhook.hook.connect("my-signal", myhandler)
```

Sending a signal:

```python
# send from anywhere, app-hook, main-app... view, model, form...

from hooks import signalhook

responses = signalhook.hook.send("my-signal", arg_one="hello", arg_two="world")
responses = signalhook.hook.send("another-signal")
```

> `SignalHook` uses django signals under the hood, so you can do pretty much the same things.

## License

MIT
