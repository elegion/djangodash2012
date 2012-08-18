# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TestCaseAssert.operator'
        db.alter_column('feditor_testcaseassert', 'operator', self.gf('django.db.models.fields.CharField')(max_length=256))

    def backwards(self, orm):

        # Changing field 'TestCaseAssert.operator'
        db.alter_column('feditor_testcaseassert', 'operator', self.gf('django.db.models.fields.CharField')(max_length='16'))

    models = {
        'fcore.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'})
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
        'feditor.testcaseassert': {
            'Meta': {'object_name': 'TestCaseAssert'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lhs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'operator': ('django.db.models.fields.CharField', [], {'default': "'Eq'", 'max_length': '256'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'rhs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assertions'", 'to': "orm['feditor.TestCaseStep']"})
        },
        'feditor.testcasestep': {
            'Meta': {'object_name': 'TestCaseStep'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'params': ('fortuitus.feditor.dbfields.ParamsField', [], {'null': 'True', 'blank': 'True'}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'steps'", 'to': "orm['feditor.TestCase']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'feditor.testproject': {
            'Meta': {'object_name': 'TestProject'},
            'base_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'common_params': ('fortuitus.feditor.dbfields.ParamsField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fcore.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'})
        }
    }

    complete_apps = ['feditor']