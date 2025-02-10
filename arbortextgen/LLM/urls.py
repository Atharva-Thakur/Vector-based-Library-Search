from django.urls import path

from LLM.views import LLMChat, UpdateTitleView

urlpatterns = [
    path('llm_chat/', LLMChat.as_view(), name='llm_chat'),
    path("update-title/", UpdateTitleView.as_view(), name="update-title"),
]
