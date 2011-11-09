import django.dispatch


log_event = django.dispatch.Signal(providing_args=[ 'test'
                                    #'action', 'data', 'url', 'type', 'instance', 'user', 'request'
                                ]
)


