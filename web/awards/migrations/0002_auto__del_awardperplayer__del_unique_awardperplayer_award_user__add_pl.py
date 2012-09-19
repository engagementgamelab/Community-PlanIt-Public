# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'AwardPerPlayer', fields ['award', 'user']
        db.delete_unique('awards_awardperplayer', ['award_id', 'user_id'])

        # Deleting model 'AwardPerPlayer'
        db.delete_table('awards_awardperplayer')

        # Adding model 'PlayerAward'
        db.create_table('awards_playeraward', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('award', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['awards.Award'])),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('awards', ['PlayerAward'])


    def backwards(self, orm):
        # Adding model 'AwardPerPlayer'
        db.create_table('awards_awardperplayer', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('award', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['awards.Award'])),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('awards', ['AwardPerPlayer'])

        # Adding unique constraint on 'AwardPerPlayer', fields ['award', 'user']
        db.create_unique('awards_awardperplayer', ['award_id', 'user_id'])

        # Deleting model 'PlayerAward'
        db.delete_table('awards_playeraward')


    models = {
        'awards.award': {
            'Meta': {'object_name': 'Award'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'100'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'unique': 'True'})
        },
        'awards.playeraward': {
            'Meta': {'object_name': 'PlayerAward'},
            'award': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['awards.Award']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['awards']