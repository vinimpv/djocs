# Create your models here.
from django.db import models
import markdown
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

    def __str__(self):
        return f"{self.user.username} Profile"


class Model(BaseModel):
    name = models.CharField(max_length=255)
    max_token_length = models.IntegerField()


class Category(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"Category: {self.name}"


class Chat(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, blank=True)
    is_template = models.BooleanField(default=False)

    def __str__(self):
        return f"Chat: {self.title[:50]}..."


class Response(BaseModel):
    content = models.TextField()
    metadata = models.TextField()

    embedding = VectorField(dimensions=1536, null=True, blank=True)

    def __str__(self):
        return f"Response: {self.content[:50]}..."


class Message(BaseModel):
    class Type(models.TextChoices):
        LLM_RESPONSE = "LLM_RESPONSE", "LLM Response"
        USER_MESSAGE = "USER_MESSAGE", "User Message"
        MODERATOR_MESSAGE = "MODERATOR_MESSAGE", "Moderator Message"

    type = models.CharField(max_length=255, choices=Type.choices, default=Type.USER_MESSAGE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    embedding = VectorField(dimensions=1536, null=True, blank=True, default=None)

    def __str__(self) -> str:
        return f"Message: {self.content[:50]}..."

    def rendered(self) -> str:
        return markdown.markdown(self.content, extensions=["fenced_code"])


class MessageResponse(BaseModel):
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name="response_association")
    response = models.OneToOneField(
        Message, on_delete=models.CASCADE, related_name="message_association", null=True, blank=True
    )

    def __str__(self) -> str:
        return f"MessageResponse: {self.message.content[:50]}..."


class Knowledge(BaseModel):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    embedding = VectorField(dimensions=1536, null=True, blank=True, default=None)

    def __str__(self) -> str:
        return f"Knowledge: {self.content[:50]}..."
