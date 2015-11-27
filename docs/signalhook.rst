.. _signalhook:

SignalHook
==========

Best practices:

* Always *document* the signals the app will send, include the parameters the receiver should handle.
* Send signals from views, only.
* Avoid sending signals from plugins.
* Try to avoid signal-hell in general. It's better to be *explicit* and call the
  functions that would've handle the signal otherwise. Of course, this won't be
  possible when there are plugins involved.

Connecting a hook-listener::

    # third_party_app/urls.py

    from third_party_app.viewhooks import myhandler
    from hooks import signalhook

    signalhook.hook.connect("my-signal", myhandler)

Sending a signal::

    # send from anywhere, app-hook, main-app... view, model, form...

    from hooks import signalhook

    responses = signalhook.hook.send("my-signal", arg_one="hello", arg_two="world")
    responses = signalhook.hook.send("another-signal")

| > ``SignalHook`` uses django signals under the hood, so you can do pretty much the same things.
