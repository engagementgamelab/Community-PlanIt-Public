# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfileEducation'
        db.create_table('accounts_userprofileeducation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('education', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileEducation'])

        # Adding model 'UserProfileGender'
        db.create_table('accounts_userprofilegender', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileGender'])

        # Adding model 'UserProfileHowDiscovered'
        db.create_table('accounts_userprofilehowdiscovered', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('how', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileHowDiscovered'])

        # Adding model 'UserProfileIncome'
        db.create_table('accounts_userprofileincome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('income', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileIncome'])

        # Adding model 'UserProfileLivingSituation'
        db.create_table('accounts_userprofilelivingsituation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('situation', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileLivingSituation'])

        # Adding model 'UserProfileRace'
        db.create_table('accounts_userprofilerace', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('race', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileRace'])

        # Adding model 'UserProfileStake'
        db.create_table('accounts_userprofilestake', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('stake', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileStake'])

        # Adding model 'UserProfilePerInstance'
        db.create_table('accounts_userprofileperinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_profiles_per_instance', to=orm['accounts.UserProfile'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instances.Instance'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfilePerInstance'])

        # Adding unique constraint on 'UserProfilePerInstance', fields ['user_profile', 'instance']
        db.create_unique('accounts_userprofileperinstance', ['user_profile_id', 'instance_id'])

        # Adding M2M table for field stakes on 'UserProfilePerInstance'
        db.create_table('accounts_userprofileperinstance_stakes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofileperinstance', models.ForeignKey(orm['accounts.userprofileperinstance'], null=False)),
            ('userprofilestake', models.ForeignKey(orm['accounts.userprofilestake'], null=False))
        ))
        db.create_unique('accounts_userprofileperinstance_stakes', ['userprofileperinstance_id', 'userprofilestake_id'])

        # Adding M2M table for field affils on 'UserProfilePerInstance'
        db.create_table('accounts_userprofileperinstance_affils', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofileperinstance', models.ForeignKey(orm['accounts.userprofileperinstance'], null=False)),
            ('affiliation', models.ForeignKey(orm['instances.affiliation'], null=False))
        ))
        db.create_unique('accounts_userprofileperinstance_affils', ['userprofileperinstance_id', 'affiliation_id'])

        # Adding model 'PlayerMissionState'
        db.create_table('accounts_playermissionstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mission_states', to=orm['auth.User'])),
            ('mission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mission_states', to=orm['missions.Mission'])),
            ('coins', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('accounts', ['PlayerMissionState'])

        # Adding unique constraint on 'PlayerMissionState', fields ['mission', 'user']
        db.create_unique('accounts_playermissionstate', ['mission_id', 'user_id'])

        # Adding model 'UserProfile'
        db.create_table('accounts_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('avatar', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=250, blank=True)),
            ('receive_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
            ('birth_year', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileGender'], null=True, blank=True)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileRace'], null=True, blank=True)),
            ('education', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileEducation'], null=True, blank=True)),
            ('income', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileIncome'], null=True, blank=True)),
            ('living', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileLivingSituation'], null=True, blank=True)),
            ('how_discovered', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileHowDiscovered'], null=True, blank=True)),
            ('how_discovered_other', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True)),
            ('tagline', self.gf('django.db.models.fields.CharField')(default='', max_length=140, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfile'])

        # Adding model 'UserProfileVariantsForInstance'
        db.create_table('accounts_userprofilevariantsforinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.OneToOneField')(related_name='user_profile_variants', unique=True, to=orm['instances.Instance'])),
        ))
        db.send_create_signal('accounts', ['UserProfileVariantsForInstance'])

        # Adding M2M table for field stake_variants on 'UserProfileVariantsForInstance'
        db.create_table('accounts_userprofilevariantsforinstance_stake_variants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofilevariantsforinstance', models.ForeignKey(orm['accounts.userprofilevariantsforinstance'], null=False)),
            ('userprofilestake', models.ForeignKey(orm['accounts.userprofilestake'], null=False))
        ))
        db.create_unique('accounts_userprofilevariantsforinstance_stake_variants', ['userprofilevariantsforinstance_id', 'userprofilestake_id'])

        # Adding M2M table for field affiliation_variants on 'UserProfileVariantsForInstance'
        db.create_table('accounts_userprofilevariantsforinstance_affiliation_variants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofilevariantsforinstance', models.ForeignKey(orm['accounts.userprofilevariantsforinstance'], null=False)),
            ('affiliation', models.ForeignKey(orm['instances.affiliation'], null=False))
        ))
        db.create_unique('accounts_userprofilevariantsforinstance_affiliation_variants', ['userprofilevariantsforinstance_id', 'affiliation_id'])

        # Adding model 'Notification'
        db.create_table('accounts_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['auth.User'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='content_type_set_for_notification', null=True, to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('accounts', ['Notification'])


    def backwards(self, orm):
        # Removing unique constraint on 'PlayerMissionState', fields ['mission', 'user']
        db.delete_unique('accounts_playermissionstate', ['mission_id', 'user_id'])

        # Removing unique constraint on 'UserProfilePerInstance', fields ['user_profile', 'instance']
        db.delete_unique('accounts_userprofileperinstance', ['user_profile_id', 'instance_id'])

        # Deleting model 'UserProfileEducation'
        db.delete_table('accounts_userprofileeducation')

        # Deleting model 'UserProfileGender'
        db.delete_table('accounts_userprofilegender')

        # Deleting model 'UserProfileHowDiscovered'
        db.delete_table('accounts_userprofilehowdiscovered')

        # Deleting model 'UserProfileIncome'
        db.delete_table('accounts_userprofileincome')

        # Deleting model 'UserProfileLivingSituation'
        db.delete_table('accounts_userprofilelivingsituation')

        # Deleting model 'UserProfileRace'
        db.delete_table('accounts_userprofilerace')

        # Deleting model 'UserProfileStake'
        db.delete_table('accounts_userprofilestake')

        # Deleting model 'UserProfilePerInstance'
        db.delete_table('accounts_userprofileperinstance')

        # Removing M2M table for field stakes on 'UserProfilePerInstance'
        db.delete_table('accounts_userprofileperinstance_stakes')

        # Removing M2M table for field affils on 'UserProfilePerInstance'
        db.delete_table('accounts_userprofileperinstance_affils')

        # Deleting model 'PlayerMissionState'
        db.delete_table('accounts_playermissionstate')

        # Deleting model 'UserProfile'
        db.delete_table('accounts_userprofile')

        # Deleting model 'UserProfileVariantsForInstance'
        db.delete_table('accounts_userprofilevariantsforinstance')

        # Removing M2M table for field stake_variants on 'UserProfileVariantsForInstance'
        db.delete_table('accounts_userprofilevariantsforinstance_stake_variants')

        # Removing M2M table for field affiliation_variants on 'UserProfileVariantsForInstance'
        db.delete_table('accounts_userprofilevariantsforinstance_affiliation_variants')

        # Deleting model 'Notification'
        db.delete_table('accounts_notification')


    models = {
        'accounts.notification': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Notification'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'content_type_set_for_notification'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['auth.User']"})
        },
        'accounts.playermissionstate': {
            'Meta': {'unique_together': "(('mission', 'user'),)", 'object_name': 'PlayerMissionState'},
            'coins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mission_states'", 'to': "orm['missions.Mission']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mission_states'", 'to': "orm['auth.User']"})
        },
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'avatar': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birth_year': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'education': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileEducation']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250', 'blank': 'True'}),
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileGender']", 'null': 'True', 'blank': 'True'}),
            'how_discovered': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileHowDiscovered']", 'null': 'True', 'blank': 'True'}),
            'how_discovered_other': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileIncome']", 'null': 'True', 'blank': 'True'}),
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_profiles'", 'to': "orm['instances.Instance']", 'through': "orm['accounts.UserProfilePerInstance']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'living': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileLivingSituation']", 'null': 'True', 'blank': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileRace']", 'null': 'True', 'blank': 'True'}),
            'receive_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'})
        },
        'accounts.userprofileeducation': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileEducation'},
            'education': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofilegender': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileGender'},
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofilehowdiscovered': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileHowDiscovered'},
            'how': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofileincome': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileIncome'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofilelivingsituation': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileLivingSituation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {}),
            'situation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'})
        },
        'accounts.userprofileperinstance': {
            'Meta': {'ordering': "('date_created', 'user_profile__user__last_name')", 'unique_together': "(('user_profile', 'instance'),)", 'object_name': 'UserProfilePerInstance'},
            'affils': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_profiles_per_instance'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['instances.Affiliation']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'stakes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'stakes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['accounts.UserProfileStake']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_profiles_per_instance'", 'to': "orm['accounts.UserProfile']"})
        },
        'accounts.userprofilerace': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileRace'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {}),
            'race': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'})
        },
        'accounts.userprofilestake': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileStake'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {}),
            'stake': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'})
        },
        'accounts.userprofilevariantsforinstance': {
            'Meta': {'object_name': 'UserProfileVariantsForInstance'},
            'affiliation_variants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['instances.Affiliation']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_profile_variants'", 'unique': 'True', 'to': "orm['instances.Instance']"}),
            'stake_variants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['accounts.UserProfileStake']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'})
        },
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
            'Meta': {'ordering': "('name',)", 'object_name': 'Affiliation'},
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'instances.basetreenode': {
            'Meta': {'object_name': 'BaseTreeNode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('polymorphic_tree.models.PolymorphicTreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['instances.BaseTreeNode']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_instances.basetreenode_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'instances.instance': {
            'Meta': {'ordering': "('start_date',)", 'object_name': 'Instance', '_ormbases': ['instances.BaseTreeNode']},
            'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['instances.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'city': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True'}),
            'curators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'days_for_mission': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'is_disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('gmapsfield.fields.GoogleMapsField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'missions.mission': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'Mission', '_ormbases': ['instances.BaseTreeNode']},
            'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['instances.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'challenge_coin_value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'video': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['accounts']