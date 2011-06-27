# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfileIncomes'
        db.create_table('accounts_userprofileincomes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('income', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('accounts', ['UserProfileIncomes'])

        # Adding model 'UserProfileEducation'
        db.create_table('accounts_userprofileeducation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eduLevel', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('accounts', ['UserProfileEducation'])

        # Adding model 'UserProfileLiving'
        db.create_table('accounts_userprofileliving', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('livingSituation', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('accounts', ['UserProfileLiving'])

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

        # Adding model 'UserProfile'
        db.create_table('accounts_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instances.Instance'], null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileGender'], null=True, blank=True)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileRace'], null=True, blank=True)),
            ('stake', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileStake'], null=True, blank=True)),
            ('education', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileEducation'], null=True, blank=True)),
            ('income', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileIncomes'], null=True, blank=True)),
            ('living', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['accounts.UserProfileLiving'], null=True, blank=True)),
            ('accepted_term', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accepted_research', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('currentCoins', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('totalPoints', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('coinPoints', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('flagged', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('affiliations', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('editedProfile', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('birth_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfile'])

        # Adding M2M table for field following on 'UserProfile'
        db.create_table('accounts_userprofile_following', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['accounts.userprofile'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('accounts_userprofile_following', ['userprofile_id', 'user_id'])

        # Adding M2M table for field comments on 'UserProfile'
        db.create_table('accounts_userprofile_comments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['accounts.userprofile'], null=False)),
            ('comment', models.ForeignKey(orm['comments.comment'], null=False))
        ))
        db.create_unique('accounts_userprofile_comments', ['userprofile_id', 'comment_id'])


    def backwards(self, orm):
        
        # Deleting model 'UserProfileIncomes'
        db.delete_table('accounts_userprofileincomes')

        # Deleting model 'UserProfileEducation'
        db.delete_table('accounts_userprofileeducation')

        # Deleting model 'UserProfileLiving'
        db.delete_table('accounts_userprofileliving')

        # Deleting model 'UserProfileGender'
        db.delete_table('accounts_userprofilegender')

        # Deleting model 'UserProfileRace'
        db.delete_table('accounts_userprofilerace')

        # Deleting model 'UserProfileStake'
        db.delete_table('accounts_userprofilestake')

        # Deleting model 'UserProfile'
        db.delete_table('accounts_userprofile')

        # Removing M2M table for field following on 'UserProfile'
        db.delete_table('accounts_userprofile_following')

        # Removing M2M table for field comments on 'UserProfile'
        db.delete_table('accounts_userprofile_comments')


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
            'editedProfile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'education': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['accounts.UserProfileEducation']", 'null': 'True', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['accounts']