from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elevenlabs import ElevenLabs
from elevenlabs import ConversationalConfig, ElevenLabs  # ✅ fixed name
from elevenlabs import AgentConfig, ConversationSimulationSpecification
from django.http import HttpResponse,JsonResponse
import requests
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import traceback
from elevenlabs import (
    ArrayJsonSchemaPropertyInput,
    ToolRequestModel,
    ToolRequestModelToolConfig_Client,
)
import json

# ✅ Forward reference fix (no new import needed)
ToolRequestModelToolConfig_Client.model_rebuild()

# dashboard

def dashboard(request):
    return render(request, 'Endpoints/dashboard.html')

def agents_page(request):
    return render(request, 'Endpoints/agents.html')

def conversations_page(request):
    return render(request, 'Endpoints/conversations.html')

def tools_page(request):
    return render(request, 'Endpoints/tools.html')

#....................................................................................................................
class CreateAgentView(APIView):

    def post(self, request):
        try:
            agent_name = request.data.get("agent_name")
            

            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key in settings."}, status=400)

            client = ElevenLabs(api_key=api_key)

            response = client.conversational_ai.agents.create(
                conversation_config=ConversationalConfig(),  # ✅ now correct
                name=agent_name,
            )
            print(response.agent_id)

            print("Agent created successfully:", response)  
            return Response({"result": response.agent_id}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


@login_required
def create_agent_ui(request):
    return render(request, 'endpoints/create_agent.html')
class GetAgentView(APIView):
    def get(self, request, agent_id):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key in settings."}, status=400)

            client = ElevenLabs(api_key=api_key)

            response = client.conversational_ai.agents.get(agent_id=agent_id)

            print("Fetched agent successfully:", response)  # ✅ Print for debugging

            return Response({"result": response}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

@login_required
def get_agent_ui(request):
    return render(request, 'endpoints/get_agent.html')



class ListAgentsView(APIView):
    def get(self, request):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key in settings."}, status=400)

            client = ElevenLabs(api_key=api_key)
            response = client.conversational_ai.agents.list()

            agents_data = [
                {
                    "agent_id": agent.agent_id,
                    "name": agent.name
                }
                for agent in response.agents
            ]

            return Response({"result": agents_data}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


@login_required
def list_agents_ui(request):
    return render(request, 'endpoints/list_agents.html')


class UpdateAgentView(APIView):
    def patch(self, request, agent_id):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key in settings."}, status=400)

            client = ElevenLabs(api_key=api_key)

            name = request.data.get("name")

            response = client.conversational_ai.agents.update(
                agent_id=agent_id,
                name=name,
            )

            return Response({"result": {
                "agent_id": response.agent_id,
                "name": response.name
            }}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
@login_required
def update_agent_ui(request):
    return render(request, 'endpoints/update_agent.html')

        

class DeleteAgentView(APIView):
    def delete(self, request, agent_id):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key in settings."}, status=status.HTTP_400_BAD_REQUEST)

            client = ElevenLabs(api_key=api_key)

            response = client.conversational_ai.agents.delete(agent_id=agent_id)

            print("Agent deleted:", response)  # ✅ Debug print

            return Response({"message": "Agent deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@login_required
def delete_agent_ui(request):
    return render(request, 'endpoints/delete_agent.html')




class GetAgentLinkView(APIView):
    def get(self, request, agent_id):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key in settings."}, status=status.HTTP_400_BAD_REQUEST)

            client = ElevenLabs(api_key=api_key)

            response = client.conversational_ai.agents.link.get(agent_id=agent_id)

            print("Agent link fetched:", response)  # ✅ Debug print

            return Response({"link": str(response)}, status=status.HTTP_200_OK)  # Ensure it's JSON-serializable

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@login_required   
def get_agent_link_ui(request):
    return render(request, 'endpoints/get_agent_link.html')

class DuplicateAgentView(APIView):
    def post(self, request, agent_id):
        try:
            # Simulated duplication logic
            duplicated_agent = {
                "id": "new_" + agent_id,
                "original_agent": agent_id,
                "message": "Agent duplicated successfully."
            }
            return Response(duplicated_agent, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@login_required
def duplicate_agent_ui(request):
    return render(request, 'endpoints/duplicate_agent.html')





class SimulateConversationView(APIView):
    def post(self, request, agent_id):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key in settings."}, status=status.HTTP_400_BAD_REQUEST)

            # Get data from request
            first_message = request.data.get("first_message", "Hello")
            language = request.data.get("language", "en")

            # Create client
            client = ElevenLabs(api_key=api_key)

            # Build request
            simulation_spec = ConversationSimulationSpecification(
                simulated_user_config={
                    "first_message": first_message,
                    "language": language,
                }
            )

            # Send request to ElevenLabs
            response = client.conversational_ai.agents.simulate_conversation(
                agent_id=agent_id,
                simulation_specification=simulation_spec
            )

            print("Simulation response:", response)

            return Response({"result": response}, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
def simulate_conversation_ui(request):
    return render(request, 'endpoints/simulate_conversation.html')



class SimulateConversationStreamView(APIView):
    def post(self, request, agent_id):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key in settings."}, status=status.HTTP_400_BAD_REQUEST)

            first_message = request.data.get("first_message", "Hello")
            language = request.data.get("language", "en")

            client = ElevenLabs(api_key=api_key)

            simulation_spec = ConversationSimulationSpecification(
                simulated_user_config={
                    "first_message": first_message,
                    "language": language
                }
            )

            print("SIMULATION SPEC:", simulation_spec.dict())
            print("AGENT ID:", agent_id)

            stream = client.conversational_ai.agents.simulate_conversation_stream(
                agent_id=agent_id,
                simulation_specification=simulation_spec
            )

            if stream is None:
                return Response({"error": "Stream is None. Possible invalid agent_id or internal server error."}, status=502)

            collected_output = []
            for chunk in stream:
                collected_output.append(chunk)
                print("Chunk:", chunk)

            return Response({"streamed_response": collected_output}, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@login_required
def simulate_conversation_stream_ui(request):
    return render(request, 'endpoints/simulate_conversation_stream.html')


#conversation endpoints


class ListConversationsView(APIView):
    def get(self, request):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key."}, status=status.HTTP_400_BAD_REQUEST)

            client = ElevenLabs(api_key=api_key)
            response = client.conversational_ai.conversations.list()

            # Safely access the expected fields
            conversations_data = []
            for convo in response.conversations:
                conversations_data.append({
                    "agent_id": convo.agent_id,
                    "conversation_id": convo.conversation_id,
                    "start_time_unix_secs": convo.start_time_unix_secs,
                    "call_duration_secs": convo.call_duration_secs,
                    "message_count": convo.message_count,
                    "status": convo.status,
                    "call_successful": convo.call_successful,
                    "agent_name": convo.agent_name,
                    "transcript_summary": convo.transcript_summary,
                    "call_summary_title": convo.call_summary_title,
                })

            return Response({"conversations": conversations_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
def list_conversations_ui(request):
    return render(request, 'endpoints/list_conversations.html')

class GetConversationView(APIView):
    def get(self, request, conversation_id):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key."}, status=status.HTTP_400_BAD_REQUEST)

            client = ElevenLabs(api_key=api_key)
            conversation = client.conversational_ai.conversations.get(conversation_id=conversation_id)

            if hasattr(conversation, "model_dump"):
                data = conversation.model_dump()
            else:
                data = conversation  # fallback

            return Response({"conversation": data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@login_required
def get_conversation_ui(request):
    return render(request, 'endpoints/get_conversation.html')

class DeleteConversationView(APIView):
    def delete(self, request, conversation_id):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key."}, status=status.HTTP_400_BAD_REQUEST)

            client = ElevenLabs(api_key=api_key)

            response = client.conversational_ai.conversations.delete(conversation_id=conversation_id)

            print("Conversation deleted:", response)  # ✅ For debug

            return Response({"message": "Conversation deleted successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@login_required
def delete_conversation_ui(request):
    return render(request, 'endpoints/delete_conversation.html')


class GetConversationAudioView(APIView):
    def get(self, request, conversation_id):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key."}, status=status.HTTP_400_BAD_REQUEST)

            url = f"https://api.elevenlabs.io/v1/convai/conversations/{conversation_id}/audio"
            headers = {
                "xi-api-key": api_key
            }

            audio_response = requests.get(url, headers=headers)

            if audio_response.status_code == 200:
                return HttpResponse(audio_response.content, content_type="audio/mpeg")
            else:
                return Response({
                    "error": "Failed to fetch audio",
                    "details": audio_response.json()
                }, status=audio_response.status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@login_required
def get_conversation_audio_ui(request):
    return render(request, 'endpoints/get_conversation_audio.html')



class CreateConversationFeedbackView(APIView):
    def post(self, request, conversation_id):
        try:
            feedback = request.data.get("feedback")
            if feedback not in ["like", "dislike"]:
                return Response({"error": "Feedback must be either 'like' or 'dislike'."}, status=400)

            api_key = settings.ELEVENLABS_API_KEY
            client = ElevenLabs(api_key=api_key)

            result = client.conversational_ai.conversations.feedback.create(
                conversation_id=conversation_id,
                feedback=feedback
            )

            return Response({"message": "Feedback submitted successfully.", "result": result}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

@login_required
def create_feedback_ui(request):
    return render(request, 'endpoints/create_feedback.html')



#list tools


class ListToolsView(APIView):
    def get(self, request):
        try:
            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
            tools_response = client.conversational_ai.tools.list()

            tools_data = []
            for tool in tools_response.tools:
                tools_data.append({
                    "id": tool.id,
                    "name": tool.tool_config.name,
                    "description": tool.tool_config.description,
                })

            return Response({"tools": tools_data}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ UI page
@login_required
def list_tools_ui(request):
    return render(request, 'endpoints/list_tools.html')



class GetToolView(APIView):
    def get(self, request, tool_id):
        try:
            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
            tool = client.conversational_ai.tools.get(tool_id=tool_id)

            tool_data = {
                "tool_id": getattr(tool, "tool_id", "N/A"),
                "name": getattr(tool, "name", "N/A"),
                "description": getattr(tool, "description", "N/A"),
                "expects_response": getattr(tool, "expects_response", False),
            }

            return Response({"tool": tool_data}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
# UI view
@login_required
def get_tool_ui(request):
    return render(request, 'endpoints/get_tool.html')




class CreateClientToolView(APIView):
    def post(self, request):
        try:
            name = request.data.get("name")
            description = request.data.get("description")
            expects_response = request.data.get("expects_response", False)

            if not name or not description:
                return Response({"error": "Missing required fields: name and description."}, status=400)

            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)

            tool_response = client.conversational_ai.tools.create(
                request=ToolRequestModel(
                    tool_config=ToolRequestModelToolConfig_Client(
                        name=name,
                        description=description,
                        expects_response=expects_response,
                    )
                )
            )

            return Response({"result": tool_response}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        
@login_required
def create_client_tool_ui(request):
    return render(request, 'endpoints/create_client_tool.html')
        
class UpdateClientToolView(APIView):
    def put(self, request, tool_id):
        try:
            name = request.data.get("name")
            description = request.data.get("description")
            expects_response = request.data.get("expects_response", False)

            if not name or not description:
                return Response({"error": "Missing 'name' or 'description'."}, status=400)

            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)

            updated_tool = client.conversational_ai.tools.update(
                tool_id=tool_id,
                request=ToolRequestModel(
                    tool_config=ToolRequestModelToolConfig_Client(
                        name=name,
                        description=description,
                        expects_response=expects_response,
                    )
                )
            )

            return Response({"result": updated_tool}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
@login_required
def update_client_tool_ui(request):
    return render(request, 'endpoints/update_client_tool.html')



class DeleteToolView(APIView):
    def delete(self, request, tool_id):
        try:
            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)

            client.conversational_ai.tools.delete(tool_id=tool_id)

            return Response({"message": f"Tool '{tool_id}' deleted successfully."}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
@login_required
def delete_tool_ui(request):
    return render(request, 'endpoints/delete_tool.html')

class GetToolDependentAgentsView(APIView):
    def get(self, request, tool_id):
        try:
            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)

            response = client.conversational_ai.tools.get_dependent_agents(tool_id=tool_id)

            return Response({"result": response}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

@login_required
def get_tool_dependent_agents_ui(request):
    return render(request, 'endpoints/get_tool_dependent_agents.html')









