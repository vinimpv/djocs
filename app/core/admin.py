# Register your models here.
from django.contrib import admin
from .models import Chat, Message, Knowledge, KnowledgeQuestionEmbedding, MessageResponse, UserProfile

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'modified_at', 'active')
    list_filter = ('author', 'created_at', 'modified_at', 'active')
    search_fields = ('title', 'author', 'created_at', 'modified_at', 'active')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'author', 'created_at', 'modified_at', 'active')
    list_filter = ('chat', 'author', 'created_at', 'modified_at', 'active')
    search_fields = ('chat', 'author', 'created_at', 'modified_at', 'active')

@admin.register(Knowledge)
class KnowledgeAdmin(admin.ModelAdmin):
    list_display = ('summary', 'content', 'created_at', 'modified_at', 'active')
    list_filter = ('created_at', 'modified_at', 'active')
    search_fields = ('summary', 'content', 'created_at', 'modified_at', 'active')

@admin.register(KnowledgeQuestionEmbedding)
class KnowledgeQuestionEmbeddingAdmin(admin.ModelAdmin):
    list_display = ('embedding_model', 'knowledge', 'content', 'embedding', 'created_at', 'modified_at', 'active')
    list_filter = ('embedding_model', 'knowledge', 'created_at', 'modified_at', 'active')
    search_fields = ('embedding_model', 'knowledge', 'content', 'embedding', 'created_at', 'modified_at', 'active')

@admin.register(MessageResponse)
class MessageResponseAdmin(admin.ModelAdmin):
    list_display = ('message', 'response', 'created_at', 'modified_at', 'active')
    list_filter = ('message', 'response', 'created_at', 'modified_at', 'active')
    search_fields = ('message', 'response', 'created_at', 'modified_at', 'active')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    list_filter = ('user', 'image')
    search_fields = ('user', 'image')
