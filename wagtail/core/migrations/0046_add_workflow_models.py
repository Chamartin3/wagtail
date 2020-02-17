# Generated by Django 3.0.3 on 2020-02-17 10:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0011_update_proxy_permissions'),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('active', models.BooleanField(default=True, help_text='Active tasks can be added to workflows. Deactivating a task does not remove it from existing workflows.', verbose_name='active')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wagtail_tasks', to='contenttypes.ContentType', verbose_name='content type')),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
            },
        ),
        migrations.CreateModel(
            name='TaskState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('in_progress', 'In progress'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('skipped', 'Skipped'), ('cancelled', 'Cancelled')], default='in_progress', max_length=50, verbose_name='status')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='started at')),
                ('finished_at', models.DateTimeField(blank=True, null=True, verbose_name='finished at')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wagtail_task_states', to='contenttypes.ContentType', verbose_name='content type')),
                ('page_revision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_states', to='wagtailcore.PageRevision', verbose_name='page revision')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_states', to='wagtailcore.Task', verbose_name='task')),
            ],
            options={
                'verbose_name': 'Task state',
                'verbose_name_plural': 'Task states',
            },
            bases=(wagtail.core.models.MultiTableCopyMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('active', models.BooleanField(default=True, help_text='Active workflows can be added to pages. Deactivating a workflow does not remove it from existing pages.', verbose_name='active')),
            ],
            options={
                'verbose_name': 'workflow',
                'verbose_name_plural': 'workflows',
            },
        ),
        migrations.CreateModel(
            name='GroupApprovalTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Task')),
            ],
            options={
                'verbose_name': 'Group approval task',
                'verbose_name_plural': 'Group approval tasks',
            },
            bases=('wagtailcore.task',),
        ),
        migrations.CreateModel(
            name='WorkflowState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('in_progress', 'In progress'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], default='in_progress', max_length=50, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('current_task_state', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailcore.TaskState', verbose_name='current task state')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_states', to='wagtailcore.Page', verbose_name='page')),
                ('requested_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requested_workflows', to=settings.AUTH_USER_MODEL, verbose_name='requested by')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_states', to='wagtailcore.Workflow', verbose_name='workflow')),
            ],
            options={
                'verbose_name': 'Workflow state',
                'verbose_name_plural': 'Workflow states',
            },
        ),
        migrations.CreateModel(
            name='WorkflowPage',
            fields=[
                ('page', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='wagtailcore.Page', verbose_name='page')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_pages', to='wagtailcore.Workflow', verbose_name='workflow')),
            ],
            options={
                'verbose_name': 'workflow page',
                'verbose_name_plural': 'workflow pages',
            },
        ),
        migrations.AddField(
            model_name='taskstate',
            name='workflow_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_states', to='wagtailcore.WorkflowState', verbose_name='workflow state'),
        ),
        migrations.CreateModel(
            name='WorkflowTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('task', models.ForeignKey(limit_choices_to={'active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='workflow_tasks', to='wagtailcore.Task', verbose_name='task')),
                ('workflow', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_tasks', to='wagtailcore.Workflow', verbose_name='workflow_tasks')),
            ],
            options={
                'verbose_name': 'workflow task order',
                'verbose_name_plural': 'workflow task orders',
                'unique_together': {('workflow', 'sort_order'), ('workflow', 'task')},
            },
        ),
        migrations.AddConstraint(
            model_name='workflowstate',
            constraint=models.UniqueConstraint(condition=models.Q(status='in_progress'), fields=('page',), name='unique_in_progress_workflow'),
        ),
        migrations.AddField(
            model_name='groupapprovaltask',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', verbose_name='groups'),
        ),
    ]
