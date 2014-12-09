# django-hooks[![Build Status](https://travis-ci.org/nitely/django-hooks.png)](https://travis-ci.org/nitely/django-hooks) [![Coverage Status](https://coveralls.io/repos/nitely/django-hooks/badge.png?branch=master)](https://coveralls.io/r/nitely/django-hooks?branch=master)

A plugin system for django apps. It provides ways for an app (called from here *App-Hook*) to inject code into another app.
So you can integrate existing or third party apps into main app.

There are 3 kinds of hooks:

* TemplateHook: the most useful one, App-Hooks will be able to inject their own code into your templates.
* ViewHook: App-Hooks will be able to add Forms in your views.
* SignalHook: This is the same as django signals except that *signal-hooks* don't need to be pre-created. You can connect or emit a signal by its name/id.

**Tested** in Django 1.4, 1.5, 1.6, 1.7; Python 2.7, 3.4

## Possible scenario

Let's say we want to render contextual information beside a record allocated in main_app. This extra information can be provided by some third party application: Notes, Attachments, Comments, Followers, ...

Adding an `{% include %}` tag to our `record.html` is not possible cause we don't know what to render beforehand (a note? a list of comments?) or even if any of those applications is installed for our case/customer/project.

We can create a TemplateHook `{% hook 'contextual_info' %}` where we delegate the rendering and content retrieval to the hooked app(s). By doing so, `record.html` doesn't need to be touched anymore, no need to add more templatetags to `{% load %}` and we also we do not overcharge our templates to be easily reused.

## Configuration

1. Add `hooks` to your *INSTALLED_APPS*. This is required only if you are going to use the templatetags.

## Learn by example

### TemplateHook

Adding a hook in your main-app template:

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

Here we are adding a *hook point* called `within_head` where App-Hooks will be able to inject their code.

Creating a hook in your App-Hook:

```python
# app_hook/templatehooks.py

from django.template.loader import render_to_string


def css_resources(context, *args, **kwargs):
    return u'<link rel="stylesheet" href="%s/app_hook/styles.css">' % settings.STATIC_URL

def a_more_complex_hook(context, *args, **kwargs):
    # If you are doing this a lot, make sure to keep your templates in memory (google: django.template.loaders.cached.Loader)
    return render_to_string('templates/app_hook/head_resources.html', context_instance=context)

def a_even_more_complex_hook(context, *args, **kwargs):
    articles = Article.objects.all()
    return render_to_string('templates/app_hook/my_articles.html', {'articles': articles, }, context_instance=context)
```

Registering a hook in your App-Hook:

```python
# app_hook/urls.py

from app_hook.templatehooks import css_resources
from hooks.templatehook import hook

hook.register("within_head", css_resources)
```

>**Note**
> 
> Where to register your hooks:
> 
> urls.py is a good place (django<=1.6)
> 
> or do it in the AppConfig.ready() method (django>=1.7). Read helpfull article http://chriskief.com/2014/02/28/django-1-7-signals-appconfig/

### ViewHook

Creating a view-hook:

```python
# main_app/viewhooks.py

from hooks.viewhook import Hook

myview = Hook()
```

Adding it to your view:

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

> **Note**
> See Miscellaneous for a real life example.

Creating a hook in your App-Hook:

```python
# app_hook/viewhooks.py

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

Registering a view-hook:

```python
# app_hook/urls.py

from app_hook.viewhooks import MyHook
from main_app import viewhooks

viewhooks.myview.register(MyHook)
```

### SignalHook

Connecting a signal-hook:

```python
# app_hook/urls.py

from app_hook.viewhooks import myhandler
from hooks import signalhook

signalhook.hook.connect("my-signal", myhandler)
```

Sending a signal:

```python
# send from anywhere, app-hook, main-app... view, model, form...

from hooks import signalhook

signalhook.hook.send("my-signal", myarg="a string", mykwarg={'somthing': "else", })
signalhook.hook.send("another-signal")
```

> **Note**
> SignalHook uses django signals under the hood, so you can do pretty much the same.

### Miscellaneous

As you saw earlier *TemplateHooks* don't need to be pre-created, passing `within_head` to hook will call any callback previously registered to that name/id.
But, what if you want to have static/pre-created template-hooks... you can! but it requires you to create an extra template tag.
Let's create a static template-hook:

```python
# main_app/templatehooks.py
from hooks.templatehook import TemplateHook

within_head = TemplateHook(providing_args=["context", ])
```

Now, we can't use the `hooks_tags`, that's only good for dynamic template-hooks!
What we need is to create our own tag that will call the `within_head` from our `hooks.py` module.

```python
# main_app/templatetags/hook.py
from hooks.templatetags import template_hook_collect
from main_app import hooks

@register.simple_tag(takes_context=True)
def hook(context, name, *args, **kwargs):
    return template_hook_collect(hooks, name, context, *args, **kwargs)
```

In your template:

```html
# main_app/templates/_base.html

{% load hook %}
<html>
    <head>
        {% hook 'within_head' %}
        ...
```

Registering in your App-Hook:

```python
app_hook/urls.py

from app_hook.templatehooks import css_resources
from main_app.templatehooks import within_head

within_head.register(css_resources)
```

Now, a real life viewhook example:

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

## Contributing

Feel free to check out the source code and submit pull requests.

You may also report any bug or propose new features in the [issues tracker](https://github.com/nitely/django-hooks/issues)

## Copyright / License

Copyright 2014 [Esteban Castro Borsani](https://github.com/nitely).

Licensed under the [MIT License](https://github.com/nitely/django-hooks/blob/master/LICENSE).

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
