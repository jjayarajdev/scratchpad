from milvus import MilvusClient

# Replace with your Milvus connection details
milvus_client = MilvusClient(host="localhost", port="19530")

def create_collections(folder_names,user_role):
    # Get user information from authentication
#  username = utility.list_usernames(using='default')
 # user_role = utility.list_roles(include_user_info=False, using="default")


  """Creates Milvus collections for each folder with default schema."""
  for folder_name in folder_names:
    if user_role == "admin":
      collection_schema = {"metric": {"similarity_type": "L2"}, "fields": [{"name": "document", "type": "VECTOR", "dim": 128}]}
      milvus_client.create_collection(name=folder_name, schema=collection_schema)
    else:
      print(f"Username with role {user_role} cannot create collections.")

folder_names = ["management", "internal", "property"]  # Your folder names
create_collections(folder_names)

from milvus import Permission, CollectionSchema

def define_roles(milvus_client):
  """Defines roles (admin, client) with specific permissions on collections."""
  # Admin Role (Create, Search, Query all collections)
  admin_role = Role(name="admin")
  admin_create_grant = Permission.create_collection()
  admin_search_grant = Permission.search(collections=["*"])  # Grant access to all collections
  admin_grant = admin_role.create_permission(actions=[admin_create_grant, admin_search_grant])
  milvus_client.create_role(role=admin_role)
  milvus_client.add_permission_to_role(role_name="admin", permission=admin_grant)

  # Client Role (Search, Query on specific collections)
  client_role = Role(name="client")
  management_grant = Permission.search(collections=["management"])
  property_grant = Permission.search(collections=["property"])
  client_grant = client_role.create_permission(actions=[management_grant, property_grant])
  milvus_client.create_role(role=client_role)
  milvus_client.add_permission_to_role(role_name="client", permission=client_grant)

define_roles(milvus_client)

def extract_permissions(role_name, milvus_client):
  """Retrieves permissions granted to a specific role."""
  role = milvus_client.get_role(name=role_name)
  permission_info = role.get_permission()
  granted_collections = [permission.collections for permission in permission_info.actions if isinstance(permission, Permission.Search)]
  return granted_collections

# Example usage
granted_collections = extract_permissions(role_name="admin", milvus_client=milvus_client)
print(granted_collections)  # Output: [['*']] (admin has access to all collections)

def query_collections():
  data = request.json
  role = data.get('role')
  vectors_to_search = data.get('vectors_to_search')

  if role not in ['admin', 'client']:
      return jsonify({'error': 'Invalid role specified'}), 400

  # Get granted collections based on role
  granted_collections = extract_permissions(role_name=role, milvus_client=milvus_client)

  # Define top-k value for search
  top_k = 5

  # Perform search on authorized collections
  search_results = {}
  for collection_name in granted_collections[0]:  # Assuming a single list is returned
      if role == 'admin':
          results = milvus_client.search(collection_name, vectors_to_search, top_k=top_k)
      elif role == 'client':
          # Restrict collections based on role (management, property)
          if collection_name in ["management", "property"]:
              results = milvus_client.search(collection_name, vectors_to_search, top_k=top_k)
          else:
              continue  # Skip unauthorized collections
      search_results[collection_name] = [result for result in results]

  return jsonify(search_results)


def func(folder_name):
    folder_paths = {
        "management": r"C:\Users\ADMIN\Downloads\management",
        "Internal": r"C:\Users\ADMIN\Downloads\Internal",
        "lease": r"C:\Users\ADMIN\Downloads\lease"
    }
    folder_names = folder_paths.get(folder_name)
    if folder_names:
        create_collections(folder_names)
    else:
        raise ValueError("Invalid folder name provided")
    
if __name__ == "__main__":
    user_role="admin"
    folder_name = "management"  
    func(folder_name)
    
