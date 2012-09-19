# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'UserProfileGenderTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofilegender_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileEducationTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofileeducation_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileIncomeTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofileincome_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileLivingSituationTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofilelivingsituation_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileStakeTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofilestake_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileHowDiscoveredTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofilehowdiscovered_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileRaceTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofilerace_translation', ['language_code', 'master_id'])

        # Deleting model 'UserProfileRaceTranslation'
        db.delete_table('accounts_userprofilerace_translation')

        # Deleting model 'UserProfileHowDiscoveredTranslation'
        db.delete_table('accounts_userprofilehowdiscovered_translation')

        # Deleting model 'UserProfileStakeTranslation'
        db.delete_table('accounts_userprofilestake_translation')

        # Deleting model 'UserProfileLivingSituationTranslation'
        db.delete_table('accounts_userprofilelivingsituation_translation')

        # Deleting model 'UserProfileIncomeTranslation'
        db.delete_table('accounts_userprofileincome_translation')

        # Deleting model 'UserProfileEducationTranslation'
        db.delete_table('accounts_userprofileeducation_translation')

        # Deleting model 'UserProfileGenderTranslation'
        db.delete_table('accounts_userprofilegender_translation')

        # Deleting field 'UserProfile.currentCoins'
        db.delete_column('accounts_userprofile', 'currentCoins')

        # Deleting field 'UserProfile.coinPoints'
        db.delete_column('accounts_userprofile', 'coinPoints')

        # Deleting field 'UserProfile.totalPoints'
        db.delete_column('accounts_userprofile', 'totalPoints')

        # Adding unique constraint on 'PlayerMissionState', fields ['mission', 'profile_per_instance']
        db.create_unique('accounts_playermissionstate', ['mission_id', 'profile_per_instance_id'])

        # Adding field 'UserProfileLivingSituation.situation'
        db.add_column('accounts_userprofilelivingsituation', 'situation',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)

        # Adding field 'UserProfileRace.race'
        db.add_column('accounts_userprofilerace', 'race',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)

        # Adding field 'UserProfileGender.gender'
        db.add_column('accounts_userprofilegender', 'gender',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)

        # Adding field 'UserProfileEducation.education'
        db.add_column('accounts_userprofileeducation', 'education',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)

        # Adding field 'UserProfileIncome.income'
        db.add_column('accounts_userprofileincome', 'income',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)

        # Adding field 'UserProfileStake.stake'
        db.add_column('accounts_userprofilestake', 'stake',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)

        # Adding field 'UserProfileHowDiscovered.how'
        db.add_column('accounts_userprofilehowdiscovered', 'how',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'PlayerMissionState', fields ['mission', 'profile_per_instance']
        db.delete_unique('accounts_playermissionstate', ['mission_id', 'profile_per_instance_id'])

        # Adding model 'UserProfileRaceTranslation'
        db.create_table('accounts_userprofilerace_translation', (
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileRace'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('race', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileRaceTranslation'])

        # Adding unique constraint on 'UserProfileRaceTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofilerace_translation', ['language_code', 'master_id'])

        # Adding model 'UserProfileHowDiscoveredTranslation'
        db.create_table('accounts_userprofilehowdiscovered_translation', (
            ('how', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileHowDiscovered'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileHowDiscoveredTranslation'])

        # Adding unique constraint on 'UserProfileHowDiscoveredTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofilehowdiscovered_translation', ['language_code', 'master_id'])

        # Adding model 'UserProfileStakeTranslation'
        db.create_table('accounts_userprofilestake_translation', (
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileStake'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stake', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileStakeTranslation'])

        # Adding unique constraint on 'UserProfileStakeTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofilestake_translation', ['language_code', 'master_id'])

        # Adding model 'UserProfileLivingSituationTranslation'
        db.create_table('accounts_userprofilelivingsituation_translation', (
            ('situation', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileLivingSituation'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileLivingSituationTranslation'])

        # Adding unique constraint on 'UserProfileLivingSituationTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofilelivingsituation_translation', ['language_code', 'master_id'])

        # Adding model 'UserProfileIncomeTranslation'
        db.create_table('accounts_userprofileincome_translation', (
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileIncome'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('income', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('accounts', ['UserProfileIncomeTranslation'])

        # Adding unique constraint on 'UserProfileIncomeTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofileincome_translation', ['language_code', 'master_id'])

        # Adding model 'UserProfileEducationTranslation'
        db.create_table('accounts_userprofileeducation_translation', (
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileEducation'])),
            ('education', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileEducationTranslation'])

        # Adding unique constraint on 'UserProfileEducationTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofileeducation_translation', ['language_code', 'master_id'])

        # Adding model 'UserProfileGenderTranslation'
        db.create_table('accounts_userprofilegender_translation', (
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileGender'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileGenderTranslation'])

        # Adding unique constraint on 'UserProfileGenderTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofilegender_translation', ['language_code', 'master_id'])

        # Adding field 'UserProfile.currentCoins'
        db.add_column('accounts_userprofile', 'currentCoins',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserProfile.coinPoints'
        db.add_column('accounts_userprofile', 'coinPoints',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserProfile.totalPoints'
        db.add_column('accounts_userprofile', 'totalPoints',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'UserProfileLivingSituation.situation'
        db.delete_column('accounts_userprofilelivingsituation', 'situation')

        # Deleting field 'UserProfileRace.race'
        db.delete_column('accounts_userprofilerace', 'race')

        # Deleting field 'UserProfileGender.gender'
        db.delete_column('accounts_userprofilegender', 'gender')

        # Deleting field 'UserProfileEducation.education'
        db.delete_column('accounts_userprofileeducation', 'education')

        # Deleting field 'UserProfileIncome.income'
        db.delete_column('accounts_userprofileincome', 'income')

        # Deleting field 'UserProfileStake.stake'
        db.delete_column('accounts_userprofilestake', 'stake')

        # Deleting field 'UserProfileHowDiscovered.how'
        db.delete_column('accounts_userprofilehowdiscovered', 'how')


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
            'Meta': {'unique_together': "(('profile_per_instance', 'mission'),)", 'object_name': 'PlayerMissionState'},
            'barriers_fifty_fifty': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'barriers_fifty_fifty'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['challenges.Challenge']"}),
            'challenges_completed': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'challenges_completed'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['challenges.Challenge']"}),
            'challenges_locked': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'challenges_locked'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['challenges.Challenge']"}),
            'challenges_unlocked': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'challenges_unlocked'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['challenges.Challenge']"}),
            'coins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_mission_states'", 'to': "orm['missions.Mission']"}),
            'next_unlocked_barrier': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'next_unlocked_barriers'", 'unique': 'True', 'null': 'True', 'to': "orm['challenges.Challenge']"}),
            'profile_per_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_mission_states'", 'to': "orm['accounts.UserProfilePerInstance']"})
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
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_profiles_list'", 'to': "orm['instances.Instance']", 'through': "orm['accounts.UserProfilePerInstance']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
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
            'stake': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileStake']", 'null': 'True', 'blank': 'True'}),
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