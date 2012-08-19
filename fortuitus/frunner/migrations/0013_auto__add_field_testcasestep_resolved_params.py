# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TestCaseStep.resolved_params'
        db.add_column('frunner_testcasestep', 'resolved_params',
                      self.gf('fortuitus.feditor.dbfields.ParamsField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TestCaseStep.resolved_params'
        db.delete_column('frunner_testcasestep', 'resolved_params')


    models = {
        'fcore.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'})
        },
        'feditor.testproject': {
            'Meta': {'ordering': "('slug',)", 'object_name': 'TestProject'},
            'base_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'common_params': ('fortuitus.feditor.dbfields.ParamsField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fcore.Company']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'})
        },
        'frunner.testcase': {
            'Meta': {'object_name': 'TestCase'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_options': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'login_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'testrun': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'testcases'", 'to': "orm['frunner.TestRun']"})
        },
        'frunner.testcaseassert': {
            'Meta': {'object_name': 'TestCaseAssert'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lhs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'operator': ('django.db.models.fields.CharField', [], {'default': "'eq'", 'max_length': '256'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'rhs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assertions'", 'to': "orm['frunner.TestCaseStep']"})
        },
        'frunner.testcasestep': {
            'Meta': {'object_name': 'TestCaseStep'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'exception': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'params': ('fortuitus.feditor.dbfields.ParamsField', [], {'null': 'True', 'blank': 'True'}),
            'resolved_params': ('fortuitus.feditor.dbfields.ParamsField', [], {'null': 'True', 'blank': 'True'}),
            'response_body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'response_headers': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'steps'", 'to': "orm['frunner.TestCase']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'frunner.testrun': {
            'Meta': {'object_name': 'TestRun'},
            'base_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'common_params': ('fortuitus.feditor.dbfields.ParamsField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'test_runs'", 'to': "orm['feditor.TestProject']"}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['frunner']