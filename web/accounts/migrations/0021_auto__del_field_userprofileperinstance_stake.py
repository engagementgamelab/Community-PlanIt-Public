# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UserProfilePerInstance.stake'
        db.delete_column('accounts_userprofileperinstance', 'stake_id')


    def backwards(self, orm):
        # Adding field 'UserProfilePerInstance.stake'
        db.add_column('accounts_userprofileperinstance', 'stake',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileStake'], null=True, blank=True),
                      keep_default=False)


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
            'Meta': {'object_name': 'PlayerMissionState'},
            'barriers_fifty_fifty': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'barriers_fifty_fifty'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['challenges.Challenge']"}),
            'challenges_completed': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'challenges_completed'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['challenges.Challenge']"}),
            'challenges_locked': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'challenges_locked'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['challenges.Challenge']"}),
            'challenges_unlocked': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'challenges_unlocked'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['challenges.Challenge']"}),
            'coins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_mission_states'", 'to': "orm['missions.Mission']"})
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
            'mission_states': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_profiles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['accounts.PlayerMissionState']"}),
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
        'challenges.challenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'Challenge', '_ormbases': ['instances.BaseTreeNode']},
            'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['instances.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'challenge_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'null': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_player_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'})
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