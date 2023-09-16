from typing import Any
from django.conf import settings
from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.http import HttpRequest
from asgiref.sync import async_to_sync
from django.http.request import HttpRequest

from simple_history.admin import SimpleHistoryAdmin

from app.core.services.knowledges import get_knowledge_embedding
from app.core.services.tokens import num_tokens_from_string_ada_2
from .models import Chat, Message, Knowledge, MessageResponse, UserProfile, Category

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0

    ordering = ("created_at",)
    exclude = ("embedding",)

@admin.register(Chat)
class ChatAdmin(SimpleHistoryAdmin):
    list_display = ("title", "author", "created_at", "modified_at", "active")
    list_filter = ("author", "created_at", "modified_at", "active")
    search_fields = ("title", "author", "created_at", "modified_at", "active")
    raw_id_fields = ("author", "category")

    inlines = [
        MessageInline,
    ]


@admin.register(Message)
class MessageAdmin(SimpleHistoryAdmin):
    summernote_fields = ("content",)
    list_display = ("chat", "author", "created_at", "modified_at", "active")
    list_filter = ("chat", "author", "created_at", "modified_at", "active")
    search_fields = ("chat", "author", "created_at", "modified_at", "active")


class KnowledgeAdminForm(ModelForm):
    def clean(self) -> None:
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        num_tokens = num_tokens_from_string_ada_2(content)
        if num_tokens > settings.DJOCS_MAX_KNOWLEDGE_TOKENS:
            raise ValidationError(
                f"Knowledge content is too long (max {settings.MAX_KNOWLEDGE_TOKENS} tokens) "
                "(current: {num_tokens} tokens)"
            )

        return cleaned_data


@admin.register(Knowledge)
class KnowledgeAdmin(SimpleHistoryAdmin):
    form = KnowledgeAdminForm
    list_display = ("__str__", "created_at", "modified_at", "active")
    list_filter = ("created_at", "modified_at", "active")
    search_fields = ("created_at", "modified_at", "active")

    def save_model(self, request: HttpRequest, obj: Knowledge, form: Any, change: bool) -> None:
        embedding = async_to_sync(get_knowledge_embedding)(obj)
        obj.embedding = embedding
        return super().save_model(request, obj, form, change)


@admin.register(MessageResponse)
class MessageResponseAdmin(SimpleHistoryAdmin):
    list_display = ("response", "created_at", "modified_at", "active")
    list_filter = ("response", "created_at", "modified_at", "active")
    search_fields = ("response", "created_at", "modified_at", "active")


@admin.register(UserProfile)
class UserProfileAdmin(SimpleHistoryAdmin):
    list_display = ("user", "image")
    list_filter = ("user", "image")
    search_fields = ("user", "image")


@admin.register(Category)
class CategoryAdmin(SimpleHistoryAdmin):
    list_display = ("name", "created_at", "modified_at", "active")
    list_filter = ("name", "created_at", "modified_at", "active")
    search_fields = ("name", "created_at", "modified_at", "active")
