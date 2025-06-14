"""
LLM Chain module for the Legal AI Assistant.
Handles the question answering process using a local LLM.
"""

import os
from typing import Dict, Any, Optional
from langchain.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from utils.ollama_utils import generate_ollama_completion, is_ollama_running
from utils.openrouter_utils import generate_openrouter_completion, is_openrouter_available

class LegalQAChain:
    """Question answering chain for legal documents using a local LLM."""
    
    def __init__(
        self,
        model_path: str = "models/llama-2-7b-chat.ggmlv3.q4_0.bin",
        temperature: float = 0.1,
        max_tokens: int = 2000,
        top_p: float = 0.95,
        verbose: bool = False,
        use_ollama: bool = False,
        ollama_model: str = "llama2",
        use_openrouter: bool = False,
        openrouter_model: str = "openai/gpt-3.5-turbo"
    ):
        """
        Initialize the QA chain with a local LLM.
        
        Args:
            model_path: Path to the local LLM model file
            temperature: Temperature parameter for the LLM
            max_tokens: Maximum number of tokens to generate
            top_p: Top-p sampling parameter
            verbose: Whether to print verbose output
            use_ollama: Whether to use Ollama for inference
            ollama_model: Name of the Ollama model to use
        """
        self.model_path = model_path
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.verbose = verbose
        self.use_ollama = use_ollama
        self.ollama_model = ollama_model
        self.use_openrouter = use_openrouter
        self.openrouter_model = openrouter_model
        self.chain = None
        self.llm = None
        
        # QA prompt template
        self.qa_system_prompt = """You are a legal assistant specialized in Omani laws. Answer the question based ONLY on the context provided.
If the context doesn't contain the information needed to answer the question, say "I don't have enough information to answer this question based on the Omani legal documents I have access to."
Do not make up or infer information that is not explicitly stated in the context."""
        
        self.qa_prompt_template = """\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer:\n"""
        
        # Summarization prompt template
        self.summary_system_prompt = """You are a legal assistant specialized in summarizing Omani legal documents. Your task is to create a concise and accurate summary of the legal text provided.

Follow these guidelines:
1. Summarize the content in 3-5 lines only
2. Focus on the key legal provisions and requirements
3. Maintain the legal accuracy of the content
4. Use clear and professional language
5. Do not add any information not present in the original text

Your summary should be brief but comprehensive enough to capture the essence of the legal text."""
        
        self.summary_prompt_template = """\nLegal Text to Summarize:\n{text}\n\nConcise Summary (3-5 lines only):\n"""
        
        self.initialize()
        
    def initialize(self):
        """
        Initialize the QA chain with the appropriate LLM.
        """
        if self.use_openrouter:
            # Use OpenRouter for inference
            self.model_type = "openrouter"
            print(f"Using OpenRouter model: {self.openrouter_model}")
            # Force initialization to succeed for OpenRouter
            self.initialized = True
        elif self.use_ollama and is_ollama_running():
            # Use Ollama for inference
            self.model_type = "ollama"
            print(f"Using Ollama model: {self.ollama_model}")
            self.initialized = True
        else:
            # Use local LLM if model exists
            if os.path.exists(self.model_path):
                callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]) if self.verbose else None
                
                self.llm = LlamaCpp(
                    model_path=self.model_path,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=self.top_p,
                    callback_manager=callback_manager,
                    verbose=self.verbose,
                    n_ctx=4096  # Context window size
                )
                
                # Create the prompt template for QA
                self.prompt_template = PromptTemplate(
                    input_variables=["context", "question"],
                    template=self.qa_system_prompt + self.qa_prompt_template
                )
                
                # Create the LLM chain
                self.chain = LLMChain(
                    llm=self.llm,
                    prompt=self.prompt_template,
                    verbose=verbose
                )
                self.model_type = "local"
            else:
                self.model_type = None
                print(f"Warning: Model file not found at {model_path}. LLM chain not initialized.")
    
    def answer_question(self, question: str, context: str) -> str:
        """
        Answer a question based on the provided context.
        
        Args:
            question: User question
            context: Context information from retrieved documents
            
        Returns:
            Answer to the question
        """
        if self.model_type is None:
            return "I apologize, but the AI model is not properly initialized. Please make sure the model file exists or Ollama is running and try again."
        
        # Check if context is empty
        if not context or context.strip() == "":
            return "I don't have enough information in my legal documents to answer this question. Please try asking about Omani laws that are included in the loaded documents."
        
        try:
            if self.model_type == "openrouter":
                # Use OpenRouter for inference
                prompt = self.qa_prompt_template.format(context=context, question=question)
                
                # Make sure we have a valid model ID
                model_id = self.openrouter_model
                if not model_id or model_id == "":
                    model_id = "openai/gpt-3.5-turbo"  # Default fallback
                    print(f"Using default OpenRouter model: {model_id}")
                
                # Print debug information about the context
                print(f"\nQuestion: {question}")
                print(f"Context length: {len(context)} characters")
                print(f"Context sample: {context[:200]}..." if len(context) > 200 else f"Context: {context}")
                
                response = generate_openrouter_completion(
                    model_id=model_id,
                    prompt=prompt,
                    system_prompt=self.qa_system_prompt,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.strip()
            elif self.model_type == "ollama":
                # Use Ollama for inference
                prompt = self.qa_prompt_template.format(context=context, question=question)
                response = generate_ollama_completion(
                    model_name=self.ollama_model,
                    prompt=prompt,
                    system_prompt=self.qa_system_prompt,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.strip()
            else:
                # Use local LLM chain
                response = self.chain.run(context=context, question=question)
                return response.strip()
        except Exception as e:
            return f"An error occurred while processing your question: {str(e)}"
    
    def summarize_text(self, text: str) -> str:
        """
        Create a concise summary of the provided legal text.
        
        Args:
            text: Legal text to summarize
            
        Returns:
            Concise summary of the text (3-5 lines)
        """
        if self.model_type is None:
            return "I apologize, but the AI model is not properly initialized. Please make sure the model file exists or Ollama is running and try again."
        
        try:
            if self.model_type == "openrouter":
                # Use OpenRouter for inference
                prompt = self.summary_prompt_template.format(text=text)
                response = generate_openrouter_completion(
                    model_id=self.openrouter_model,
                    prompt=prompt,
                    system_prompt=self.summary_system_prompt,
                    temperature=self.temperature,
                    max_tokens=500  # Limit tokens for summary
                )
                return response.strip()
            elif self.model_type == "ollama":
                # Use Ollama for inference
                prompt = self.summary_prompt_template.format(text=text)
                response = generate_ollama_completion(
                    model_name=self.ollama_model,
                    prompt=prompt,
                    system_prompt=self.summary_system_prompt,
                    temperature=self.temperature,
                    max_tokens=500  # Limit tokens for summary
                )
                return response.strip()
            else:
                # Use local LLM for summarization
                # Create a temporary prompt template for summarization
                summary_prompt = PromptTemplate(
                    input_variables=["text"],
                    template=self.summary_system_prompt + self.summary_prompt_template
                )
                
                # Create a temporary chain for summarization
                summary_chain = LLMChain(
                    llm=self.llm,
                    prompt=summary_prompt,
                    verbose=self.verbose
                )
                
                response = summary_chain.run(text=text)
                return response.strip()
        except Exception as e:
            return f"An error occurred while creating the summary: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        if self.model_type is None:
            return {"status": "not_loaded", "path": self.model_path}
        
        if self.model_type == "ollama":
            return {
                "status": "loaded",
                "type": "ollama",
                "model": self.ollama_model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
        else:
            return {
                "status": "loaded",
                "type": "local",
                "path": self.model_path,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p
            }


def create_local_chain(model_path: str, temperature: float = 0.1, max_tokens: int = 2000) -> LegalQAChain:
    """
    Create a QA chain using a local LLM model.
    
    Args:
        model_path: Path to the local LLM model file
        temperature: Temperature parameter for the LLM
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        Initialized LegalQAChain
    """
    return LegalQAChain(
        model_path=model_path,
        temperature=temperature,
        max_tokens=max_tokens,
        use_ollama=False
    )

def create_ollama_chain(model_name: str, temperature: float = 0.1, max_tokens: int = 2000) -> LegalQAChain:
    """
    Create a QA chain using an Ollama model.
    
    Args:
        model_name: Name of the Ollama model to use
        temperature: Temperature parameter for the LLM
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        Initialized LegalQAChain
    """
    return LegalQAChain(
        temperature=temperature,
        max_tokens=max_tokens,
        use_ollama=True,
        ollama_model=model_name
    )

if __name__ == "__main__":
    # Example usage with Ollama
    if is_ollama_running():
        print("Testing with Ollama")
        qa_chain = LegalQAChain(use_ollama=True, ollama_model="llama2")
    else:
        print("Ollama not running, testing with local model")
        qa_chain = LegalQAChain(model_path="models/llama-2-7b-chat.ggmlv3.q4_0.bin")
    
    # Test with a sample question and context
    question = "What is the punishment for theft according to Omani laws?"
    context = """
    According to Article 279 of the Omani Penal Code, the punishment for theft is imprisonment for a period not less than three months and not exceeding three years, and a fine not less than 100 Omani Rials and not exceeding 500 Omani Rials.
    
    In case of aggravated theft, as per Article 280, the punishment is increased to imprisonment for a period not less than three years and not exceeding seven years.
    """
    
    answer = qa_chain.answer_question(question, context)
    print(f"Question: {question}")
    print(f"Answer: {answer}")
