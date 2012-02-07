# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfilePerInstance'
        db.create_table('accounts_userprofileperinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.UserProfile'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instances.Instance'])),
            ('stake', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileStake'], null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileGender'], null=True, blank=True)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileRace'], null=True, blank=True)),
            ('education', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileEducation'], null=True, blank=True)),
            ('income', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileIncome'], null=True, blank=True)),
            ('living', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileLivingSituation'], null=True, blank=True)),
            ('how_discovered', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileHowDiscovered'], null=True, blank=True)),
            ('how_discovered_other', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfilePerInstance'])

        # Adding model 'UserProfileVariantsForInstance'
        db.create_table('accounts_userprofilevariantsforinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['instances.Instance'], unique=True)),
        ))
        db.send_create_signal('accounts', ['UserProfileVariantsForInstance'])

        # Adding M2M table for field stake_variants on 'UserProfileVariantsForInstance'
        db.create_table('accounts_userprofilevariantsforinstance_stake_variants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofilevariantsforinstance', models.ForeignKey(orm['accounts.userprofilevariantsforinstance'], null=False)),
            ('userprofilestake', models.ForeignKey(orm['accounts.userprofilestake'], null=False))
        ))
        db.create_unique('accounts_userprofilevariantsforinstance_stake_variants', ['userprofilevariantsforinstance_id', 'userprofilestake_id'])

        # Adding M2M table for field gender_variants on 'UserProfileVariantsForInstance'
        db.create_table('accounts_userprofilevariantsforinstance_gender_variants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofilevariantsforinstance', models.ForeignKey(orm['accounts.userprofilevariantsforinstance'], null=False)),
            ('userprofilegender', models.ForeignKey(orm['accounts.userprofilegender'], null=False))
        ))
        db.create_unique('accounts_userprofilevariantsforinstance_gender_variants', ['userprofilevariantsforinstance_id', 'userprofilegender_id'])

        # Adding M2M table for field race_variants on 'UserProfileVariantsForInstance'
        db.create_table('accounts_userprofilevariantsforinstance_race_variants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofilevariantsforinstance', models.ForeignKey(orm['accounts.userprofilevariantsforinstance'], null=False)),
            ('userprofilerace', models.ForeignKey(orm['accounts.userprofilerace'], null=False))
        ))
        db.create_unique('accounts_userprofilevariantsforinstance_race_variants', ['userprofilevariantsforinstance_id', 'userprofilerace_id'])

        # Adding M2M table for field education_variants on 'UserProfileVariantsForInstance'
        db.create_table('accounts_userprofilevariantsforinstance_education_variants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofilevariantsforinstance', models.ForeignKey(orm['accounts.userprofilevariantsforinstance'], null=False)),
            ('userprofileeducation', models.ForeignKey(orm['accounts.userprofileeducation'], null=False))
        ))
        db.create_unique('accounts_userprofilevariantsforinstance_education_variants', ['userprofilevariantsforinstance_id', 'userprofileeducation_id'])

        # Adding M2M table for field income_variants on 'UserProfileVariantsForInstance'
        db.create_table('accounts_userprofilevariantsforinstance_income_variants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofilevariantsforinstance', models.ForeignKey(orm['accounts.userprofilevariantsforinstance'], null=False)),
            ('userprofileincome', models.ForeignKey(orm['accounts.userprofileincome'], null=False))
        ))
        db.create_unique('accounts_userprofilevariantsforinstance_income_variants', ['userprofilevariantsforinstance_id', 'userprofileincome_id'])

        # Adding M2M table for field living_variants on 'UserProfileVariantsForInstance'
        db.create_table('accounts_userprofilevariantsforinstance_living_variants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofilevariantsforinstance', models.ForeignKey(orm['accounts.userprofilevariantsforinstance'], null=False)),
            ('userprofilelivingsituation', models.ForeignKey(orm['accounts.userprofilelivingsituation'], null=False))
        ))
        db.create_unique('accounts_userprofilevariantsforinstance_living_variants', ['userprofilevariantsforinstance_id', 'userprofilelivingsituation_id'])

        # Adding M2M table for field how_discovered_variants on 'UserProfileVariantsForInstance'
        db.create_table('accounts_userprofilevariantsforinstance_how_discovered_variants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofilevariantsforinstance', models.ForeignKey(orm['accounts.userprofilevariantsforinstance'], null=False)),
            ('userprofilehowdiscovered', models.ForeignKey(orm['accounts.userprofilehowdiscovered'], null=False))
        ))
        db.create_unique('accounts_userprofilevariantsforinstance_how_discovered_variants', ['userprofilevariantsforinstance_id', 'userprofilehowdiscovered_id'])


    def backwards(self, orm):
        
        # Deleting model 'UserProfilePerInstance'
        db.delete_table('accounts_userprofileperinstance')

        # Deleting model 'UserProfileVariantsForInstance'
        db.delete_table('accounts_userprofilevariantsforinstance')

        # Removing M2M table for field stake_variants on 'UserProfileVariantsForInstance'
        db.delete_table('accounts_userprofilevariantsforinstance_stake_variants')

        # Removing M2M table for field gender_variants on 'UserProfileVariantsForInstance'
        db.delete_table('accounts_userprofilevariantsforinstance_gender_variants')

        # Removing M2M table for field race_variants on 'UserProfileVariantsForInstance'
        db.delete_table('accounts_userprofilevariantsforinstance_race_variants')

        # Removing M2M table for field education_variants on 'UserProfileVariantsForInstance'
        db.delete_table('accounts_userprofilevariantsforinstance_education_variants')

        # Removing M2M table for field income_variants on 'UserProfileVariantsForInstance'
        db.delete_table('accounts_userprofilevariantsforinstance_income_variants')

        # Removing M2M table for field living_variants on 'UserProfileVariantsForInstance'
        db.delete_table('accounts_userprofilevariantsforinstance_living_variants')

        # Removing M2M table for field how_discovered_variants on 'UserProfileVariantsForInstance'
        db.delete_table('accounts_userprofilevariantsforinstance_how_discovered_variants')


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
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'affiliations': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'affils': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['instances.Affiliation']", 'symmetrical': 'False'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birth_year': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'coinPoints': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'currentCoins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'education': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileEducation']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250', 'blank': 'True'}),
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileGender']", 'null': 'True', 'blank': 'True'}),
            'how_discovered': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileHowDiscovered']", 'null': 'True', 'blank': 'True'}),
            'how_discovered_other': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileIncome']", 'null': 'True', 'blank': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_profiles'", 'null': 'True', 'to': "orm['instances.Instance']"}),
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_profiles_list'", 'to': "orm['instances.Instance']", 'through': "orm['accounts.UserProfilePerInstance']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'living': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileLivingSituation']", 'null': 'True', 'blank': 'True'}),
            'preferred_language': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '5'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileRace']", 'null': 'True', 'blank': 'True'}),
            'receive_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'stake': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileStake']", 'null': 'True', 'blank': 'True'}),
            'totalPoints': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'})
        },
        'accounts.userprofileeducation': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileEducation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofileeducationtranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'UserProfileEducationTranslation'},
            'education': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['accounts.UserProfileEducation']"})
        },
        'accounts.userprofilegender': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileGender'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofilegendertranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'UserProfileGenderTranslation'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['accounts.UserProfileGender']"})
        },
        'accounts.userprofilehowdiscovered': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileHowDiscovered'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofilehowdiscoveredtranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'UserProfileHowDiscoveredTranslation'},
            'how': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['accounts.UserProfileHowDiscovered']"})
        },
        'accounts.userprofileincome': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileIncome'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofileincometranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'UserProfileIncomeTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['accounts.UserProfileIncome']"})
        },
        'accounts.userprofilelivingsituation': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileLivingSituation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofilelivingsituationtranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'UserProfileLivingSituationTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['accounts.UserProfileLivingSituation']"}),
            'situation': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'accounts.userprofileperinstance': {
            'Meta': {'object_name': 'UserProfilePerInstance'},
            'education': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileEducation']", 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileGender']", 'null': 'True', 'blank': 'True'}),
            'how_discovered': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileHowDiscovered']", 'null': 'True', 'blank': 'True'}),
            'how_discovered_other': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileIncome']", 'null': 'True', 'blank': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'living': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileLivingSituation']", 'null': 'True', 'blank': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileRace']", 'null': 'True', 'blank': 'True'}),
            'stake': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileStake']", 'null': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.UserProfile']"})
        },
        'accounts.userprofilerace': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileRace'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofileracetranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'UserProfileRaceTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['accounts.UserProfileRace']"}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'accounts.userprofilestake': {
            'Meta': {'ordering': "('pos',)", 'object_name': 'UserProfileStake'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofilestaketranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'UserProfileStakeTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['accounts.UserProfileStake']"}),
            'stake': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'accounts.userprofilevariantsforinstance': {
            'Meta': {'object_name': 'UserProfileVariantsForInstance'},
            'education_variants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['accounts.UserProfileEducation']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'gender_variants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['accounts.UserProfileGender']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'how_discovered_variants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['accounts.UserProfileHowDiscovered']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income_variants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['accounts.UserProfileIncome']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'instance': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['instances.Instance']", 'unique': 'True'}),
            'living_variants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['accounts.UserProfileLivingSituation']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'race_variants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['accounts.UserProfileRace']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'stake_variants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['accounts.UserProfileStake']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'})
        },
        'attachments.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']", 'null': 'True', 'blank': 'True'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_validity_check': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
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
        'comments.comment': {
            'Meta': {'object_name': 'Comment'},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments.Attachment']", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'content_type_set_for_comment'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'flagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comments'", 'null': 'True', 'to': "orm['instances.Instance']"}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'liked_comments'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'posted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
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
        'instances.instance': {
            'Meta': {'object_name': 'Instance'},
            'affiliations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['instances.Affiliation']", 'symmetrical': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'curators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'days_for_mission': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['instances.Language']", 'symmetrical': 'False'}),
            'location': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'instances.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']
