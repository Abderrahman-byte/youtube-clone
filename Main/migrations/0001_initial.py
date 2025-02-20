# Generated by Django 3.0.7 on 2020-07-02 15:35

import Main.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('content', models.TextField(max_length=1500)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.TextField(default=Main.utils.generateId, editable=False, max_length=11, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=1500, null=True)),
                ('duration', models.IntegerField(default=0)),
                ('allow_comments', models.BooleanField(default=True)),
                ('views', models.IntegerField(default=0)),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('video_url', models.CharField(max_length=500)),
                ('thumbnail_url', models.CharField(max_length=500)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='VideoImpression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Video')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify', models.BooleanField(default=False)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.TextField(default=Main.utils.generetePlaylistId, editable=False, max_length=35, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=1500, null=True)),
                ('is_public', models.BooleanField(default=True)),
                ('views', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('videos', models.ManyToManyField(to='Main.Video')),
            ],
        ),
        migrations.AddConstraint(
            model_name='contenttype',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_content_name'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Video'),
        ),
        migrations.AddConstraint(
            model_name='videoimpression',
            constraint=models.UniqueConstraint(fields=('video', 'user'), name='one_impression_foreach_user_on_a_video'),
        ),
        migrations.AddConstraint(
            model_name='video',
            constraint=models.UniqueConstraint(fields=('channel', 'title'), name='unique_videos_per_channel'),
        ),
        migrations.AddConstraint(
            model_name='video',
            constraint=models.UniqueConstraint(fields=('video_url',), name='unique_videos_url'),
        ),
        migrations.AddConstraint(
            model_name='video',
            constraint=models.UniqueConstraint(fields=('thumbnail_url',), name='unique_thumbnail_url'),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('channel', 'user'), name='unique_subscription'),
        ),
        migrations.AddConstraint(
            model_name='playlist',
            constraint=models.UniqueConstraint(fields=('creator', 'title'), name='unique_playlist_per_user'),
        ),
    ]
