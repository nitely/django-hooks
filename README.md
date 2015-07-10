# django-hooks[![Build Status](https://travis-ci.org/nitely/django-hooks.png)](https://travis-ci.org/nitely/django-hooks) [![Coverage Status](https://coveralls.io/repos/nitely/django-hooks/badge.png?branch=master)](https://coveralls.io/r/nitely/django-hooks?branch=master)

A modular plugin system for django apps.

There are 3 kinds of hooks:

* TemplateHook: Third-party apps will be able to insert their own code (text/html) into an app template.
* ViewHook: Third-party apps will be able to insert Forms in an app view.
* SignalHook: Connect or emit a signal by its name/id. This is the same as django signals except that signals don't need to be pre-created.

**Tested** in Django 1.7, 1.8 LTS; Python 2.7, 3.4

## Use case example

Let's say we want to render contextual information beside a record allocated in main_app. This extra information can be provided by some third-party application: Notes, Attachments, Comments, Followers, etc.

Adding an `{% include %}` tag to our `record.html` is not possible cause we don't know what to render beforehand (a note? a list of comments?) or even if any of those applications is installed for our case/customer/project.

We can create a TemplateHook `{% hook 'contextual_info' %}` where we delegate the rendering and content retrieval to the hooked app(s). By doing so, `record.html` doesn't need to be touched anymore, no need to add more templatetags to `{% load %}` and we also we do not overcharge our templates to be easily reused.

## Configuration

1. Add `hooks` to your *INSTALLED_APPS*. This is required only if you are going to use the TemplateHook.

## Usage

### TemplateHook

Adding a hook-point in the main app template:

```html
# main_app/templates/_base.html

{% load hooks_tags %}

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    #...
    
    {% hook 'within_head' %}
   
    #...
  </head>
</html>
```

> Here we are adding a *hook-point* called `within_head` where third-party apps will be able to insert their code.

Creating a hook-listener in a third-party app:

```python
# third_party_app/templatehooks.py

from django.template.loader import render_to_string
from django.utils.html import mark_safe, format_html


def css_resources(context, *args, **kwargs):
    return mark_safe(u'<link rel="stylesheet" href="%s/app_hook/styles.css">' % settings.STATIC_URL)


def user_about_info(context, *args, **kwargs):
    user = context['request'].user
    return format_html(
        "<b>{name}</b> {last_name}: {about}",
        name=user.first_name,
        last_name=user.last_name,
        about=mark_safe(user.profile.about_html)
    )


def a_more_complex_hook(context, *args, **kwargs):
    # If you are doing this a lot, make sure to keep your templates in memory (google: django.template.loaders.cached.Loader)
    return render_to_string('templates/app_hook/head_resources.html', context_instance=context)


def an_even_more_complex_hook(context, *args, **kwargs):
    articles = Article.objects.all()
    return render_to_string('templates/app_hook/my_articles.html', {'articles': articles, }, context_instance=context)
```

Registering a hook in your App-Hook:

```python
# third_party_app/urls.py

from hooks.templatehook import hook

from third_party_app.templatehooks import css_resources


hook.register("within_head", css_resources)
```

> Where to register your hooks:
> 
> urls.py for django<=1.6
> 
> AppConfig.ready() method for django>=1.7. [Helpful article](http://chriskief.com/2014/02/28/django-1-7-signals-appconfig/).

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
    #...
    hook = hooks.myview(request)
    hook.dispatch()

    if is_post:
        #...
        hook.post()

        if hook.is_valid():
            #...
            hook.save()
            redirect('/')
    else:
        #...
        hook.get()

    context = {'foo': foobar, }
    context.update(hook.context)

    return response(context) #...
```

> Go to the Miscellaneous section for a real life example.

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

signalhook.hook.send("my-signal", myarg="hello")
signalhook.hook.send("another-signal")
```

> SignalHook uses django signals under the hood, so you can do pretty much the same things.

### Miscellaneous: TemplateHook

As you saw earlier *TemplateHooks* don't need to be pre-created, passing `within_head` to the hook-point will call any listener previously registered to that name/id.
But, what if you want to have static/pre-created hook-point... you can! but it requires you to create an extra template tag.
Let's create a static hook-point:

```python
# main_app/templatehooks.py
from hooks.templatehook import TemplateHook

within_head = TemplateHook(providing_args=["context", ])
```

Creating a template-tag that will call the `within_head` from the `templatehooks.py` module.

```python
# main_app/templatetags/hook.py
from hooks.templatetags import template_hook_collect
from main_app import templatehooks

@register.simple_tag(takes_context=True)
def hook(context, name, *args, **kwargs):
    return template_hook_collect(hooks, name, context, *args, **kwargs)
```

In the main app template:

```html
# main_app/templates/_base.html

{% load hook %}
<html>
    <head>
        {% hook 'within_head' %}
        ...
```

Registering a third-party app:

```python
# third_party_app/urls.py

from main_app.templatehooks import within_head
from third_party_app.templatehooks import css_resources

within_head.register(css_resources)
```

### Miscellaneous: ViewHook

A real life viewhook example:

```python
main_app/views.py

from main_app import viewhooks

from main_app.form import UserForm


def myview(request, article_id):
    article = Article.objects.get(pk=article_id)

    hook = hooks.myview(request)
    hook.dispatch(article)

    if request.method == 'POST':
        form = UserForm(data=request.POST)
        hook.post(article)

        if form.is_valid() and hook.is_valid():
            user = form.save()
            hook.save(user)
            redirect('/')
    else:
        form = UserForm()
        hook.get()

    context = {'form': form, }
    context.update(hook.context)

    return render(request, 'main_app/my_template.html', context)
```

## License

MIT