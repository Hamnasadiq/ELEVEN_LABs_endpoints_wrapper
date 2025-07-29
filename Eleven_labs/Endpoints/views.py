from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elevenlabs import ElevenLabs
from elevenlabs import ConversationalConfig, ElevenLabs  # ✅ fixed name
from elevenlabs import AgentConfig, ConversationSimulationSpecification
from django.http import HttpResponse
import requests
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from elevenlabs.conversational_ai.schemas import SimulatedUserConfig
import traceback
from elevenlabs import (
    ArrayJsonSchemaPropertyInput,
    ToolRequestModel,
    ToolRequestModelToolConfig_Client,
)
import json

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

            # Extracting the first message and language from request body
            first_message = request.data.get("first_message", "Hello")
            language = request.data.get("language", "en")

            client = ElevenLabs(api_key=api_key)

            simulation_spec = ConversationSimulationSpecification(
                simulated_user_config=SimulatedUserConfig(
                    first_message=first_message,
                    language=language,
                )
            )

            response = client.conversational_ai.agents.simulate_conversation(
                agent_id=agent_id,
                simulation_specification=simulation_spec
            )

            print("Simulation response:", response)  # ✅ For debugging

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
                simulated_user_config=AgentConfig(
                    first_message=first_message,
                    language=language,
                )
            )

            # Stream the chunks and collect them
            stream = client.conversational_ai.agents.simulate_conversation_stream(
                agent_id=agent_id,
                simulation_specification=simulation_spec
            )

            collected_output = []
            for chunk in stream:
                collected_output.append(chunk)
                print("Chunk received:", chunk)

            return Response({"streamed_response": collected_output}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#conversation endpoints
class ListConversationsView(APIView):
    def get(self, request):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key in settings."}, status=status.HTTP_400_BAD_REQUEST)

            client = ElevenLabs(api_key=api_key)

            response = client.conversational_ai.conversations.list()

            print("Conversations:", response)  # ✅ Debug

            return Response({"conversations": response}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetConversationView(APIView):
    def get(self, request, conversation_id):
        try:
            api_key = settings.ELEVENLABS_API_KEY
            if not api_key:
                return Response({"error": "Missing API key."}, status=status.HTTP_400_BAD_REQUEST)

            client = ElevenLabs(api_key=api_key)

            conversation = client.conversational_ai.conversations.get(conversation_id=conversation_id)

            print("Conversation:", conversation)  # ✅ For debugging

            return Response({"conversation": conversation}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        

#list tools
class ListToolsView(APIView):
    def get(self, request):
        try:
            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
            tools = client.conversational_ai.tools.list()
            return Response({"tools": tools}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
class GetToolView(APIView):
    def get(self, request, tool_id):
        try:
            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
            tool = client.conversational_ai.tools.get(tool_id=tool_id)
            return Response({"tool": tool}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
ToolRequestModelToolConfig_Client.model_rebuild()

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
class DeleteToolView(APIView):
    def delete(self, request, tool_id):
        try:
            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)

            client.conversational_ai.tools.delete(tool_id=tool_id)

            return Response({"message": f"Tool '{tool_id}' deleted successfully."}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
class GetToolDependentAgentsView(APIView):
    def get(self, request, tool_id):
        try:
            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)

            response = client.conversational_ai.tools.get_dependent_agents(tool_id=tool_id)

            return Response({"result": response}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        










