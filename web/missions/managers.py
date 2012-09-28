
"""
class MissionManager(TreeManager):

    @cached(60*60*24, 'missions_for_instance')
    def for_instance(self, instance):
        return self.filter(instance=instance)

    @cached(60*60*24, 'missions')
    def latest_by_instance(self, instance):
        missions_for_instance = self.filter(instance=instance)
        if missions_for_instance:
            latest_by =  max(missions_for_instance.values_list('end_date', flat=True))
            return self.get(**dict(end_date=latest_by))

        return self.none()

    @cached(60*60*24, 'missions')
    def past(self, instance):
        return self.filter(instance=instance, end_date__lt=datetime.datetime.now()).order_by('-end_date')

    @cached(60*60*24, 'missions')
    def future(self, instance):
        return self.filter(instance=instance, start_date__gt=datetime.datetime.now()).order_by('start_date')

    #@cached(60*60*24, 'missions')
    def default(self, instance_id):
        qs =  self.active(instance_id)
        if qs.count() > 0:
            return qs[0]

    def first(self, instance_id):
        qs =  self.filter(instance__pk=instance_id).order_by('start_date')
        if qs.count() > 0:
            return qs[0]

    #@cached(60*60*24, 'missions')
    def active(self, instance_id):
        now = datetime.datetime.now()
        qs = self.filter(instance__pk=instance_id, start_date__lte=now, end_date__gte=now).order_by('start_date')
        return qs
"""

