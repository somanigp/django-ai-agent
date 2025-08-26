from documents.models import Document  # Django Document Model/DB
from langchain_core.tools import tool  # Tool is a function that can be called by the LLM/Agent.
from langchain_core.runnables import RunnableConfig  # To pass extra config to the tool function.

# CURD : Create, Update, Retrieve, Delete

@tool
def list_documents(config: RunnableConfig):
    """List the most recent 5 active documents for the current user."""
    # print(config) # {'tags': [], 'metadata': {'user_id': 4}, 'callbacks': None, 'recursion_limit': 25, 'configurable': {'user_id': 4}}
    
    limit = 5
    user_id = config.get("configurable") or config.get("metadata")
    user_id = user_id.get("user_id")  # Get the user_id from the metadata.
    if not user_id:
        raise Exception("User ID not found.")
    qs = Document.objects.filter(owner_id=user_id, active=True).order_by("-created_at")  # We don't need User object. Owner is a foreign key so only owner_id will do.
    # -created_at is reverse of created_at.
    response_data = []
    # Serialize the queryset, meaning convert it to a list of dictionaries.
    # Can also use the Django Rest Framework serializers, Django Ninja, model_to_dict, pydantic to turn data to dict.
    for doc in qs[:limit]:
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
    user_id = config.get("configurable") or config.get("metadata")
    user_id = user_id.get("user_id")  # Get the user_id from the metadata.
    if not user_id:
        raise Exception("User ID not found.")
    try:
        doc = Document.objects.get(id=document_id, owner_id=user_id, active=True)
        response_data = {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "created_at": doc.created_at,
        }
        return response_data
    except Document.DoesNotExist: # It’s raised when you try to retrieve an object that doesn’t exist in the database.
        raise Exception("Document not found or you do not have permission to access it.")
        # return None
    except Exception as e:
        raise Exception(f"An error occurred : {e}, while retrieving the document.")
    
    
@tool
def create_document(title: str, content: str, config: RunnableConfig):  # Parameters will take arguments as dictionary. 
    # put RunnableConfig after the arguments you need for the function.
    """
    Create a new document to store for the user.
    Arguments are:
    title : string max 255 characters
    content : long form text in mini paragraphs or pages.
    """
    user_id = config.get("configurable") or config.get("metadata")
    user_id = user_id.get("user_id")  # Get the user_id from the metadata.
    if not user_id:
        raise Exception("User ID not found.")
    doc = Document.objects.create(title=title, content=content, owner_id=user_id)
    response_data = {
        "id": doc.id,
        "title": doc.title,
        "content": doc.content,
        "created_at": doc.created_at,
    }
    return response_data

@tool
def update_document(document_id: int, title: str = None, content: str = None, config: RunnableConfig = None):  # Parameters will take arguments as dictionary. 
    # put RunnableConfig after the arguments you need for the function.
    """
    Update an existing document for the user by document_id.
    Arguments are:
    document_id : id of document (required)
    title : string max 255 characters (optional)
    content : long form text in mini paragraphs or pages. (optional)
    """
    user_id = config.get("configurable") or config.get("metadata")
    user_id = user_id.get("user_id")  # Get the user_id from the metadata.
    if not user_id:
        raise Exception("User ID not found.")
    
    try:
        doc = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found or you do not have permission to access it.")
    except Exception as e:
        raise Exception(f"An error occurred : {e}, while retrieving the document.")
    if title is not None:
        doc.title = title
    if content is not None:
        doc.content = content
    if title or content:
        doc.save()
    response_data = {
        "id": doc.id,
        "title": doc.title,
        "content": doc.content,
        "created_at": doc.created_at,
    }
    return response_data


@tool
def delete_document(document_id: int, config: RunnableConfig):  # Parameters will take arguments as dictionary. 
    # put RunnableConfig after the arguments you need for the function.
    """Delete a specific document by document_id for a User."""
    user_id = config.get("configurable") or config.get("metadata")
    user_id = user_id.get("user_id")  # Get the user_id from the metadata.
    if not user_id:
        raise Exception("User ID not found.")
    try:
        doc = Document.objects.get(id=document_id, owner_id=user_id, active=True)
        doc.delete()  # This will delete the document from the database. Fetch the object and then delete it.
        response_data = {
            "message": "Document deleted successfully."
        }
        return response_data
    except Document.DoesNotExist: # It’s raised when you try to retrieve an object that doesn’t exist in the database.
        raise Exception("Document not found or you do not have permission to access it.")
        # return None
    except Exception as e:
        raise Exception(f"An error occurred : {e}, while retrieving the document.")


document_tools = [
    update_document,
    delete_document,
    create_document,
    list_documents,  # Make sure both have a short doc string explaining the function.
    get_document,
]