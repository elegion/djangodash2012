# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TestCaseStep.response_headers'
        db.alter_column('frunner_testcasestep', 'response_headers', self.gf('jsonfield.fields.JSONField')(null=True))

        # Changing field 'TestCaseStep.end_date'
        db.alter_column('frunner_testcasestep', 'end_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'TestCaseStep.response_body'
        db.alter_column('frunner_testcasestep', 'response_body', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'TestCaseStep.response_code'
        db.alter_column('frunner_testcasestep', 'response_code', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True))

        # Changing field 'TestCaseStep.start_date'
        db.alter_column('frunner_testcasestep', 'start_date', self.gf('django.db.models.fields.DateTimeField')(null=True))
        # Adding field 'TestCase.project'
        db.add_column('frunner_testcase', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='test_runs', to=orm['feditor.TestProject']),
                      keep_default=False)


        # Changing field 'TestCase.end_date'
        db.alter_column('frunner_testcase', 'end_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'TestCase.start_date'
        db.alter_column('frunner_testcase', 'start_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'TestCaseStep.response_headers'
        db.alter_column('frunner_testcasestep', 'response_headers', self.gf('jsonfield.fields.JSONField')())

        # User chose to not deal with backwards NULL issues for 'TestCaseStep.end_date'
        raise RuntimeError("Cannot reverse this migration. 'TestCaseStep.end_date' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'TestCaseStep.response_body'
        raise RuntimeError("Cannot reverse this migration. 'TestCaseStep.response_body' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'TestCaseStep.response_code'
        raise RuntimeError("Cannot reverse this migration. 'TestCaseStep.response_code' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'TestCaseStep.start_date'
        raise RuntimeError("Cannot reverse this migration. 'TestCaseStep.start_date' and its values cannot be restored.")
        # Deleting field 'TestCase.project'
        db.delete_column('frunner_testcase', 'project_id')


        # User chose to not deal with backwards NULL issues for 'TestCase.end_date'
        raise RuntimeError("Cannot reverse this migration. 'TestCase.end_date' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'TestCase.start_date'
        raise RuntimeError("Cannot reverse this migration. 'TestCase.start_date' and its values cannot be restored.")

    models = {
        'fcore.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'})
        },
        'feditor.testproject': {
            'Meta': {'object_name': 'TestProject'},
            'base_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'common_params': ('fortuitus.feditor.dbfields.ParamsField', [], {}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fcore.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'})
        },
        'frunner.params': {
            'Meta': {'object_name': 'Params'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'frunner.testcase': {
            'Meta': {'object_name': 'TestCase'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'test_runs'", 'to': "orm['feditor.TestProject']"}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
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
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'params': ('fortuitus.feditor.dbfields.ParamsField', [], {}),
            'response_body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'response_headers': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'steps'", 'to': "orm['frunner.TestCase']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['frunner']