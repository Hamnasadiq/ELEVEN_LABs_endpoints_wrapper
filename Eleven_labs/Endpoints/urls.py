from django.urls import path
from .views import (
    CreateAgentView, GetAgentView, ListAgentsView,
    UpdateAgentView, DeleteAgentView, DuplicateAgentView,
    GetAgentLinkView, SimulateConversationView, SimulateConversationStreamView,
    ListConversationsView,GetConversationView,DeleteConversationView,GetConversationAudioView,
    CreateConversationFeedbackView,ListToolsView,GetToolView,CreateClientToolView,UpdateClientToolView,
    DeleteToolView,GetToolDependentAgentsView

)   

urlpatterns = [
    path('create/', CreateAgentView.as_view(), name='create-agent'),
    path('list/', ListAgentsView.as_view(), name='list-agents'),

    # 👇 Place conversations FIRST before dynamic <str:agent_id>
    path('tools/list/', ListToolsView.as_view(), name='list-tools'),

    path('conversations/', ListConversationsView.as_view(), name='list-conversations'),
    path('tools/create-client/', CreateClientToolView.as_view(), name='create-client-tool'),
    path('tools/<str:tool_id>/delete/', DeleteToolView.as_view(), name='delete-tool'),
    path('tools/<str:tool_id>/update/', UpdateClientToolView.as_view(), name='update-tool'),
    path('tools/<str:tool_id>/dependent-agents/', GetToolDependentAgentsView.as_view(), name='tool-dependent-agents'),

    path('tools/<str:tool_id>/', GetToolView.as_view(), name='get-tool'),
    path('conversations/<str:conversation_id>/feedback/', CreateConversationFeedbackView.as_view(), name='conversation-feedback'),
    path('conversations/<str:conversation_id>/audio/', GetConversationAudioView.as_view(), name='get-conversation-audio'),
    path('conversations/<str:conversation_id>/delete/', DeleteConversationView.as_view(), name='delete-conversation'),
    path('conversations/<str:conversation_id>/', GetConversationView.as_view(), name='get-conversation'),
    path('<str:agent_id>/', GetAgentView.as_view(), name='get-agent'),
    path('<str:agent_id>/update/', UpdateAgentView.as_view(), name='update-agent'),
    path('<str:agent_id>/delete/', DeleteAgentView.as_view(), name='delete-agent'),
    path('<str:agent_id>/duplicate/', DuplicateAgentView.as_view(), name='duplicate-agent'),
    path('<str:agent_id>/link/', GetAgentLinkView.as_view(), name='get-agent-link'),
    path('<str:agent_id>/simulate/', SimulateConversationView.as_view(), name='simulate-conversation'),
    path('<str:agent_id>/simulate-stream/', SimulateConversationStreamView.as_view(), name='simulate-conversation-stream'),
]
