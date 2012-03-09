# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'City'
        db.create_table('instances_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('instances', ['City'])

        # Adding model 'Language'
        db.create_table('instances_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('instances', ['Language'])

        # Adding model 'Affiliation'
        db.create_table('instances_affiliation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
        ))
        db.send_create_signal('instances', ['Affiliation'])

        # Adding model 'InstanceTranslation'
        db.create_table('instances_instancetranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['instances.Instance'])),
        ))
        db.send_create_signal('instances', ['InstanceTranslation'])

        # Adding unique constraint on 'InstanceTranslation', fields ['language_code', 'master']
        db.create_unique('instances_instancetranslation', ['language_code', 'master_id'])

        # Adding model 'Instance'
        db.create_table('instances_instance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('gmapsfield.fields.GoogleMapsField')()),
            ('days_for_mission', self.gf('django.db.models.fields.IntegerField')(default=7)),
            ('for_city', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', null=True, to=orm['instances.City'])),
        ))
        db.send_create_signal('instances', ['Instance'])

        # Adding M2M table for field curators on 'Instance'
        db.create_table('instances_instance_curators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('instance', models.ForeignKey(orm['instances.instance'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('instances_instance_curators', ['instance_id', 'user_id'])

        # Adding M2M table for field languages on 'Instance'
        db.create_table('instances_instance_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('instance', models.ForeignKey(orm['instances.instance'], null=False)),
            ('language', models.ForeignKey(orm['instances.language'], null=False))
        ))
        db.create_unique('instances_instance_languages', ['instance_id', 'language_id'])

        # Adding M2M table for field affiliations on 'Instance'
        db.create_table('instances_instance_affiliations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('instance', models.ForeignKey(orm['instances.instance'], null=False)),
            ('affiliation', models.ForeignKey(orm['instances.affiliation'], null=False))
        ))
        db.create_unique('instances_instance_affiliations', ['instance_id', 'affiliation_id'])

        # Adding model 'PointsAssignmentAction'
        db.create_table('instances_pointsassignmentaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=260)),
        ))
        db.send_create_signal('instances', ['PointsAssignmentAction'])

        # Adding model 'PointsAssignment'
        db.create_table('instances_pointsassignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='points_assignments', to=orm['instances.PointsAssignmentAction'])),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='points_assignments', to=orm['instances.Instance'])),
        ))
        db.send_create_signal('instances', ['PointsAssignment'])

        # Adding model 'NotificationRequest'
        db.create_table('instances_notificationrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notification_requests', to=orm['instances.Instance'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('instances', ['NotificationRequest'])

        # Adding unique constraint on 'NotificationRequest', fields ['instance', 'email']
        db.create_unique('instances_notificationrequest', ['instance_id', 'email'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'NotificationRequest', fields ['instance', 'email']
        db.delete_unique('instances_notificationrequest', ['instance_id', 'email'])

        # Removing unique constraint on 'InstanceTranslation', fields ['language_code', 'master']
        db.delete_unique('instances_instancetranslation', ['language_code', 'master_id'])

        # Deleting model 'City'
        db.delete_table('instances_city')

        # Deleting model 'Language'
        db.delete_table('instances_language')

        # Deleting model 'Affiliation'
        db.delete_table('instances_affiliation')

        # Deleting model 'InstanceTranslation'
        db.delete_table('instances_instancetranslation')

        # Deleting model 'Instance'
        db.delete_table('instances_instance')

        # Removing M2M table for field curators on 'Instance'
        db.delete_table('instances_instance_curators')

        # Removing M2M table for field languages on 'Instance'
        db.delete_table('instances_instance_languages')

        # Removing M2M table for field affiliations on 'Instance'
        db.delete_table('instances_instance_affiliations')

        # Deleting model 'PointsAssignmentAction'
        db.delete_table('instances_pointsassignmentaction')

        # Deleting model 'PointsAssignment'
        db.delete_table('instances_pointsassignment')

        # Deleting model 'NotificationRequest'
        db.delete_table('instances_notificationrequest')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'instances.affiliation': {
            'Meta': {'object_name': 'Affiliation'},
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'instances.city': {
            'Meta': {'object_name': 'City'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'instances.instance': {
            'Meta': {'object_name': 'Instance'},
            'affiliations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['instances.Affiliation']", 'symmetrical': 'False'}),
            'curators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'days_for_mission': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
            'for_city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'null': 'True', 'to': "orm['instances.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['instances.Language']", 'symmetrical': 'False'}),
            'location': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'instances.instancetranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'InstanceTranslation'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['instances.Instance']"})
        },
        'instances.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'instances.notificationrequest': {
            'Meta': {'unique_together': "(['instance', 'email'],)", 'object_name': 'NotificationRequest'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_requests'", 'to': "orm['instances.Instance']"})
        },
        'instances.pointsassignment': {
            'Meta': {'ordering': "('action__action', 'instance', 'points')", 'object_name': 'PointsAssignment'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'points_assignments'", 'to': "orm['instances.PointsAssignmentAction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'points_assignments'", 'to': "orm['instances.Instance']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'instances.pointsassignmentaction': {
            'Meta': {'ordering': "('action',)", 'object_name': 'PointsAssignmentAction'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '260'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['instances']
