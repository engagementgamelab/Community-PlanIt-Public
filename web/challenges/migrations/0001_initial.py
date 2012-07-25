# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChallengeType'
        db.create_table('player_activities_playeractivitytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('displayType', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('defaultPoints', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('challenges', ['ChallengeType'])

        # Adding model 'ChallengeTranslation'
        db.create_table('player_activities_playeractivity_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('instructions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('addInstructions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['challenges.Challenge'])),
        ))
        db.send_create_signal('challenges', ['ChallengeTranslation'])

        # Adding unique constraint on 'ChallengeTranslation', fields ['language_code', 'master']
        db.create_unique('player_activities_playeractivity_translation', ['language_code', 'master_id'])

        # Adding model 'Challenge'
        db.create_table('player_activities_playeractivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creationUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('mission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='challenges_challenge_related', to=orm['missions.Mission'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.ChallengeType'])),
            ('createDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('comment_required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_player_submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('challenges', ['Challenge'])

        # Adding M2M table for field attachment on 'Challenge'
        db.create_table('player_activities_playeractivity_attachment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('challenge', models.ForeignKey(orm['challenges.challenge'], null=False)),
            ('attachment', models.ForeignKey(orm['attachments_v2.attachment'], null=False))
        ))
        db.create_unique('player_activities_playeractivity_attachment', ['challenge_id', 'attachment_id'])

        # Adding model 'MapChallengeTranslation'
        db.create_table(['player_activities_playermapactivity_translation'], (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('instructions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('addInstructions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['challenges.MapChallenge'])),
        ))
        db.send_create_signal('challenges', ['MapChallengeTranslation'])

        # Adding unique constraint on 'MapChallengeTranslation', fields ['language_code', 'master']
        db.create_unique(['player_activities_playermapactivity_translation'], ['language_code', 'master_id'])

        # Adding model 'MapChallenge'
        db.create_table('player_activities_playermapactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creationUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('mission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='challenges_mapchallenge_related', to=orm['missions.Mission'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.ChallengeType'])),
            ('createDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('comment_required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_player_submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('maxNumMarkers', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal('challenges', ['MapChallenge'])

        # Adding M2M table for field attachment on 'MapChallenge'
        db.create_table('player_activities_playermapactivity_attachment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mapchallenge', models.ForeignKey(orm['challenges.mapchallenge'], null=False)),
            ('attachment', models.ForeignKey(orm['attachments_v2.attachment'], null=False))
        ))
        db.create_unique('player_activities_playermapactivity_attachment', ['mapchallenge_id', 'attachment_id'])

        # Adding model 'EmpathyChallengeTranslation'
        db.create_table('player_activities_playerempathyactivity_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('instructions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('addInstructions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['challenges.EmpathyChallenge'])),
        ))
        db.send_create_signal('challenges', ['EmpathyChallengeTranslation'])

        # Adding unique constraint on 'EmpathyChallengeTranslation', fields ['language_code', 'master']
        db.create_unique('player_activities_playerempathyactivity_translation', ['language_code', 'master_id'])

        # Adding model 'EmpathyChallenge'
        db.create_table('player_activities_playerempathyactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creationUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('mission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='challenges_empathychallenge_related', to=orm['missions.Mission'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.ChallengeType'])),
            ('createDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('comment_required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_player_submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('challenges', ['EmpathyChallenge'])

        # Adding M2M table for field attachment on 'EmpathyChallenge'
        db.create_table('player_activities_playerempathyactivity_attachment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('empathychallenge', models.ForeignKey(orm['challenges.empathychallenge'], null=False)),
            ('attachment', models.ForeignKey(orm['attachments_v2.attachment'], null=False))
        ))
        db.create_unique('player_activities_playerempathyactivity_attachment', ['empathychallenge_id', 'attachment_id'])

        # Adding model 'MultiChoiceActivityTranslation'
        db.create_table('player_activities_multichoiceactivity_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['challenges.MultiChoiceActivity'])),
        ))
        db.send_create_signal('challenges', ['MultiChoiceActivityTranslation'])

        # Adding unique constraint on 'MultiChoiceActivityTranslation', fields ['language_code', 'master']
        db.create_unique('player_activities_multichoiceactivity_translation', ['language_code', 'master_id'])

        # Adding model 'MultiChoiceActivity'
        db.create_table('player_activities_multichoiceactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answer_choices', to=orm['challenges.Challenge'])),
            ('trivia_correct_answer', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('challenges', ['MultiChoiceActivity'])

        # Adding model 'Answer'
        db.create_table('answers_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answerUser', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['auth.User'])),
            ('createDate', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('challenges', ['Answer'])

        # Adding model 'AnswerSingleResponse'
        db.create_table('answers_answersingleresponse', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
            ('selected', self.gf('django.db.models.fields.related.ForeignKey')(related_name='singleresponse_answers', to=orm['challenges.MultiChoiceActivity'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='singleresponse_answers', to=orm['challenges.Challenge'])),
        ))
        db.send_create_signal('challenges', ['AnswerSingleResponse'])

        # Adding model 'AnswerMultiChoice'
        db.create_table('answers_answermultichoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(related_name='multichoice_answers', to=orm['challenges.MultiChoiceActivity'])),
        ))
        db.send_create_signal('challenges', ['AnswerMultiChoice'])

        # Adding model 'AnswerMap'
        db.create_table('answers_answermap', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
            ('map', self.gf('gmapsfield.fields.GoogleMapsField')()),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='map_answers', to=orm['challenges.MapChallenge'])),
        ))
        db.send_create_signal('challenges', ['AnswerMap'])

        # Adding model 'AnswerEmpathy'
        db.create_table('answers_answerempathy', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='empathy_answers', to=orm['challenges.EmpathyChallenge'])),
        ))
        db.send_create_signal('challenges', ['AnswerEmpathy'])

        # Adding model 'AnswerOpenEnded'
        db.create_table('answers_answeropenended', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='openended_answers', to=orm['challenges.Challenge'])),
        ))
        db.send_create_signal('challenges', ['AnswerOpenEnded'])


    def backwards(self, orm):
        # Removing unique constraint on 'MultiChoiceActivityTranslation', fields ['language_code', 'master']
        db.delete_unique('player_activities_multichoiceactivity_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'EmpathyChallengeTranslation', fields ['language_code', 'master']
        db.delete_unique('player_activities_playerempathyactivity_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'MapChallengeTranslation', fields ['language_code', 'master']
        db.delete_unique(['player_activities_playermapactivity_translation'], ['language_code', 'master_id'])

        # Removing unique constraint on 'ChallengeTranslation', fields ['language_code', 'master']
        db.delete_unique('player_activities_playeractivity_translation', ['language_code', 'master_id'])

        # Deleting model 'ChallengeType'
        db.delete_table('player_activities_playeractivitytype')

        # Deleting model 'ChallengeTranslation'
        db.delete_table('player_activities_playeractivity_translation')

        # Deleting model 'Challenge'
        db.delete_table('player_activities_playeractivity')

        # Removing M2M table for field attachment on 'Challenge'
        db.delete_table('player_activities_playeractivity_attachment')

        # Deleting model 'MapChallengeTranslation'
        db.delete_table(['player_activities_playermapactivity_translation'])

        # Deleting model 'MapChallenge'
        db.delete_table('player_activities_playermapactivity')

        # Removing M2M table for field attachment on 'MapChallenge'
        db.delete_table('player_activities_playermapactivity_attachment')

        # Deleting model 'EmpathyChallengeTranslation'
        db.delete_table('player_activities_playerempathyactivity_translation')

        # Deleting model 'EmpathyChallenge'
        db.delete_table('player_activities_playerempathyactivity')

        # Removing M2M table for field attachment on 'EmpathyChallenge'
        db.delete_table('player_activities_playerempathyactivity_attachment')

        # Deleting model 'MultiChoiceActivityTranslation'
        db.delete_table('player_activities_multichoiceactivity_translation')

        # Deleting model 'MultiChoiceActivity'
        db.delete_table('player_activities_multichoiceactivity')

        # Deleting model 'Answer'
        db.delete_table('answers_answer')

        # Deleting model 'AnswerSingleResponse'
        db.delete_table('answers_answersingleresponse')

        # Deleting model 'AnswerMultiChoice'
        db.delete_table('answers_answermultichoice')

        # Deleting model 'AnswerMap'
        db.delete_table('answers_answermap')

        # Deleting model 'AnswerEmpathy'
        db.delete_table('answers_answerempathy')

        # Deleting model 'AnswerOpenEnded'
        db.delete_table('answers_answeropenended')


    models = {
        'attachments_v2.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'att_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']", 'null': 'True', 'blank': 'True'}),
            'is_post_game': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_resource_center': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_slideshow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
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
        'challenges.answer': {
            'Meta': {'ordering': "('-createDate',)", 'object_name': 'Answer', 'db_table': "'answers_answer'"},
            'answerUser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['auth.User']"}),
            'createDate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'challenges.answerempathy': {
            'Meta': {'ordering': "('-createDate',)", 'object_name': 'AnswerEmpathy', 'db_table': "'answers_answerempathy'", '_ormbases': ['challenges.Answer']},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'empathy_answers'", 'to': "orm['challenges.EmpathyChallenge']"}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Answer']", 'unique': 'True', 'primary_key': 'True'})
        },
        'challenges.answermap': {
            'Meta': {'ordering': "('-createDate',)", 'object_name': 'AnswerMap', 'db_table': "'answers_answermap'", '_ormbases': ['challenges.Answer']},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'map_answers'", 'to': "orm['challenges.MapChallenge']"}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'map': ('gmapsfield.fields.GoogleMapsField', [], {})
        },
        'challenges.answermultichoice': {
            'Meta': {'object_name': 'AnswerMultiChoice', 'db_table': "'answers_answermultichoice'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'multichoice_answers'", 'to': "orm['challenges.MultiChoiceActivity']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'challenges.answeropenended': {
            'Meta': {'ordering': "('-createDate',)", 'object_name': 'AnswerOpenEnded', 'db_table': "'answers_answeropenended'", '_ormbases': ['challenges.Answer']},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'openended_answers'", 'to': "orm['challenges.Challenge']"}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Answer']", 'unique': 'True', 'primary_key': 'True'})
        },
        'challenges.answersingleresponse': {
            'Meta': {'ordering': "('-createDate',)", 'object_name': 'AnswerSingleResponse', 'db_table': "'answers_answersingleresponse'", '_ormbases': ['challenges.Answer']},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'singleresponse_answers'", 'to': "orm['challenges.Challenge']"}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'selected': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'singleresponse_answers'", 'to': "orm['challenges.MultiChoiceActivity']"})
        },
        'challenges.challenge': {
            'Meta': {'object_name': 'Challenge', 'db_table': "'player_activities_playeractivity'"},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments_v2.Attachment']", 'null': 'True', 'blank': 'True'}),
            'comment_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'createDate': ('django.db.models.fields.DateTimeField', [], {}),
            'creationUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_player_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'challenges_challenge_related'", 'to': "orm['missions.Mission']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenges.ChallengeType']"})
        },
        'challenges.challengetranslation': {
            'Meta': {'ordering': "['name']", 'unique_together': "[('language_code', 'master')]", 'object_name': 'ChallengeTranslation', 'db_table': "'player_activities_playeractivity_translation'"},
            'addInstructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['challenges.Challenge']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'challenges.challengetype': {
            'Meta': {'object_name': 'ChallengeType', 'db_table': "'player_activities_playeractivitytype'"},
            'defaultPoints': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'displayType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'challenges.empathychallenge': {
            'Meta': {'object_name': 'EmpathyChallenge', 'db_table': "'player_activities_playerempathyactivity'"},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments_v2.Attachment']", 'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'createDate': ('django.db.models.fields.DateTimeField', [], {}),
            'creationUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_player_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'challenges_empathychallenge_related'", 'to': "orm['missions.Mission']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenges.ChallengeType']"})
        },
        'challenges.empathychallengetranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'EmpathyChallengeTranslation', 'db_table': "'player_activities_playerempathyactivity_translation'"},
            'addInstructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['challenges.EmpathyChallenge']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'challenges.mapchallenge': {
            'Meta': {'object_name': 'MapChallenge', 'db_table': "'player_activities_playermapactivity'"},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments_v2.Attachment']", 'null': 'True', 'blank': 'True'}),
            'comment_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'createDate': ('django.db.models.fields.DateTimeField', [], {}),
            'creationUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_player_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'maxNumMarkers': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'challenges_mapchallenge_related'", 'to': "orm['missions.Mission']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenges.ChallengeType']"})
        },
        'challenges.mapchallengetranslation': {
            'Meta': {'ordering': "['name']", 'unique_together': "[('language_code', 'master')]", 'object_name': 'MapChallengeTranslation', 'db_table': "['player_activities_playermapactivity_translation']"},
            'addInstructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['challenges.MapChallenge']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'challenges.multichoiceactivity': {
            'Meta': {'object_name': 'MultiChoiceActivity', 'db_table': "'player_activities_multichoiceactivity'"},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer_choices'", 'to': "orm['challenges.Challenge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trivia_correct_answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'challenges.multichoiceactivitytranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'MultiChoiceActivityTranslation', 'db_table': "'player_activities_multichoiceactivity_translation'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['challenges.MultiChoiceActivity']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'comments.comment': {
            'Meta': {'object_name': 'Comment'},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments_v2.Attachment']", 'null': 'True', 'blank': 'True'}),
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
        'instances.city': {
            'Meta': {'object_name': 'City'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50'})
        },
        'instances.instance': {
            'Meta': {'ordering': "('start_date',)", 'object_name': 'Instance'},
            'curators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'days_for_mission': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
            'for_city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'null': 'True', 'to': "orm['instances.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['instances.Language']", 'symmetrical': 'False'}),
            'location': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'instances.language': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'missions.mission': {
            'Meta': {'ordering': "('end_date',)", 'object_name': 'Mission'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'missions'", 'to': "orm['instances.Instance']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'video': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['challenges']