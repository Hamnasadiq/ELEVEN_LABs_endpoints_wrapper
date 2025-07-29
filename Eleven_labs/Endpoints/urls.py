from django.urls import path
# endpoint views..............................
from .views import (
    CreateAgentView, GetAgentView, ListAgentsView,
    UpdateAgentView, DeleteAgentView, DuplicateAgentView,
    GetAgentLinkView, SimulateConversationView, SimulateConversationStreamView,
    ListConversationsView,GetConversationView,DeleteConversationView,GetConversationAudioView,
    CreateConversationFeedbackView,ListToolsView,GetToolView,CreateClientToolView,UpdateClientToolView,
    DeleteToolView,GetToolDependentAgentsView,create_agent_ui,get_agent_ui,list_agents_ui,update_agent_ui,
    delete_agent_ui,get_agent_link_ui,duplicate_agent_ui,simulate_conversation_ui
)
from .views import dashboard,agents_page,conversations_page,tools_page



urlpatterns = [

    path('dashboard/', dashboard, name='dashboard'),
    path('agents/', agents_page, name='agents-page'),
    path('conversations/', conversations_page, name='conversations-page'),
    path('tools/', tools_page, name='tools-page'),



    #
    path("agents/create-ui/", create_agent_ui, name="create-agent-ui"),
    path("agents/get-ui/", get_agent_ui, name="get-agent-ui"),
    path("agents/list-ui/", list_agents_ui, name="list-agents-ui"),
    path("agents/update-ui/", update_agent_ui, name="update-agent-ui"),
    path("api/agents/update/<str:agent_id>/", UpdateAgentView.as_view(), name="update-agent-api"),
    path("agents/delete-ui/", delete_agent_ui, name="delete-agent-ui"),
    path("api/agents/delete/<str:agent_id>/", DeleteAgentView.as_view(), name="delete-agent-api"),
    path("api/agents/link/<str:agent_id>/", GetAgentLinkView.as_view(), name="get-agent-link"),
    path("agents/link-ui/", get_agent_link_ui, name="get-agent-link-ui"),
    path('agents/duplicate-ui/', duplicate_agent_ui, name='duplicate_agent_ui'),
    path('api/agents/<str:agent_id>/duplicate/', DuplicateAgentView.as_view(), name='duplicate_agent'),
    path("agents/simulate-ui/", simulate_conversation_ui, name="simulate_agent_ui"),
    path("api/agents/<str:agent_id>/simulate/", SimulateConversationView.as_view(), name="simulate_agent"),




    # API_endpoints urls
    path('create/', CreateAgentView.as_view(), name='create-agent'),
    path('list/', ListAgentsView.as_view(), name='list-agents'),
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
