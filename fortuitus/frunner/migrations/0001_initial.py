# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestCase'
        db.create_table('frunner_testcase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=None)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal('frunner', ['TestCase'])

        # Adding model 'Params'
        db.create_table('frunner_params', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('frunner', ['Params'])

        # Adding model 'TestCaseStep'
        db.create_table('frunner_testcasestep', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('params', self.gf('fortuitus.feditor.dbfields.ParamsField')()),
            ('testcase', self.gf('django.db.models.fields.related.ForeignKey')(related_name='steps', to=orm['frunner.TestCase'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('response_code', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('response_headers', self.gf('jsonfield.fields.JSONField')(default={})),
            ('response_body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('frunner', ['TestCaseStep'])

        # Adding model 'TestCaseAssert'
        db.create_table('frunner_testcaseassert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('expression', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('step', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assertions', to=orm['frunner.TestCaseStep'])),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal('frunner', ['TestCaseAssert'])


    def backwards(self, orm):
        # Deleting model 'TestCase'
        db.delete_table('frunner_testcase')

        # Deleting model 'Params'
        db.delete_table('frunner_params')

        # Deleting model 'TestCaseStep'
        db.delete_table('frunner_testcasestep')

        # Deleting model 'TestCaseAssert'
        db.delete_table('frunner_testcaseassert')


    models = {
        'frunner.params': {
            'Meta': {'object_name': 'Params'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'frunner.testcase': {
            'Meta': {'object_name': 'TestCase'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'frunner.testcaseassert': {
            'Meta': {'object_name': 'TestCaseAssert'},
            'expression': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assertions'", 'to': "orm['frunner.TestCaseStep']"})
        },
        'frunner.testcasestep': {
            'Meta': {'object_name': 'TestCaseStep'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'params': ('fortuitus.feditor.dbfields.ParamsField', [], {}),
            'response_body': ('django.db.models.fields.TextField', [], {}),
            'response_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'response_headers': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'steps'", 'to': "orm['frunner.TestCase']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['frunner']