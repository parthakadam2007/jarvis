import pickle
import os
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredExcelLoader,Docx2txtLoader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_chroma import Chroma
print('Imported')


    

def upload_Embeddings():
    """Function to process files from the 'uploads' directory and store embeddings."""
    

    # Define paths
    current_dir = os.path.dirname(os.path.realpath(__file__))
    uploads_path = os.path.join(current_dir, 'uploads')
    persist_directory = os.path.join(current_dir, 'db', 'chroma_db')

    # Get all files in the uploads directory
    files = [os.path.join(uploads_path, f) for f in os.listdir(uploads_path)]
    in_database = []
    path_in_database = 'C://Users//DELL//Desktop//easyMail//backend//in_database.pkl'
    
    with open ('C://Users//DELL//Desktop//easyMail//backend//in_database.pkl', 'rb') as file:

        
        in_database = pickle.load(file)
        if file.read() == "b''" or os.path.getsize(path_in_database) == 0:
            in_database = []


  
    for f in files:

        if os.path.basename(f) not in in_database:
            ext = f.rsplit('.', 1)[-1].lower()

            # Load document based on file type
            if ext == 'txt':
                print(f'{os.path.basename(f)} ---> is a txt')
                loader = TextLoader(f)
            elif ext == 'pdf':
                print(f'{os.path.basename(f)} ---> is a pdf')
                loader = PyPDFLoader(f)
            elif ext == 'docx':  
                print(f'{os.path.basename(f)} ---> is a docx')
                loader = Docx2txtLoader(f) # Consider using a DocxLoader instead
            elif ext == 'xlsx':  
                print(f'{os.path.basename(f)} ---> is an xlsx')
                loader = UnstructuredExcelLoader(f)
            else:
                print(f'{os.path.basename(f)} ---> skipped')
                continue  

            document = loader.load()
            in_database.append(os.path.basename(f))

            # Split the document into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
            docs = text_splitter.split_documents(document)

            if not docs:
                print(f"Split into {len(docs)} chunks, so skipped")
                continue

            print(f"Split into {len(docs)} chunks")

            # Generate embeddings and store in Chroma
            embeddings = VertexAIEmbeddings(model="text-embedding-004")
            db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
            
            
            # Store data using pickle
            with open('C://Users//DELL//Desktop//easyMail//backend//in_database.pkl', 'wb') as file:
                pickle.dump(in_database, file)
                
            print(f'Done with embeddings for {f}')
        else:
            print(f'{os.path.basename(f)} file  already in the database')
    print(in_database)
    return in_database

upload_Embeddings()