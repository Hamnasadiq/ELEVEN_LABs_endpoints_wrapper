from django.urls import path
# endpoint views..............................
from .views import (
    CreateAgentView, GetAgentView, ListAgentsView,
    UpdateAgentView, DeleteAgentView, DuplicateAgentView,
    GetAgentLinkView, SimulateConversationView, SimulateConversationStreamView,
    ListConversationsView,GetConversationView,DeleteConversationView,GetConversationAudioView,
    CreateConversationFeedbackView,ListToolsView,GetToolView,CreateClientToolView,UpdateClientToolView,
    DeleteToolView,GetToolDependentAgentsView,create_agent_ui,get_agent_ui,list_agents_ui,update_agent_ui,
    delete_agent_ui,get_agent_link_ui,duplicate_agent_ui,simulate_conversation_ui,simulate_conversation_stream_ui,
    list_conversations_ui,get_conversation_ui,delete_conversation_ui,get_conversation_audio_ui,
)
from .views import ( 
    dashboard,agents_page,conversations_page,tools_page,create_feedback_ui,list_tools_ui,
get_tool_ui,create_client_tool_ui,update_client_tool_ui,delete_tool_ui,get_tool_dependent_agents_ui
)



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
   # UI page route
    path('simulate/stream/ui/', simulate_conversation_stream_ui, name='simulate_conversation_stream_ui'),

    # API route with <agent_id>
    path('api/agents/<str:agent_id>/simulate/stream/', SimulateConversationStreamView.as_view(), name='simulate_conversation_stream_api'),
    #conversation
    path("conversations/list-ui/", list_conversations_ui, name="list-conversations-ui"),
    path("conversations/list/", ListConversationsView.as_view(), name="list-conversations-api"),
    path("conversations/get-ui/", get_conversation_ui, name="get-conversation-ui"),
    path("api/agents/conversations/<str:conversation_id>/", GetConversationView.as_view(), name="get-conversation-api"),
    path("conversations/delete-ui/", delete_conversation_ui, name="delete-conversation-ui"),
    path("conversations/<str:conversation_id>/delete/", DeleteConversationView.as_view(), name="delete-conversation-api"),
    path("conversations/audio-ui/", get_conversation_audio_ui, name="get-conversation-audio-ui"),
    path("conversations/<str:conversation_id>/audio/", GetConversationAudioView.as_view(), name="get-conversation-audio-api"),
    path("conversations/<str:conversation_id>/feedback/", CreateConversationFeedbackView.as_view(), name="create-feedback-api"),
    path("conversations/feedback-ui/", create_feedback_ui, name="create-feedback-ui"),
   
    # ✅ 1. UI Routes — STATIC FIRST (DO NOT depend on <tool_id>)
    path("tools/list-ui/", list_tools_ui, name="list-tools-ui"),
    path("tools/get-ui/", get_tool_ui, name="get-tool-ui"),
    path("tools/create-ui/", create_client_tool_ui, name="create-client-tool-ui"),
    path("tools/update-ui/", update_client_tool_ui, name="update-client-tool-ui"),
    path("tools/delete-ui/", delete_tool_ui, name="delete-tool-ui"),
    path("tools/dependent-agents-ui/", get_tool_dependent_agents_ui, name="get-tool-dependent-agents-ui"),

    # ✅ 2. API Routes — SPECIFIC patterns (include action keyword in path)
    path("tools/list/", ListToolsView.as_view(), name="list-tools-api"),
    path("tools/create-client/", CreateClientToolView.as_view(), name="create-client-tool-api"),
    path("tools/<str:tool_id>/update/", UpdateClientToolView.as_view(), name="update-client-tool-api"),
    path("tools/<str:tool_id>/delete/", DeleteToolView.as_view(), name="delete-tool-api"),
    path("tools/<str:tool_id>/dependent-agents/", GetToolDependentAgentsView.as_view(), name="get-tool-dependent-agents-api"),

    # 🚨 3. Wildcard Route — LAST to prevent it from catching specific routes above
    path("tools/<str:tool_id>/", GetToolView.as_view(), name="get-tool-api"),







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
