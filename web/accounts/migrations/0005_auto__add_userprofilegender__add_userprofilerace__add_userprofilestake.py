# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfileGender'
        db.create_table('accounts_userprofilegender', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('accounts', ['UserProfileGender'])

        # Adding model 'UserProfileRace'
        db.create_table('accounts_userprofilerace', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('race', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('accounts', ['UserProfileRace'])

        # Adding model 'UserProfileStake'
        db.create_table('accounts_userprofilestake', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stake', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('accounts', ['UserProfileStake'])

        # Deleting field 'UserProfile.username'
        db.delete_column('accounts_userprofile', 'username')

        # Deleting field 'UserProfile.last_name'
        db.delete_column('accounts_userprofile', 'last_name')

        # Deleting field 'UserProfile.points_multiplier'
        db.delete_column('accounts_userprofile', 'points_multiplier')

        # Deleting field 'UserProfile.first_name'
        db.delete_column('accounts_userprofile', 'first_name')

        # Deleting field 'UserProfile.coins'
        db.delete_column('accounts_userprofile', 'coins')

        # Deleting field 'UserProfile.is_of_age'
        db.delete_column('accounts_userprofile', 'is_of_age')

        # Deleting field 'UserProfile.points'
        db.delete_column('accounts_userprofile', 'points')

        # Deleting field 'UserProfile.email'
        db.delete_column('accounts_userprofile', 'email')

        # Deleting field 'UserProfile.completed'
        db.delete_column('accounts_userprofile', 'completed')

        # Deleting field 'UserProfile.location_tracking'
        db.delete_column('accounts_userprofile', 'location_tracking')

        # Deleting field 'UserProfile.generated_password'
        db.delete_column('accounts_userprofile', 'generated_password')

        # Adding field 'UserProfile.currentCoins'
        db.add_column('accounts_userprofile', 'currentCoins', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.totalPoints'
        db.add_column('accounts_userprofile', 'totalPoints', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.coinPoints'
        db.add_column('accounts_userprofile', 'coinPoints', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Removing M2M table for field player_challenges on 'UserProfile'
        db.delete_table('accounts_userprofile_player_challenges')

        # Renaming column for 'UserProfile.gender' to match new field type.
        db.rename_column('accounts_userprofile', 'gender', 'gender_id')
        # Changing field 'UserProfile.gender'
        db.alter_column('accounts_userprofile', 'gender_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.UserProfileGender'], null=True))

        # Adding index on 'UserProfile', fields ['gender']
        db.create_index('accounts_userprofile', ['gender_id'])

        # Renaming column for 'UserProfile.stake' to match new field type.
        db.rename_column('accounts_userprofile', 'stake', 'stake_id')
        # Changing field 'UserProfile.stake'
        db.alter_column('accounts_userprofile', 'stake_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.UserProfileStake'], null=True))

        # Adding index on 'UserProfile', fields ['stake']
        db.create_index('accounts_userprofile', ['stake_id'])

        # Renaming column for 'UserProfile.race' to match new field type.
        db.rename_column('accounts_userprofile', 'race', 'race_id')
        # Changing field 'UserProfile.race'
        db.alter_column('accounts_userprofile', 'race_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.UserProfileRace'], null=True))

        # Adding index on 'UserProfile', fields ['race']
        db.create_index('accounts_userprofile', ['race_id'])


    def backwards(self, orm):
        
        # Removing index on 'UserProfile', fields ['race']
        db.delete_index('accounts_userprofile', ['race_id'])

        # Removing index on 'UserProfile', fields ['stake']
        db.delete_index('accounts_userprofile', ['stake_id'])

        # Removing index on 'UserProfile', fields ['gender']
        db.delete_index('accounts_userprofile', ['gender_id'])

        # Deleting model 'UserProfileGender'
        db.delete_table('accounts_userprofilegender')

        # Deleting model 'UserProfileRace'
        db.delete_table('accounts_userprofilerace')

        # Deleting model 'UserProfileStake'
        db.delete_table('accounts_userprofilestake')

        # Adding field 'UserProfile.username'
        db.add_column('accounts_userprofile', 'username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.last_name'
        db.add_column('accounts_userprofile', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.points_multiplier'
        db.add_column('accounts_userprofile', 'points_multiplier', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.first_name'
        db.add_column('accounts_userprofile', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.coins'
        db.add_column('accounts_userprofile', 'coins', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.is_of_age'
        db.add_column('accounts_userprofile', 'is_of_age', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'UserProfile.points'
        db.add_column('accounts_userprofile', 'points', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.email'
        db.add_column('accounts_userprofile', 'email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'UserProfile.completed'
        db.add_column('accounts_userprofile', 'completed', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'UserProfile.location_tracking'
        db.add_column('accounts_userprofile', 'location_tracking', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'UserProfile.generated_password'
        db.add_column('accounts_userprofile', 'generated_password', self.gf('django.db.models.fields.CharField')(default='', max_length=260), keep_default=False)

        # Deleting field 'UserProfile.currentCoins'
        db.delete_column('accounts_userprofile', 'currentCoins')

        # Deleting field 'UserProfile.totalPoints'
        db.delete_column('accounts_userprofile', 'totalPoints')

        # Deleting field 'UserProfile.coinPoints'
        db.delete_column('accounts_userprofile', 'coinPoints')

        # Adding M2M table for field player_challenges on 'UserProfile'
        db.create_table('accounts_userprofile_player_challenges', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['accounts.userprofile'], null=False)),
            ('playerchallenge', models.ForeignKey(orm['challenges.playerchallenge'], null=False))
        ))
        db.create_unique('accounts_userprofile_player_challenges', ['userprofile_id', 'playerchallenge_id'])

        # Renaming column for 'UserProfile.gender' to match new field type.
        db.rename_column('accounts_userprofile', 'gender_id', 'gender')
        # Changing field 'UserProfile.gender'
        db.alter_column('accounts_userprofile', 'gender', self.gf('django.db.models.fields.CharField')(max_length=64, null=True))

        # Renaming column for 'UserProfile.stake' to match new field type.
        db.rename_column('accounts_userprofile', 'stake_id', 'stake')
        # Changing field 'UserProfile.stake'
        db.alter_column('accounts_userprofile', 'stake', self.gf('django.db.models.fields.CharField')(max_length=125, null=True))

        # Renaming column for 'UserProfile.race' to match new field type.
        db.rename_column('accounts_userprofile', 'race_id', 'race')
        # Changing field 'UserProfile.race'
        db.alter_column('accounts_userprofile', 'race', self.gf('django.db.models.fields.CharField')(max_length=125, null=True))


    models = {
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'accepted_research': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'accepted_term': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'affiliations': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birth_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coinPoints': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['comments.Comment']", 'null': 'True', 'blank': 'True'}),
            'currentCoins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'education': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileEducation']", 'null': 'True', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'following_user_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileGender']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileIncomes']", 'null': 'True', 'blank': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']", 'null': 'True', 'blank': 'True'}),
            'living': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileLiving']", 'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileRace']", 'null': 'True', 'blank': 'True'}),
            'stake': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileStake']", 'null': 'True', 'blank': 'True'}),
            'totalPoints': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'accounts.userprofileeducation': {
            'Meta': {'object_name': 'UserProfileEducation'},
            'eduLevel': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofilegender': {
            'Meta': {'object_name': 'UserProfileGender'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofileincomes': {
            'Meta': {'object_name': 'UserProfileIncomes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofileliving': {
            'Meta': {'object_name': 'UserProfileLiving'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'livingSituation': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'accounts.userprofilerace': {
            'Meta': {'object_name': 'UserProfileRace'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'accounts.userprofilestake': {
            'Meta': {'object_name': 'UserProfileStake'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {}),
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
            'type': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
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
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['comments.Comment']", 'symmetrical': 'False', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'liked_comments'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'posted_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'curator': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['accounts']
