# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfileRaceTranslation'
        db.create_table('accounts_userprofileracetranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('race', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileRace'])),
        ))
        db.send_create_signal('accounts', ['UserProfileRaceTranslation'])

        # Adding unique constraint on 'UserProfileRaceTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofileracetranslation', ['language_code', 'master_id'])

        # Adding model 'UserProfileGender'
        db.create_table('accounts_userprofilegender', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instances.Instance'])),
        ))
        db.send_create_signal('accounts', ['UserProfileGender'])

        # Adding model 'UserProfileLivingSituation'
        db.create_table('accounts_userprofilelivingsituation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instances.Instance'])),
        ))
        db.send_create_signal('accounts', ['UserProfileLivingSituation'])

        # Adding model 'UserProfileStakeTranslation'
        db.create_table('accounts_userprofilestaketranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stake', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileStake'])),
        ))
        db.send_create_signal('accounts', ['UserProfileStakeTranslation'])

        # Adding unique constraint on 'UserProfileStakeTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofilestaketranslation', ['language_code', 'master_id'])

        # Adding model 'UserProfileLivingSituationTranslation'
        db.create_table('accounts_userprofilelivingsituationtranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('situation', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileLivingSituation'])),
        ))
        db.send_create_signal('accounts', ['UserProfileLivingSituationTranslation'])

        # Adding unique constraint on 'UserProfileLivingSituationTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofilelivingsituationtranslation', ['language_code', 'master_id'])

        # Adding model 'UserProfileIncomeTranslation'
        db.create_table('accounts_userprofileincometranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('income', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileIncome'])),
        ))
        db.send_create_signal('accounts', ['UserProfileIncomeTranslation'])

        # Adding unique constraint on 'UserProfileIncomeTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofileincometranslation', ['language_code', 'master_id'])

        # Adding model 'UserProfileRace'
        db.create_table('accounts_userprofilerace', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instances.Instance'])),
        ))
        db.send_create_signal('accounts', ['UserProfileRace'])

        # Adding model 'UserProfileEducationTranslation'
        db.create_table('accounts_userprofileeducationtranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('education', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileEducation'])),
        ))
        db.send_create_signal('accounts', ['UserProfileEducationTranslation'])

        # Adding unique constraint on 'UserProfileEducationTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofileeducationtranslation', ['language_code', 'master_id'])

        # Adding model 'UserProfileHowDiscoveredTranslation'
        db.create_table('accounts_userprofilehowdiscoveredtranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('how', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileHowDiscovered'])),
        ))
        db.send_create_signal('accounts', ['UserProfileHowDiscoveredTranslation'])

        # Adding unique constraint on 'UserProfileHowDiscoveredTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofilehowdiscoveredtranslation', ['language_code', 'master_id'])

        # Adding model 'UserProfileEducation'
        db.create_table('accounts_userprofileeducation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instances.Instance'])),
        ))
        db.send_create_signal('accounts', ['UserProfileEducation'])

        # Adding model 'UserProfileStake'
        db.create_table('accounts_userprofilestake', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instances.Instance'])),
        ))
        db.send_create_signal('accounts', ['UserProfileStake'])

        # Adding model 'UserProfileIncome'
        db.create_table('accounts_userprofileincome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instances.Instance'])),
        ))
        db.send_create_signal('accounts', ['UserProfileIncome'])

        # Adding model 'UserProfileGenderTranslation'
        db.create_table('accounts_userprofilegendertranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['accounts.UserProfileGender'])),
        ))
        db.send_create_signal('accounts', ['UserProfileGenderTranslation'])

        # Adding unique constraint on 'UserProfileGenderTranslation', fields ['language_code', 'master']
        db.create_unique('accounts_userprofilegendertranslation', ['language_code', 'master_id'])

        # Adding model 'UserProfileHowDiscovered'
        db.create_table('accounts_userprofilehowdiscovered', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instances.Instance'])),
        ))
        db.send_create_signal('accounts', ['UserProfileHowDiscovered'])

        # Deleting field 'UserProfile.phone_number'
        db.delete_column('accounts_userprofile', 'phone_number')

        # Deleting field 'UserProfile.accepted_term'
        db.delete_column('accounts_userprofile', 'accepted_term')

        # Deleting field 'UserProfile.editedProfile'
        db.delete_column('accounts_userprofile', 'editedProfile')

        # Deleting field 'UserProfile.flagged'
        db.delete_column('accounts_userprofile', 'flagged')

        # Deleting field 'UserProfile.accepted_research'
        db.delete_column('accounts_userprofile', 'accepted_research')

        # Deleting field 'UserProfile.receive_email'
        db.delete_column('accounts_userprofile', 'receive_email')

        # Adding field 'UserProfile.stake'
        db.add_column('accounts_userprofile', 'stake', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileStake'], null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.gender'
        db.add_column('accounts_userprofile', 'gender', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileGender'], null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.race'
        db.add_column('accounts_userprofile', 'race', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileRace'], null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.education'
        db.add_column('accounts_userprofile', 'education', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileEducation'], null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.income'
        db.add_column('accounts_userprofile', 'income', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileIncome'], null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.living'
        db.add_column('accounts_userprofile', 'living', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileLivingSituation'], null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.how_discovered'
        db.add_column('accounts_userprofile', 'how_discovered', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileHowDiscovered'], null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.how_discovered_other'
        db.add_column('accounts_userprofile', 'how_discovered_other', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Removing unique constraint on 'UserProfileGenderTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofilegendertranslation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileHowDiscoveredTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofilehowdiscoveredtranslation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileEducationTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofileeducationtranslation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileIncomeTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofileincometranslation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileLivingSituationTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofilelivingsituationtranslation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileStakeTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofilestaketranslation', ['language_code', 'master_id'])

        # Removing unique constraint on 'UserProfileRaceTranslation', fields ['language_code', 'master']
        db.delete_unique('accounts_userprofileracetranslation', ['language_code', 'master_id'])

        # Deleting model 'UserProfileRaceTranslation'
        db.delete_table('accounts_userprofileracetranslation')

        # Deleting model 'UserProfileGender'
        db.delete_table('accounts_userprofilegender')

        # Deleting model 'UserProfileLivingSituation'
        db.delete_table('accounts_userprofilelivingsituation')

        # Deleting model 'UserProfileStakeTranslation'
        db.delete_table('accounts_userprofilestaketranslation')

        # Deleting model 'UserProfileLivingSituationTranslation'
        db.delete_table('accounts_userprofilelivingsituationtranslation')

        # Deleting model 'UserProfileIncomeTranslation'
        db.delete_table('accounts_userprofileincometranslation')

        # Deleting model 'UserProfileRace'
        db.delete_table('accounts_userprofilerace')

        # Deleting model 'UserProfileEducationTranslation'
        db.delete_table('accounts_userprofileeducationtranslation')

        # Deleting model 'UserProfileHowDiscoveredTranslation'
        db.delete_table('accounts_userprofilehowdiscoveredtranslation')

        # Deleting model 'UserProfileEducation'
        db.delete_table('accounts_userprofileeducation')

        # Deleting model 'UserProfileStake'
        db.delete_table('accounts_userprofilestake')

        # Deleting model 'UserProfileIncome'
        db.delete_table('accounts_userprofileincome')

        # Deleting model 'UserProfileGenderTranslation'
        db.delete_table('accounts_userprofilegendertranslation')

        # Deleting model 'UserProfileHowDiscovered'
        db.delete_table('accounts_userprofilehowdiscovered')

        # Adding field 'UserProfile.phone_number'
        db.add_column('accounts_userprofile', 'phone_number', self.gf('django.db.models.fields.CharField')(default='', max_length=12, blank=True), keep_default=False)

        # Adding field 'UserProfile.accepted_term'
        db.add_column('accounts_userprofile', 'accepted_term', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'UserProfile.editedProfile'
        db.add_column('accounts_userprofile', 'editedProfile', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'UserProfile.flagged'
        db.add_column('accounts_userprofile', 'flagged', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'UserProfile.accepted_research'
        db.add_column('accounts_userprofile', 'accepted_research', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'UserProfile.receive_email'
        db.add_column('accounts_userprofile', 'receive_email', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Deleting field 'UserProfile.stake'
        db.delete_column('accounts_userprofile', 'stake_id')

        # Deleting field 'UserProfile.gender'
        db.delete_column('accounts_userprofile', 'gender_id')

        # Deleting field 'UserProfile.race'
        db.delete_column('accounts_userprofile', 'race_id')

        # Deleting field 'UserProfile.education'
        db.delete_column('accounts_userprofile', 'education_id')

        # Deleting field 'UserProfile.income'
        db.delete_column('accounts_userprofile', 'income_id')

        # Deleting field 'UserProfile.living'
        db.delete_column('accounts_userprofile', 'living_id')

        # Deleting field 'UserProfile.how_discovered'
        db.delete_column('accounts_userprofile', 'how_discovered_id')

        # Deleting field 'UserProfile.how_discovered_other'
        db.delete_column('accounts_userprofile', 'how_discovered_other')


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
            'affiliations': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birth_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'living': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileLivingSituation']", 'null': 'True', 'blank': 'True'}),
            'preferred_language': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '5'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileRace']", 'null': 'True', 'blank': 'True'}),
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
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['instances.Instance']"}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'liked_comments'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'posted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'instances.instance': {
            'Meta': {'object_name': 'Instance'},
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
