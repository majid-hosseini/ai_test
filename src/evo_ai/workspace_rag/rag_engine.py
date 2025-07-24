
from typing import List
from . import rag

from vertexai.generative_models import (
    Tool
)

from .rag_corpus import RAGCorpus

DEFAULT_VDT = 0.5 
DEFAULT_TOP_K = 10

class RAGEngine:

    def __init__(self, gcp_resource_id):
        self.gcp_resource_id = gcp_resource_id
        self.corpus = None
        self.connect_to_corpus()


    def connect_to_corpus(self):
        try:
            self.corpus = RAGCorpus(self.gcp_resource_id)
        except Exception as e:
            '''
            A workspace may not have a corpus built for it, 
            so we need to handle that case gracefully.
            '''
            print(f"Failed to connect to corpus: {e}")
        

    def has_corpus(self):
        return self.corpus is not None


    def query(self, query_text, top_k=DEFAULT_TOP_K, vdt=DEFAULT_VDT, concat_chunks=True):
        
        if not self.corpus:
            raise ValueError("No corpus connected")
        
        response = rag.retrieval_query(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=self.corpus.corpus_name,
                )
            ],
            text=query_text,
            similarity_top_k=top_k, 
            vector_distance_threshold=vdt, 
        )

        def serialize_chunk(chunk):
            chunk_string = ""
            chunk_string += f"Document: {chunk.source_display_name}\n"    
            chunk_string += f"Content: {chunk.text}\n---\n"
            return chunk_string
        
        if concat_chunks:            
            # Combine the retrieved documents into a single text
            combined_text = "\n".join([serialize_chunk(context) for context in response.contexts.contexts])
            return combined_text
        else:
            return response


    def get_retrieval_tool(self, top_k=DEFAULT_TOP_K, vdt=DEFAULT_VDT):# Create a RAG retrieval tool
        
        if not self.corpus:
            raise ValueError("No corpus connected")
        
        rag_retrieval_tool = Tool.from_retrieval(
            retrieval=rag.Retrieval(
                source=rag.VertexRagStore(
                    rag_resources=[
                        rag.RagResource(
                            rag_corpus=self.corpus.corpus_name,  # Currently only 1 corpus is allowed.
                        )
                    ],
                    similarity_top_k=top_k,  
                    vector_distance_threshold=vdt, 
                ),
            )
        )

        return rag_retrieval_tool


    def refresh_corpus(self):
        '''
        Additional data might have been loaded into the corpus,
        so we need to refresh the class instance.
        '''
        
        self.connect_to_corpus()