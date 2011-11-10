import django.dispatch

log_event = django.dispatch.Signal(providing_args=[ 'action', 'data', 'url', 'type', 'user', ])
