# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Challenge'
        db.create_table('challenges_challenge', (
            ('basetreenode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['instances.BaseTreeNode'], unique=True, primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('challenge_type', self.gf('django.db.models.fields.IntegerField')(max_length=1, null=True)),
            ('mission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='challenges_challenge_related', to=orm['missions.Mission'])),
            ('is_player_submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('challenges', ['Challenge'])

        # Adding model 'SingleResponseChallenge'
        db.create_table('challenges_singleresponsechallenge', (
            ('challenge_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Challenge'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('challenges', ['SingleResponseChallenge'])

        # Adding model 'MultiResponseChallenge'
        db.create_table('challenges_multiresponsechallenge', (
            ('challenge_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Challenge'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('challenges', ['MultiResponseChallenge'])

        # Adding model 'MapChallenge'
        db.create_table('challenges_mapchallenge', (
            ('challenge_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Challenge'], unique=True, primary_key=True)),
            ('maxNumMarkers', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal('challenges', ['MapChallenge'])

        # Adding model 'EmpathyChallenge'
        db.create_table('challenges_empathychallenge', (
            ('challenge_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Challenge'], unique=True, primary_key=True)),
            ('bio_text', self.gf('django.db.models.fields.TextField')(default='', max_length=1000)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('challenges', ['EmpathyChallenge'])

        # Adding model 'AnswerChoice'
        db.create_table('challenges_answerchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answer_choices', to=orm['challenges.Challenge'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('trivia_correct_answer', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('challenges', ['AnswerChoice'])

        # Adding model 'Answer'
        db.create_table('challenges_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['auth.User'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('challenges', ['Answer'])

        # Adding model 'AnswerWithChoices'
        db.create_table('challenges_answerwithchoices', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='singleresponse_answers', to=orm['challenges.Challenge'])),
        ))
        db.send_create_signal('challenges', ['AnswerWithChoices'])

        # Adding M2M table for field selected on 'AnswerWithChoices'
        db.create_table('challenges_answerwithchoices_selected', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('answerwithchoices', models.ForeignKey(orm['challenges.answerwithchoices'], null=False)),
            ('answerchoice', models.ForeignKey(orm['challenges.answerchoice'], null=False))
        ))
        db.create_unique('challenges_answerwithchoices_selected', ['answerwithchoices_id', 'answerchoice_id'])

        # Adding model 'AnswerMap'
        db.create_table('challenges_answermap', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
            ('map', self.gf('gmapsfield.fields.GoogleMapsField')()),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='map_answers', to=orm['challenges.MapChallenge'])),
        ))
        db.send_create_signal('challenges', ['AnswerMap'])

        # Adding model 'AnswerEmpathy'
        db.create_table('challenges_answerempathy', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')(default='', max_length=1000)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='empathy_answers', to=orm['challenges.EmpathyChallenge'])),
        ))
        db.send_create_signal('challenges', ['AnswerEmpathy'])

        # Adding model 'AnswerOpenEnded'
        db.create_table('challenges_answeropenended', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')(default='', max_length=1000)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='openended_answers', to=orm['challenges.Challenge'])),
        ))
        db.send_create_signal('challenges', ['AnswerOpenEnded'])


    def backwards(self, orm):
        # Deleting model 'Challenge'
        db.delete_table('challenges_challenge')

        # Deleting model 'SingleResponseChallenge'
        db.delete_table('challenges_singleresponsechallenge')

        # Deleting model 'MultiResponseChallenge'
        db.delete_table('challenges_multiresponsechallenge')

        # Deleting model 'MapChallenge'
        db.delete_table('challenges_mapchallenge')

        # Deleting model 'EmpathyChallenge'
        db.delete_table('challenges_empathychallenge')

        # Deleting model 'AnswerChoice'
        db.delete_table('challenges_answerchoice')

        # Deleting model 'Answer'
        db.delete_table('challenges_answer')

        # Deleting model 'AnswerWithChoices'
        db.delete_table('challenges_answerwithchoices')

        # Removing M2M table for field selected on 'AnswerWithChoices'
        db.delete_table('challenges_answerwithchoices_selected')

        # Deleting model 'AnswerMap'
        db.delete_table('challenges_answermap')

        # Deleting model 'AnswerEmpathy'
        db.delete_table('challenges_answerempathy')

        # Deleting model 'AnswerOpenEnded'
        db.delete_table('challenges_answeropenended')


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
        'challenges.answer': {
            'Meta': {'object_name': 'Answer'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['auth.User']"})
        },
        'challenges.answerchoice': {
            'Meta': {'object_name': 'AnswerChoice'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer_choices'", 'to': "orm['challenges.Challenge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trivia_correct_answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'challenges.answerempathy': {
            'Meta': {'object_name': 'AnswerEmpathy', '_ormbases': ['challenges.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'empathy_answers'", 'to': "orm['challenges.EmpathyChallenge']"}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1000'})
        },
        'challenges.answermap': {
            'Meta': {'object_name': 'AnswerMap', '_ormbases': ['challenges.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'map_answers'", 'to': "orm['challenges.MapChallenge']"}),
            'map': ('gmapsfield.fields.GoogleMapsField', [], {})
        },
        'challenges.answeropenended': {
            'Meta': {'object_name': 'AnswerOpenEnded', '_ormbases': ['challenges.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'openended_answers'", 'to': "orm['challenges.Challenge']"}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1000'})
        },
        'challenges.answerwithchoices': {
            'Meta': {'object_name': 'AnswerWithChoices', '_ormbases': ['challenges.Answer']},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'singleresponse_answers'", 'to': "orm['challenges.Challenge']"}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'selected': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'singleresponse_answers'", 'symmetrical': 'False', 'to': "orm['challenges.AnswerChoice']"})
        },
        'challenges.challenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'Challenge', '_ormbases': ['instances.BaseTreeNode']},
            'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['instances.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'challenge_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'null': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_player_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'challenges_challenge_related'", 'to': "orm['missions.Mission']"}),
            'question': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'})
        },
        'challenges.empathychallenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'EmpathyChallenge', '_ormbases': ['challenges.Challenge']},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bio_text': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1000'}),
            'challenge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Challenge']", 'unique': 'True', 'primary_key': 'True'})
        },
        'challenges.mapchallenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'MapChallenge', '_ormbases': ['challenges.Challenge']},
            'challenge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Challenge']", 'unique': 'True', 'primary_key': 'True'}),
            'maxNumMarkers': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        'challenges.multiresponsechallenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'MultiResponseChallenge', '_ormbases': ['challenges.Challenge']},
            'challenge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Challenge']", 'unique': 'True', 'primary_key': 'True'})
        },
        'challenges.singleresponsechallenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'SingleResponseChallenge', '_ormbases': ['challenges.Challenge']},
            'challenge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Challenge']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'Meta': {'ordering': "('end_date',)", 'object_name': 'Mission', '_ormbases': ['instances.BaseTreeNode']},
            'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['instances.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'missions'", 'to': "orm['instances.Instance']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'video': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['challenges']