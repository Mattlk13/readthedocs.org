from rest_framework import serializers

from readthedocs.builds.models import Build, BuildCommandResult, Version
from readthedocs.projects.models import Project
from readthedocs.oauth.models import (GithubOrganization, GithubProject,
                                      BitbucketTeam, BitbucketProject)


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id',
            'name', 'slug', 'description', 'language',
            'repo', 'repo_type',
            'default_version', 'default_branch',
            'documentation_type',
            'users',
        )


class VersionSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    downloads = serializers.DictField(source='get_downloads', read_only=True)

    class Meta:
        model = Version
        fields = (
            'id',
            'project', 'slug',
            'identifier', 'verbose_name',
            'active', 'built',
            'downloads',
        )


class BuildCommandSerializer(serializers.ModelSerializer):
    run_time = serializers.ReadOnlyField()

    class Meta:
        model = BuildCommandResult


class BuildSerializer(serializers.ModelSerializer):
    """Readonly version of the build serializer, used for user facing display"""

    commands = BuildCommandSerializer(many=True, read_only=True)
    state_display = serializers.ReadOnlyField(source='get_state_display')

    class Meta:
        model = Build
        exclude = ('builder',)


class BuildSerializerFull(BuildSerializer):
    """Writeable Build instance serializer, for admin access by builders"""

    class Meta:
        model = Build


class SearchIndexSerializer(serializers.Serializer):
    q = serializers.CharField(max_length=500)
    project = serializers.CharField(max_length=500, required=False)
    version = serializers.CharField(max_length=500, required=False)
    page = serializers.CharField(max_length=500, required=False)


class GithubOrganizationSerializer(serializers.ModelSerializer):

    avatar_url = serializers.ReadOnlyField()

    class Meta:
        model = GithubOrganization
        exclude = ('json', 'email', 'users')


class GithubProjectSerializer(serializers.ModelSerializer):

    """Github project serializer"""

    private = serializers.ReadOnlyField(source='is_private')
    owner = serializers.ReadOnlyField()
    organization = GithubOrganizationSerializer()

    class Meta:
        model = GithubProject
        exclude = ('json', 'users')


class BitbucketTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = BitbucketTeam
        exclude = ('json',)


class BitbucketProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = BitbucketProject
        exclude = ('json',)
