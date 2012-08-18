# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Params'
        db.delete_table('feditor_params')

        # Adding model 'TestCaseAssert'
        db.create_table('feditor_testcaseassert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('testcase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feditor.TestCase'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('expression', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('feditor', ['TestCaseAssert'])

        # Adding field 'TestCaseStep.testcase'
        db.add_column('feditor_testcasestep', 'testcase',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['feditor.TestCase']),
                      keep_default=False)

        # Adding field 'TestCaseStep.order'
        db.add_column('feditor_testcasestep', 'order',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'TestCaseStep.url'
        db.add_column('feditor_testcasestep', 'url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'TestCaseStep.method'
        db.add_column('feditor_testcasestep', 'method',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TestCaseStep.params'
        db.add_column('feditor_testcasestep', 'params',
                      self.gf('fortuitus.feditor.dbfields.ParamsField')(default=''),
                      keep_default=False)

        # Adding field 'TestProject.common_params'
        db.add_column('feditor_testproject', 'common_params',
                      self.gf('fortuitus.feditor.dbfields.ParamsField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Params'
        db.create_table('feditor_params', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('feditor', ['Params'])

        # Deleting model 'TestCaseAssert'
        db.delete_table('feditor_testcaseassert')

        # Deleting field 'TestCaseStep.testcase'
        db.delete_column('feditor_testcasestep', 'testcase_id')

        # Deleting field 'TestCaseStep.order'
        db.delete_column('feditor_testcasestep', 'order')

        # Deleting field 'TestCaseStep.url'
        db.delete_column('feditor_testcasestep', 'url')

        # Deleting field 'TestCaseStep.method'
        db.delete_column('feditor_testcasestep', 'method')

        # Deleting field 'TestCaseStep.params'
        db.delete_column('feditor_testcasestep', 'params')

        # Deleting field 'TestProject.common_params'
        db.delete_column('feditor_testproject', 'common_params')


    models = {
        'fcore.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'})
        },
        'feditor.testcase': {
            'Meta': {'object_name': 'TestCase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feditor.TestProject']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'})
        },
        'feditor.testcaseassert': {
            'Meta': {'object_name': 'TestCaseAssert'},
            'expression': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feditor.TestCase']"})
        },
        'feditor.testcasestep': {
            'Meta': {'object_name': 'TestCaseStep'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'params': ('fortuitus.feditor.dbfields.ParamsField', [], {}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feditor.TestCase']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'feditor.testproject': {
            'Meta': {'object_name': 'TestProject'},
            'base_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'common_params': ('fortuitus.feditor.dbfields.ParamsField', [], {}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fcore.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'})
        }
    }

    complete_apps = ['feditor']