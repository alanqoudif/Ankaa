"""
Document comparison utilities for the Sultanate Legal AI Assistant.
Provides functionality for comparing legal documents and extracting relevant information.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class DocumentComparator:
    """Class for comparing legal documents and extracting relevant information."""
    
    def __init__(self, retriever, llm_or_chain, language: str = "en"):
        """
        Initialize the document comparator.
        
        Args:
            retriever: Document retriever for fetching relevant documents
            llm_or_chain: Language model or QA chain for generating comparisons
            language: Language for the comparison (en or ar)
        """
        import streamlit as st
        from llm_chain import LegalQAChain
        
        self.retriever = retriever
        self.language = language
        self.initialized = False
        
        # Check if we received a LegalQAChain or an LLM
        if isinstance(llm_or_chain, LegalQAChain):
            # If it's a LegalQAChain, we'll use it directly for text generation
            self.qa_chain = llm_or_chain
            self.llm = None  # We don't need a separate LLM
            st.info("Using LegalQAChain for document comparison")
        else:
            # If it's an LLM, we'll use it to create our chains
            self.llm = llm_or_chain
            self.qa_chain = None
            
            # Check if LLM is available
            if self.llm is None:
                st.error("LLM is not available for document comparison. Please initialize the system with a valid model.")
                return
        
        try:
            # Initialize the comparison chain
            self.comparison_chain = self._create_comparison_chain()
            
            # Initialize the summarization chain
            self.summarization_chain = self._create_summarization_chain()
            
            self.initialized = True
            st.success("Document comparison initialized successfully")
        except Exception as e:
            st.error(f"Error initializing document comparison: {e}")
    
    def _create_comparison_chain(self):
        """
        Create a chain for identifying laws to compare.
        
        Returns:
            Chain for comparison (either LLMChain or a wrapper around LegalQAChain)
        """
        # Define the prompt template based on language
        if self.language == "ar":
            template = """
            أنت مساعد قانوني ذكي متخصص في القوانين العمانية. مهمتك هي تحليل طلب المستخدم وتحديد القوانين التي يرغب في مقارنتها.
            
            طلب المستخدم: {query}
            
            حدد القوانين التي يجب مقارنتها والموضوع الرئيسي للمقارنة.
            
            القوانين للمقارنة (قائمة مفصولة بفواصل):
            موضوع المقارنة:
            """
        else:
            template = """
            You are a smart legal assistant specializing in Omani laws. Your task is to analyze the user's request and identify the laws they want to compare.
            
            User request: {query}
            
            Identify the laws that should be compared and the main topic of comparison.
            
            Laws to compare (comma-separated list):
            Comparison topic:
            """
        
        prompt = PromptTemplate(
            input_variables=["query"],
            template=template
        )
        
        if self.llm is not None:
            # If we have an LLM, create a standard LLMChain
            from langchain.chains import LLMChain
            return LLMChain(llm=self.llm, prompt=prompt)
        else:
            # If we're using a LegalQAChain, create a wrapper
            class QAChainWrapper:
                def __init__(self, qa_chain, prompt):
                    self.qa_chain = qa_chain
                    self.prompt = prompt
                
                def run(self, **kwargs):
                    # Format the prompt
                    formatted_prompt = self.prompt.format(**kwargs)
                    # Use the QA chain to generate a response
                    # We'll use an empty context since we're just asking a question
                    return self.qa_chain.answer_question(formatted_prompt, context="")
            
            return QAChainWrapper(self.qa_chain, prompt)
    
    def _create_summarization_chain(self):
        """
        Create a chain for summarizing law content.
        
        Returns:
            Chain for summarization (either LLMChain or a wrapper around LegalQAChain)
        """
        # Define the prompt template based on language
        if self.language == "ar":
            template = """
            أنت مساعد قانوني ذكي متخصص في القوانين العمانية. مهمتك هي تلخيص المعلومات المهمة من القانون المحدد حول موضوع معين.
            
            القانون: {law_name}
            الموضوع: {topic}
            
            محتوى القانون:
            {content}
            
            قم بتلخيص النقاط الرئيسية المتعلقة بالموضوع من هذا القانون. قدم النقاط في شكل قائمة نقطية واضحة ومختصرة.
            
            النقاط الرئيسية (مفصولة بعلامة |):
            """
        else:
            template = """
            You are a smart legal assistant specializing in Omani laws. Your task is to summarize important information from the specified law about a specific topic.
            
            Law: {law_name}
            Topic: {topic}
            
            Law content:
            {content}
            
            Summarize the key points related to the topic from this law. Present the points as a clear and concise bullet list.
            
            Key points (separated by |):
            """
        
        prompt = PromptTemplate(
            input_variables=["law_name", "topic", "content"],
            template=template
        )
        
        if self.llm is not None:
            # If we have an LLM, create a standard LLMChain
            from langchain.chains import LLMChain
            return LLMChain(llm=self.llm, prompt=prompt)
        else:
            # If we're using a LegalQAChain, create a wrapper
            class QAChainWrapper:
                def __init__(self, qa_chain, prompt):
                    self.qa_chain = qa_chain
                    self.prompt = prompt
                
                def run(self, **kwargs):
                    # Format the prompt
                    formatted_prompt = self.prompt.format(**kwargs)
                    # Use the QA chain to generate a response
                    # We'll use the content as context since we're summarizing
                    return self.qa_chain.answer_question(
                        question=f"Summarize the key points about {kwargs.get('topic')} in {kwargs.get('law_name')}",
                        context=kwargs.get('content', '')
                    )
            
            return QAChainWrapper(self.qa_chain, prompt)
    
    def _extract_laws_and_topic(self, query: str) -> Tuple[List[str], str]:
        """
        Extract the laws to compare and the comparison topic from the query.
        
        Args:
            query: User query
            
        Returns:
            Tuple of (list of laws to compare, comparison topic)
        """
        # Run the comparison chain
        result = self.comparison_chain.run(query=query)
        
        # Extract laws and topic
        laws_to_compare = []
        comparison_topic = ""
        
        # Parse the result
        lines = result.strip().split('\n')
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                
                if "laws to compare" in key or "قوانين للمقارنة" in key:
                    laws_to_compare = [law.strip() for law in value.split(",")]
                elif "comparison topic" in key or "موضوع المقارنة" in key:
                    comparison_topic = value
        
        return laws_to_compare, comparison_topic
    
    def _retrieve_law_documents(self, law_name: str, topic: str, k: int = 5) -> List[Document]:
        """
        Retrieve documents related to a specific law and topic.
        
        Args:
            law_name: Name of the law
            topic: Topic for comparison
            k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        # Create a query that combines the law name and topic
        query = f"{law_name} {topic}"
        
        # Retrieve documents
        documents = self.retriever.retrieve(query, k=k)
        
        # Filter documents to only include those from the specified law
        filtered_docs = []
        for doc in documents:
            # Check if the document is from the specified law
            if law_name.lower() in doc.metadata.get("source", "").lower():
                filtered_docs.append(doc)
        
        return filtered_docs
    
    def _summarize_law_content(self, law_name: str, topic: str, documents: List[Document]) -> List[str]:
        """
        Summarize the content of a law related to a specific topic.
        
        Args:
            law_name: Name of the law
            topic: Topic for comparison
            documents: List of documents from the law
            
        Returns:
            List of key points from the law
        """
        if not documents:
            return []
        
        # Combine the content of all documents
        combined_content = "\n\n".join([doc.page_content for doc in documents])
        
        # Run the summarization chain
        result = self.summarization_chain.run(
            law_name=law_name,
            topic=topic,
            content=combined_content
        )
        
        # Extract key points
        key_points = [point.strip() for point in result.split("|") if point.strip()]
        
        return key_points
    
    def compare_laws(self, query: str, k: int = 5) -> Dict[str, Any]:
        """
        Compare laws based on the user query.
        
        Args:
            query: User query
            k: Number of documents to retrieve per law
            
        Returns:
            Dictionary with comparison results
        """
        import streamlit as st
        
        # Check if the comparator is initialized
        if not getattr(self, 'initialized', False):
            return {
                "success": False,
                "message": "Document comparator is not properly initialized. Please initialize the system with a valid model." if self.language == "en" else
                           "لم يتم تهيئة أداة المقارنة بشكل صحيح. يرجى تهيئة النظام باستخدام نموذج صالح."
            }
        
        try:
            # Extract laws to compare and comparison topic
            laws_to_compare, comparison_topic = self._extract_laws_and_topic(query)
            
            if not laws_to_compare:
                return {
                    "success": False,
                    "message": "Could not identify laws to compare from your query. Please specify the laws you want to compare." if self.language == "en" else
                               "لم أتمكن من تحديد القوانين المراد مقارنتها من استفسارك. يرجى تحديد القوانين التي ترغب في مقارنتها."
                }
        except Exception as e:
            st.error(f"Error extracting laws to compare: {e}")
            return {
                "success": False,
                "message": f"Error processing comparison query: {str(e)}"
            }
        
        # Initialize results
        results = {}
        
        # Process each law
        for law_name in laws_to_compare:
            # Retrieve documents for this law
            documents = self._retrieve_law_documents(law_name, comparison_topic, k=k)
            
            if not documents:
                # No documents found for this law
                results[law_name] = {
                    "documents": [],
                    "summary": [f"No information found about {comparison_topic} in {law_name}." if self.language == "en" else
                                f"لم يتم العثور على معلومات حول {comparison_topic} في {law_name}."]
                }
            else:
                # Summarize the content
                summary = self._summarize_law_content(law_name, comparison_topic, documents)
                
                # Add to results
                results[law_name] = {
                    "documents": documents,
                    "summary": summary
                }
        
        return {
            "success": True,
            "laws_compared": laws_to_compare,
            "comparison_topic": comparison_topic,
            "results": results
        }
