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
        ollama_model: str = "llama2"
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
        self.chain = None
        self.llm = None
        
        # QA prompt template
        self.qa_system_prompt = """You are a legal assistant specialized in Omani laws. Answer the question based ONLY on the context provided.
If the context doesn't contain the information needed to answer the question, say "I don't have enough information to answer this question based on the Omani legal documents I have access to."
Do not make up or infer information that is not explicitly stated in the context."""
        
        self.qa_prompt_template = """\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer:\n"""
        
        # Initialize LLM based on the chosen method
        if use_ollama:
            # Check if Ollama is running
            if is_ollama_running():
                print(f"Using Ollama model: {ollama_model}")
                self.model_type = "ollama"
            else:
                print("Warning: Ollama is not running. Please start Ollama and try again.")
                self.model_type = None
        else:
            # Initialize LLM if model exists
            if os.path.exists(model_path):
                callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]) if verbose else None
                
                self.llm = LlamaCpp(
                    model_path=model_path,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    callback_manager=callback_manager,
                    verbose=verbose,
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
        
        try:
            if self.model_type == "ollama":
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
