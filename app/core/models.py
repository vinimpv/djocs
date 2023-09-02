# Create your models here.
from django.db import models
from simple_history.models import HistoricalRecords
import uuid
from django.contrib.auth.models import User
from pgvector.django import VectorField


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    history = HistoricalRecords(inherit=True)

    class Meta:
        ordering = ["-created_at"]
        abstract = True


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="avatar", blank=True)


class Chat(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


class Message(BaseModel):
    class Type(models.TextChoices):
        LLM_RESPONSE = "LLM_RESPONSE", "LLM Response"
        USER_MESSAGE = "USER_MESSAGE", "User Message"
        MODERATOR_MESSAGE = "MODERATOR_MESSAGE", "Moderator Message"

    type = models.CharField(max_length=255, choices=Type.choices, default=Type.USER_MESSAGE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()


class MessageResponse(BaseModel):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="response")
    response = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="+", null=True, blank=True)


class Knowledge(BaseModel):
    summary = models.TextField()
    content = models.TextField()
    metadata = models.TextField()


class KnowledgeQuestionEmbedding(BaseModel):
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE)
    content = models.TextField()
    embedding = VectorField(dimensions=1536)


# when a question comes in we need to
# -> get the embedding of the question
# -> find similar questions that have association with a knowledge
# -> get the relevant knowledges
# -> send the knowledges to the LLM along with the question
