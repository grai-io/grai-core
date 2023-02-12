from django.contrib import admin

from .models import Branch, Commit, PullRequest, Repository


class RepositoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "owner",
        "repo",
        "installation_id",
        "created_at",
        "workspace",
    )

    search_fields = ["owner", "repo"]

    list_filter = (
        "workspace",
        "type",
        "owner",
    )


class BranchAdmin(admin.ModelAdmin):
    search_fields = ["reference"]

    list_display = (
        "repository",
        "reference",
        "workspace",
        "created_at",
    )

    list_filter = (
        "workspace",
        "repository",
    )


class PullRequestAdmin(admin.ModelAdmin):
    search_fields = ["reference"]

    list_display = (
        "repository",
        "reference",
        "workspace",
        "created_at",
    )

    list_filter = (
        "workspace",
        "repository",
    )


class CommitAdmin(admin.ModelAdmin):
    search_fields = ["reference"]

    list_display = (
        "repository",
        "branch",
        "reference",
        "workspace",
        "created_at",
    )

    list_filter = (
        "workspace",
        "repository",
        "branch",
    )


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(PullRequest, PullRequestAdmin)
admin.site.register(Commit, CommitAdmin)
