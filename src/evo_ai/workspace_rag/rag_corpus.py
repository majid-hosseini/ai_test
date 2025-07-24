from . import rag

def get_corpora_list(corpus_status=None):
    '''
    Get all corpora available to the RAG engine.
    If corpus_status is None, return all corpora.
    If corpus_status is specified, return only corpora with that status.
    '''
    all_corpora = {}
    response = rag.list_corpora()
    for corpus in response.rag_corpora:
        if corpus_status is None or corpus.corpus_status == corpus_status:
            all_corpora[corpus.display_name] = corpus
    
    return all_corpora


class RAGCorpus:
    def __init__(self, gcp_resource_id):
        self.gcp_resource_id = gcp_resource_id
        
        self.corpus = None
        self.connect_to_corpus()

        self.corpus_name = self.corpus.name if self.corpus else None

    def set_corpus_display_name(self):
        return f'workspace_{self.workspace_name}_{self.workspace_id}'

    def connect_to_corpus(self):
        all_corpora = get_corpora_list()
        
        if self.gcp_resource_id not in all_corpora:
            raise ValueError(f"Corpus {self.gcp_resource_id} not found")
        
        corpus_full_name =  all_corpora[self.gcp_resource_id].name
        self.corpus = rag.get_corpus(name=corpus_full_name)

    def get_file_names(self):
        if not self.corpus:
            return None
        
        corpus_file_names = []
        try:
            files = rag.list_files(corpus_name=self.corpus.name)
            for file in files:
                corpus_file_names.append(file.display_name)
        except Exception as e:
            print(f"An error occurred: {e}")
    
        return [file.display_name for file in self.corpus.files]