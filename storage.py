import os
import json
import shutil
import hashlib
import faiss
from langchain_community.vectorstores import FAISS

class Storage:
   def __init__(self):
       self.upload_folder = "uploads"
       self.table_folder = "tables"
       self.vector_db = "vector_db/text"
       self.image_folder = "vector_db/image"
       self.chat_folder = "chat_memory"
       os.makedirs(self.upload_folder, exist_ok=True)
       os.makedirs(self.table_folder, exist_ok=True)
       os.makedirs(self.vector_db, exist_ok=True)
       os.makedirs(self.image_folder, exist_ok=True)
       os.makedirs(self.chat_folder, exist_ok=True)
       self.index_file = "indexed_files.json"
       self.chat_file = os.path.join(
           self.chat_folder,
           "chat_history.json"
       )
       self.image_index = os.path.join(
           self.image_folder,
           "image_index.faiss"
       )
       self.image_metadata = os.path.join(
           self.image_folder,
           "image_metadata.json"
       )
   def save_uploaded_file(self, uploaded_file):
       path = os.path.join(
           self.upload_folder,
           uploaded_file.name
       )
       with open(path, "wb") as f:
           f.write(uploaded_file.getbuffer())
       return path
   
   def file_hash(self, file_path):
       md5 = hashlib.md5()
       with open(file_path, "rb") as f:
           while True:
               chunk = f.read(8192)
               if not chunk:
                   break
               md5.update(chunk)
       return md5.hexdigest()
   
   def load_indexed_files(self):
       if os.path.exists(self.index_file):
           with open(self.index_file, "r") as f:
               return json.load(f)
       return {}
   
   def save_indexed_files(self, data):
       with open(self.index_file, "w") as f:
           json.dump(data, f, indent=4)

   def is_new_file(self, file_path):
       indexed = self.load_indexed_files()
       name = os.path.basename(file_path)
       current_hash = self.file_hash(file_path)
       if indexed.get(name) == current_hash:
           return False
       indexed[name] = current_hash
       self.save_indexed_files(indexed)
       return True
   
   def load_vectorstore(self, embeddings):
       index_path = os.path.join(
           self.vector_db,
           "index.faiss"
       )
       if os.path.exists(index_path):
           return FAISS.load_local(
               self.vector_db,
               embeddings,
               allow_dangerous_deserialization=True
           )
       return None
   
   def save_vectorstore(self, vectorstore):
       vectorstore.save_local(
           self.vector_db
       )

   def load_image_index(self):
       if os.path.exists(self.image_index):
           return faiss.read_index(
               self.image_index
           )
       return None
   
   def save_image_index(self, index):
       faiss.write_index(
           index,
           self.image_index
       )

   def load_image_metadata(self):
       if os.path.exists(self.image_metadata):
           with open(
               self.image_metadata,
               "r",
               encoding="utf-8"
           ) as f:
               return json.load(f)
       return []

   def save_image_metadata(self, metadata):
       with open(
           self.image_metadata,
           "w",
           encoding="utf-8"
       ) as f:
           json.dump(
               metadata,
               f,
               indent=4
           )

   def load_chat_history(self):
       if os.path.exists(self.chat_file):
           with open(
               self.chat_file,
               "r",
               encoding="utf-8"
           ) as f:
               return json.load(f)
       return []
   
   def save_chat(self, question, answer):
       history = self.load_chat_history() 
       history.append(
            {
                "question": question,
                "answer": answer
            }
        )
       with open(
           self.chat_file,
           "w",
           encoding="utf-8"
       ) as f:
           json.dump(
               history,
               f,
               indent=4
           )

   def clear_database(self):
       shutil.rmtree(
           "vector_db",
           ignore_errors=True
       )
       shutil.rmtree(
           self.table_folder,
           ignore_errors=True
       )
       shutil.rmtree(
           self.chat_folder,
           ignore_errors=True
       )
       if os.path.exists(self.index_file):
           os.remove(self.index_file)

       os.makedirs(
           self.vector_db,
           exist_ok=True
       )
       os.makedirs(
           self.image_folder,
           exist_ok=True
       )
       os.makedirs(
           self.table_folder,
           exist_ok=True
       )
       os.makedirs(
           self.chat_folder,
           exist_ok=True
       )

   def get_uploaded_files(self):
       return list(self.load_indexed_files().keys())
   
   def delete_uploaded_file(self, filename):
       path = os.path.join(
           self.upload_folder,
           filename
       )
       if os.path.exists(path):
           os.remove(path)

   def get_session_history(self, session_id):
       history = self.load_chat_history()
       return history