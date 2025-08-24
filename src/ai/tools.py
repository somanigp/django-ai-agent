from documents.models import Document  # Django Document Model/DB
from langchain_core.tools import tool  # Tool is a function that can be called by the LLM/Agent.
from langchain_core.runnables import RunnableConfig  # To pass extra config to the tool function.

@tool
def list_documents(config: RunnableConfig):
    """List all active documents for a User."""
    print(config) # {'tags': [], 'metadata': {'user_id': 4}, 'callbacks': None, 'recursion_limit': 25, 'configurable': {'user_id': 4}}
    user_id = config.get("configurable").get("user_id")  # Get the user_id from the metadata.
    if not user_id:
        raise Exception("User ID not found.")
    qs = Document.objects.filter(owner_id=user_id, active=True) # We don't need User object. Owner is a foreign key so only owner_id will do.
    response_data = []
    # Serialize the queryset, meaning convert it to a list of dictionaries.
    # Can also use the Django Rest Framework serializers, Django Ninja, model_to_dict, pydantic to turn data to dict.
    for doc in qs:
        response_data.append({
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
        })
    return response_data

@tool
def get_document(document_id: int, config: RunnableConfig):  # Parameters will take arguments as dictionary. 
    # put RunnableConfig after the arguments you need for the function.
    """Get a specific document by ID for a User."""
    user_id = config.get("configurable").get("user_id")
    if not user_id:
        raise Exception("User ID not found.")
    try:
        doc = Document.objects.get(id=document_id, owner_id=user_id, active=True)
        response_data = {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
        }
        return response_data
    except Document.DoesNotExist: # It’s raised when you try to retrieve an object that doesn’t exist in the database.
        raise Exception("Document not found or you do not have permission to access it.")
        # return None
    except Exception as e:
        raise Exception(f"An error occurred : {e}, while retrieving the document.")