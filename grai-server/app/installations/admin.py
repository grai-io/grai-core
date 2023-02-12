from django.contrib import admin

from connections.models import Run

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

    search_fields = ["id", "owner", "repo"]

    list_filter = (
        "workspace",
        "type",
        "owner",
    )

    fields = ["workspace", "type", "owner", "repo", "installation_id"]
    readonly_fields = ["owner", "repo"]


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


class CommitInline(admin.TabularInline):
    model = Commit
    extra = 0
    fields = ["workspace", "repository", "branch"]
    readonly_fields = ["workspace", "repository", "branch"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PullRequestAdmin(admin.ModelAdmin):
    search_fields = ["id", "reference"]

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

    fields = ["workspace", "repository", "reference"]
    readonly_fields = ["workspace", "repository", "reference"]

    inlines = [
        CommitInline,
    ]


class RunInline(admin.TabularInline):
    model = Run
    extra = 0
    fields = ["status", "metadata", "created_at", "started_at", "finished_at", "user"]
    readonly_fields = ["status", "metadata", "created_at", "started_at", "finished_at", "user"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CommitAdmin(admin.ModelAdmin):
    search_fields = ["id", "reference"]

    list_display = (
        "reference",
        "repository",
        "branch",
        "workspace",
        "created_at",
    )

    list_filter = (
        "workspace",
        "repository",
        "branch",
    )

    inlines = [
        RunInline,
    ]


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(PullRequest, PullRequestAdmin)
admin.site.register(Commit, CommitAdmin)
