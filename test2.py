from pymilvus import utility
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, db
from pymilvus import Role, utility
from pymilvus import MilvusClient
import random
# connections.connect(alias="default", uri='https://in01-dd7aa06ed745f7f.gcp-us-west1.vectordb.zillizcloud.com:443', token='2740a0c084502c386d873daca18f10f06342ae699f7f0342a9b66d32ac06b2d921968af3b8e634c53d01a6da3a069b6d64e713ac',)

# milvus_client = MilvusClient(
   
#     uri="https://in01-dd7aa06ed745f7f.gcp-us-west1.vectordb.zillizcloud.com:443",
#     token="2740a0c084502c386d873daca18f10f06342ae699f7f0342a9b66d32ac06b2d921968af3b8e634c53d01a6da3a069b6d64e713ac", # replace this with your token
# )

# connections.connect(
#   alias="default",
#   uri="https://in01-dd7aa06ed745f7f.gcp-us-west1.vectordb.zillizcloud.com:443",
#   token="2740a0c084502c386d873daca18f10f06342ae699f7f0342a9b66d32ac06b2d921968af3b8e634c53d01a6da3a069b6d64e713ac",
# )

def connect_to_milvus(db_name="algo_db"):
    connections.connect(
        alias='default',
        host='192.168.1.73',
        port='19530',
        user='algoleap.dialogflow@gmail.com',
        password='Algo@1234',
        db_name=db_name)




users = utility.list_usernames(using='default')
print(users)

utility.create_user('Jay', 'Algo@123', using='default') 

#database=db.list_database()
# print(database)
#database = db.create_database("algo_db")

role_name = "client"
# role = Role(role_name, using='default')
clients = Role(role_name, using="default")
clients.create()

clients.add_user("Sai")
# print(role.is_exist())
# print(role.list_grants())
print(clients.get_users())

# grant = Role(role)
# #role.grant("Collection", "Insert")
# print(role.list_grants())



#role.create()
#role.add_user('Jay')
# if role.is_exist():
#     role.grant("Collection", "*", "Search")
# print(role.list_grants())

#utility.list_roles('Jay', using="default")


#database = db.create_database("db1")
# role1=role.get_users('client')
# print(role1)


# def create_collection(collection_name, db_name):
#     default_fields = [
#         FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
#         FieldSchema(name="double", dtype=DataType.DOUBLE),
#         FieldSchema(name="fv", dtype=DataType.FLOAT_VECTOR, dim=128)
#     ]
#     default_schema = CollectionSchema(fields=default_fields)
#     print(f"Create collection:{collection_name} within db:{db_name}")
#     return Collection(name=collection_name, schema=default_schema)
 

# def insert(collection, num, dim):
#     data = [
#         [i for i in range(num)],
#         [float(i) for i in range(num)],
#         [[random.random() for _ in range(dim)] for _ in range(num)],
#     ]
#     collection.insert(data)
#     return data[2]


# METRIC_TYPE = 'IP'
# INDEX_TYPE = 'IVF_FLAT'
# NLIST = 1024
# NPROBE = 16
# TOPK = 3
# # Vector parameters
# DIM = 128
# # max file size of stored index
# INDEX_FILE_SIZE = 32 


# def search(collection, vector_field, id_field, search_vectors):
#     search_param = {
#         "data": search_vectors,
#         "anns_field": vector_field,
#         "param": {"metric_type": METRIC_TYPE, "params": {"nprobe": NPROBE}},
#         "limit": TOPK,
#         "expr": "id >= 0"}
#     results = collection.search(**search_param)
#     for i, result in enumerate(results):
#         print("\nSearch result for {}th vector: ".format(i))
#         for j, res in enumerate(result):
#             print("Top {}: {}".format(j, res))

# def collection_read_write(collection, db_name):
#     col_name = "{}:{}".format(db_name, collection.name)
#     vectors = insert(collection, 10000, DIM)
#     collection.flush()
#     print("\nInsert {} rows data into collection:{}".format(collection.num_entities, col_name))

#     # create index
#     index_param = {
#         "index_type": INDEX_TYPE,
#         "params": {"nlist": NLIST},
#         "metric_type": METRIC_TYPE}
#     collection.create_index("fv", index_param)
#     print("\nCreated index:{} for collection:{}".format(collection.index().params, col_name))

#     # load data to memory
#     print("\nLoad collection:{}".format(col_name))
#     collection.load()
#     # search
#     print("\nSearch collection:{}".format(col_name))
#     search(collection, "fv", "id", vectors[:3])


# if __name__ == '__main__':
#     # connect to milvus and using database db1
#     # there will not check db1 already exists during connect
#     connect_to_milvus(db_name="algo_db")
#     col1_db1 = create_collection("col1_db1", "algo_db")
#     collection_read_write(col1_db1, "db1")
#     print("\nlist collections of database db1:")
#     print(utility.list_collections())
#     print("\nlist databases:")
#     print(db.list_database())