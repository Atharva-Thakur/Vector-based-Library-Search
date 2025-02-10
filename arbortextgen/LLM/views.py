from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from django.conf import settings
import os
import re

def remove_noise(text):
    """
    Cleans retrieved context by removing metadata, redundant headers, and extra whitespaces.
    """
    # Remove metadata (e.g., "Source: Wikipedia, Last Updated: 2023")
    text = re.sub(r'Source: .*|Last Updated: .*', '', text)

    # Remove repeated section headers (e.g., "Introduction", "Summary")
    text = re.sub(r'\b(Introduction|Summary|Conclusion)\b', '', text, flags=re.IGNORECASE)

    # Remove excessive new lines and spaces
    text = re.sub(r'\n+', '\n', text).strip()

    return text


class UpdateTitleView(APIView):
    def post(self, request):
        new_title = request.data.get("title")

        if not new_title:
            return Response({"error": "No title provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Update FAISS index path
        settings.FAISS_INDEX_PATH = os.path.join(settings.MEDIA_ROOT, f'vectorstores/{new_title}')

        return Response({"message": "Title updated successfully", "new_title": settings.FAISS_INDEX_PATH},
                        status=status.HTTP_200_OK)
class LLMChat(APIView):
    def post(self, request):
        # try:
        question = request.data.get('question', '')
        user_grade = int(request.data.get('grade', 0))  # Default to 0 if no grade is provided

        if not question:
            return Response({"error": "No question provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Load FAISS index and enforce grade-based restrictions
        context = self.load_faiss_and_answer(question, user_grade)

        # STRICT RESTRICTION: If no matching documents found, return "I cannot answer this question."
        if context is None:
            return Response({
                "question": question,
                "answer": f"I cannot answer this question since you are from grade-{user_grade}."
            }, status=status.HTTP_200_OK)

        # ✅ Lazy-load LLM only when needed
        llm_model = getattr(self, 'llm', None)
        if llm_model is None:
            print("⚡ Loading LLM model on demand...")
            llm_model = self.load_llm()
            self.llm = llm_model  # Cache model for future use

        if not llm_model:
            return Response({"error": "Failed to load model"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Construct structured input for the model
        structured_input = {
            "context": context,
            "question": question
        }

        # Invoke the model with the structured input
        output = llm_model.invoke(structured_input)

        output_dict = {
            "question": question,
            "answer": output
        }

        return Response(output_dict)

        # except Exception as e:
        #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def load_faiss_and_answer(self, question, user_role):
        """Load FAISS index and retrieve relevant documents for a specific user role."""

        FAISS_INDEX_PATH = settings.FAISS_INDEX_PATH  # Use dynamic path

        # Load FAISS index
        faiss_index = self.load_faiss_index(FAISS_INDEX_PATH)

        # Perform similarity search and retrieve relevant documents
        relevant_texts = self.query_faiss_index(question, faiss_index, user_role)

        # If no relevant texts match the user's role, return None
        if not relevant_texts:
            return None

        return remove_noise(relevant_texts)

    def load_faiss_index(self, index_path):
        """Load the FAISS index using LangChain's FAISS wrapper."""
        embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformer/bge-m3")

        # Load FAISS index and allow deserialization
        faiss_index = FAISS.load_local(index_path, embeddings_model, allow_dangerous_deserialization=True)
        return faiss_index

    def query_faiss_index(self, query, faiss_index, user_grade):
        """Retrieve documents from FAISS but enforce strict grade-based access control."""

        # Retrieve top 5 relevant documents
        results = faiss_index.similarity_search(query, k=5)

        # Define grade-based access: Higher grades can access lower grades, but not vice versa
        def has_access(doc_grade):
            return doc_grade <= user_grade  # Allow access if document grade is ≤ user grade

        # Filter results based on grade hierarchy
        filtered_results = [
            doc for doc in results if has_access(doc.metadata.get("grade", 0))  # Default grade = 0 if missing
        ]

        # If no results match, return None (Restricted Access)
        if not filtered_results:
            return None

        return " ".join([doc.page_content for doc in filtered_results])

    def load_llm(self):
        try:
            template = """You are a highly knowledgeable AI assistant. You must only answer based on the provided context. 
            If the answer is not found in the context, respond with "I don't know."

            Context:
            {context}

            Question: {question}

            Answer:"""

            from langchain_core.prompts import PromptTemplate
            from langchain_community.llms import LlamaCpp
            from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

            prompt = PromptTemplate.from_template(template)

            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

            print("⚡ Attempting to load LLM model...")  # Debugging line

            llm = LlamaCpp(
                model_path="model/tinyllama-1.1b-chat-v1.0.Q8_0.gguf",
                n_ctx=4096,
                max_tokens=1048,
                callback_manager=callback_manager,
                temperature=0.2,
                verbose=True
            )

            print("✅ LLM Model Loaded Successfully!")
            return prompt | llm

        except Exception as e:
            print(f"❌ Failed to load model: {e}")  # Print the exact error
            return None  # Return None if model fails to load

