# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestProject'
        db.create_table('feditor_testproject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fcore.Company'])),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=None)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('base_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('feditor', ['TestProject'])

        # Adding model 'Params'
        db.create_table('feditor_params', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('feditor', ['Params'])

        # Adding model 'TestCase'
        db.create_table('feditor_testcase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feditor.TestProject'])),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=None)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('feditor', ['TestCase'])

        # Adding model 'TestCaseStep'
        db.create_table('feditor_testcasestep', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('feditor', ['TestCaseStep'])


    def backwards(self, orm):
        # Deleting model 'TestProject'
        db.delete_table('feditor_testproject')

        # Deleting model 'Params'
        db.delete_table('feditor_params')

        # Deleting model 'TestCase'
        db.delete_table('feditor_testcase')

        # Deleting model 'TestCaseStep'
        db.delete_table('feditor_testcasestep')


    models = {
        'fcore.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'})
        },
        'feditor.params': {
            'Meta': {'object_name': 'Params'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'feditor.testcase': {
            'Meta': {'object_name': 'TestCase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feditor.TestProject']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'})
        },
        'feditor.testcasestep': {
            'Meta': {'object_name': 'TestCaseStep'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'feditor.testproject': {
            'Meta': {'object_name': 'TestProject'},
            'base_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fcore.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'})
        }
    }

    complete_apps = ['feditor']