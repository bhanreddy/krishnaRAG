"""
LLM Module - Generates answers using local LLM
Integrates with Ollama or other local LLM services
"""
import sys
import os
from typing import Optional, Dict, Tuple
import logging
import re

logger = logging.getLogger(__name__)

# Predefined greeting responses
GREETINGS = {
    # Hello greetings
    r'\b(hi|hello|hey|greetings|namaste|namaskar|pranaam)\b': 
        "🙏 Namaste! Welcome to the Bhagavad Gita AI Assistant. I am here to help you explore the profound teachings of the Bhagavad Gita. Feel free to ask any questions about dharma, yoga, karma, or any other concepts from the sacred text.",
    
    # How are you
    r'\b(how are you|how are ya|how\'re you|how do you do|how you doing)\b':
        "🙏 I am doing well, thank you for asking! I am here and ready to guide you through the wisdom of the Bhagavad Gita. How can I assist you today?",
    
    # What's up
    r'\b(what\'?s up|what\'?s going on|what\'?s happening|sup)\b':
        "🙏 All is well! I'm here to share the timeless wisdom of the Bhagavad Gita with you. What would you like to know?",
    
    # Thank you
    r'\b(thank you|thanks|thankyou|appreciate|much obliged)\b':
        "🙏 You're welcome! I'm honored to serve you. Please feel free to ask more questions about the Bhagavad Gita whenever you need guidance.",
    
    # Who are you
    r'\b(who are you|who are u|who\'re you|what are you)\b':
        "🙏 I am a Bhagavad Gita AI Assistant, powered by neural-chat and enhanced with Retrieval-Augmented Generation (RAG). I have access to the sacred verses of the Bhagavad Gita and can provide insightful answers to your questions about yoga, dharma, karma, and the path to enlightenment.",
    
    # What can you do
    r'\b(what can you do|what do you do|what are your capabilities|what can i ask you)\b':
        "🙏 I can help you with:\n• Understanding the teachings of the Bhagavad Gita\n• Explaining concepts like yoga, dharma, and karma\n• Answering questions about Krishna's wisdom\n• Discussing the paths to liberation\n• Providing relevant verses for your questions\n\nJust ask me anything about the Gita!",
    
    # Bye/Goodbye
    r'\b(bye|goodbye|farewell|see you|take care|until next time|gotta go)\b':
        "🙏 Namaste! May the wisdom of the Bhagavad Gita guide you on your spiritual journey. Come back anytime you seek guidance. Hari Om!",
    
    # Good morning/afternoon/evening
    r'\b(good morning|good afternoon|good evening|good night)\b':
        "🙏 Greetings! I hope you're having a blessed day. I'm here to share the teachings of the Bhagavad Gita with you. What would you like to explore?",
}

# Predefined Gita answers for common questions (fast responses without LLM)
PREDEFINED_ANSWERS = {
    r'\b(what is yoga|define yoga|yoga meaning|explain yoga)\b':
        "📖 **Yoga** in the Bhagavad Gita refers to a disciplined practice aimed at connecting the individual soul (Atman) with the universal consciousness (Brahman).\n\nFrom Chapter 6, Verse 23:\n'That which is perceived to be yoga is said to be the steady intellect. One must practice it with determination and without doubt.'\n\nThere are several paths of yoga:\n• **Karma Yoga** - Yoga of action (performing duties without attachment)\n• **Bhakti Yoga** - Yoga of devotion (loving surrender to the divine)\n• **Jnana Yoga** - Yoga of knowledge (intellectual understanding of truth)\n• **Raja Yoga** - Yoga of meditation and mental discipline\n\nThe goal is to achieve Moksha (liberation) through steady practice.",
    
    r'\b(what is dharma|define dharma|dharma meaning|explain dharma)\b':
        "📖 **Dharma** is often translated as 'righteousness', 'duty', or 'cosmic law'. It is one of the fundamental concepts in Hindu philosophy.\n\nFrom Chapter 2, Verse 31:\n'Moreover, considering your duty as a warrior, you should not waver. For a warrior, there is nothing better than a righteous battle.'\n\nKey aspects of Dharma:\n• **Svadharma** - Your own specific duty based on your nature and position\n• **Moral Law** - Cosmic order and ethical principles\n• **Social Duty** - Responsibilities to family and society\n• **Spiritual Path** - The way to achieve spiritual liberation\n\nArjuna's entire dilemma in the Gita revolves around understanding and fulfilling his dharma despite his doubts.",
    
    r'\b(what is karma|define karma|karma meaning|explain karma)\b':
        "📖 **Karma** means 'action' in Sanskrit. It is the law of cause and effect - every action produces consequences.\n\nFrom Chapter 2, Verse 47:\n'You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions. Never consider yourself the cause of the results of your activities.'\n\nKey principles of Karma:\n• **Action & Reaction** - Every deed creates corresponding effects\n• **Not About Results** - Focus on duty, not on outcomes\n• **Karmic Debt** - Actions bind us through their consequences\n• **Liberation Through Knowledge** - Understanding karma leads to freedom\n• **Detachment** - Perform actions without attachment to results\n\nThe Gita teaches that by performing your duty without attachment to success or failure, you attain liberation.",
    
    r'\b(what is soul|atman|self|spirit)\b':
        "📖 **Atman** (the Soul) is the eternal, unchanging, indestructible essence within all beings.\n\nFrom Chapter 2, Verse 20:\n'For the soul, there is neither birth nor death at any time. He has not come into being, does not come into being, and will not come into being. He is unborn, eternal, permanent, and primeval. He is not destroyed when the body is destroyed.'\n\nCharacteristics of Atman:\n• **Eternal** - Exists beyond time\n• **Indestructible** - Cannot be harmed or destroyed\n• **Unchanging** - Remains constant throughout all changes\n• **Universal** - Same in all beings\n• **Divine** - Direct manifestation of the divine consciousness\n\nThe ultimate goal is to realize the Atman and unite with Brahman (universal consciousness).",
    
    r'\b(what is moksha|liberation|freedom|enlightenment|salvation)\b':
        "📖 **Moksha** is liberation from the cycle of birth and death (Samsara). It is the ultimate goal of spiritual life.\n\nFrom Chapter 8, Verse 15:\n'After attaining Me, the great souls, who are yogis in devotion, never return to this temporary world, which is full of miseries, because they have attained the highest perfection.'\n\nPaths to Moksha:\n• **Bhakti** - Through devotion and love for the divine\n• **Karma** - Through selfless action and duty\n• **Jnana** - Through knowledge and wisdom\n• **Meditation** - Through disciplined practice and concentration\n\nMoksha is characterized by:\n• Complete freedom from desire and ego\n• Eternal peace and bliss\n• Unity with the divine\n• End of the cycle of rebirth",
    
    r'\b(who is krishna|about krishna|krishna teaching)\b':
        "📖 **Krishna** is the divine incarnation of Lord Vishnu and the central figure of the Bhagavad Gita.\n\nIn the Gita, Krishna:\n• Acts as a charioteer and spiritual guide to Arjuna\n• Teaches the path of dharma and righteousness\n• Reveals the nature of the divine and the self\n• Explains multiple paths to liberation\n• Demonstrates how to live a spiritual life while performing worldly duties\n\nFrom Chapter 10, Verse 8:\n'I am the source of all spiritual and material worlds. Everything emanates from Me. The wise who perfectly engage in My devotional service and surrender their lives unto Me are certainly the best among all beings.'\n\nKrishna represents:\n• Divine wisdom and compassion\n• The ultimate source of all existence\n• The ideal guide and spiritual teacher",
    
    r'\b(what should i do|how to live|life purpose|right path)\b':
        "📖 The Bhagavad Gita teaches that the right way to live involves:\n\n**1. Understand Your Duty (Dharma)**\n• Fulfill your responsibilities based on your nature and position\n• Act according to your abilities and circumstances\n\n**2. Perform Actions Without Attachment**\nFrom Chapter 2, Verse 47:\n'You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions.'\n\n**3. Cultivate Inner Peace**\n• Practice meditation and self-discipline\n• Control your mind and desires\n• Develop equanimity in success and failure\n\n**4. Choose Your Path**\n• Karma Yoga - Through selfless action\n• Bhakti Yoga - Through devotion\n• Jnana Yoga - Through knowledge\n\n**5. Surrender to the Divine**\n• Trust in a higher power\n• Align your will with cosmic order\n• Seek spiritual growth above material gains",
    
    r'\b(what is wisdom|what is knowledge|jnana)\b':
        "📖 **Jnana** (Knowledge/Wisdom) is experiential understanding of the nature of reality and the self.\n\nFrom Chapter 4, Verse 33:\n'All sacrifices and penances, indeed all Vedic rituals, are insignificant in comparison to knowledge. All work culminates in knowledge.'\n\nTypes of Knowledge:\n• **Intellectual Knowledge** - Understanding through study and learning\n• **Experiential Knowledge** - Direct realization and understanding\n• **Spiritual Knowledge** - Understanding of the eternal truth and divine nature\n• **Self-Knowledge** - Realizing your true nature as Atman\n\nBenefits of True Knowledge:\n• Liberates from ignorance\n• Breaks the cycle of karma\n• Leads to Moksha\n• Brings lasting peace and happiness\n\nThe Gita emphasizes that true knowledge is not mere information, but transformative realization.",
    
    r'\b(what is bhakti|devotion|love of god)\b':
        "📖 **Bhakti** is devotion - the practice of cultivating love and surrender toward the divine.\n\nFrom Chapter 9, Verse 34:\n'Think of Me, become My devotee, worship Me and offer your homage unto Me. Thus you will come to Me without fail.'\n\nPillars of Bhakti:\n• **Love** - Pure, unconditional love for the divine\n• **Surrender** - Complete submission to divine will\n• **Faith** - Absolute trust in God\n• **Devotion** - Sincere practice and commitment\n\nBhakti can take many forms:\n• Singing devotional songs\n• Meditation on the divine\n• Service to others\n• Ritual worship\n• Constant remembrance\n\nFrom Chapter 12, Verse 6:\n'To those who are constantly devoted and who engage in My devotional service with love, I give the understanding by which they can come to Me.'",
    
    r'\b(what is detachment|non-attachment|vairagya)\b':
        "📖 **Detachment** (Vairagya) is freedom from excessive desires and attachment to worldly outcomes.\n\nFrom Chapter 2, Verse 55:\n'O Partha, when a man gives up all varieties of sense desire which arise from mental speculation, and finds satisfaction in the self alone, then he is said to be in pure consciousness.'\n\nDetachment means:\n• Performing your duty without clinging to results\n• Remaining unaffected by success or failure\n• Freedom from possessiveness\n• Internal peace regardless of external circumstances\n\nDetachment is NOT:\n• Apathy or indifference\n• Escapism or avoidance\n• Lack of effort\n• Emotional coldness\n\nTrue detachment is the freedom to act fully without being enslaved by desires, outcomes, or ego. It brings peace and liberation.",
    
    r'\b(how to meditate|meditation practice|dhyana)\b':
        "📖 The Bhagavad Gita provides guidance on meditation practice.\n\nFrom Chapter 6, Verse 25:\n'Gradually, by practice and detachment, one withdraws from all sense engagements and achieves perfect tranquility.'\n\n**Meditation Steps:**\n\n1. **Find a Quiet Place** - Sit in a peaceful, clean location\n2. **Assume a Posture** - Sit upright, cross-legged or on a chair\n3. **Control Your Breath** - Practice slow, steady breathing\n4. **Focus the Mind** - Concentrate on a mantra, the divine, or your breath\n5. **Withdraw Senses** - Gradually turn attention inward\n6. **Steady Practice** - Meditate regularly at the same time\n7. **Patience** - Allow the mind to gradually settle\n\nFrom Chapter 6, Verse 26:\n'Whenever and wherever the mind wanders, one must immediately withdraw it and bring it back under the control of the Self.'\n\nBenefits:\n• Inner peace and calm\n• Mental clarity\n• Spiritual insight\n• Liberation from thoughts"
}


def is_greeting(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check if text is a greeting and return predefined response
    
    Args:
        text: User input text
        
    Returns:
        Tuple of (is_greeting, response_text)
    """
    text_lower = text.strip().lower()
    
    # Check against greeting patterns
    for pattern, response in GREETINGS.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True, response
    
    return False, None


def get_predefined_answer(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check if there's a predefined answer for the question
    
    Args:
        text: User question
        
    Returns:
        Tuple of (has_predefined, answer_text)
    """
    text_lower = text.strip().lower()
    
    # Check against predefined answer patterns
    for pattern, answer in PREDEFINED_ANSWERS.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True, answer
    
    return False, None

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gemini_llm import get_gemini_client


def generate_answer(
    prompt: str,
    context: str = "",
    max_tokens: int = 256,
    temperature: float = 0.7,
    model_name: str = "gemini-pro",
    gemini_api_key: str = None
) -> str:
    """
    Generate answer using Gemini API
    
    Args:
        prompt: Input prompt for generation
        context: Retrieved context (for fallback)
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        model_name: Gemini model name
        gemini_api_key: Google Gemini API key
        
    Returns:
        Generated answer text
    """
    try:
        # Get Gemini client
        client = get_gemini_client(api_key=gemini_api_key)
        
        # Check if Gemini is available
        if not client.is_available():
            logger.warning("Gemini service not available, using fallback")
            return _fallback_answer(context)
        
        # Generate using Gemini API
        answer = client.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return answer.strip()
    
    except Exception as e:
        logger.error(f"Error in generate_answer: {e}")
        return _fallback_answer(context)


def _fallback_answer(context: str) -> str:
    """
    Fallback answer when LLM is unavailable
    Returns retrieved context as fallback
    """
    if not context or context.strip() == "":
        return """
        The LLM service is not available. 
        To use this feature, please ensure:
        1. Ollama or another local LLM service is running
        2. The service is accessible at the configured URL
        3. The model is properly installed
        """
    
    return f"""
    The Bhagavad Gita teaches:
    
    {context[:1000]}
    
    (Note: Detailed analysis unavailable - LLM service not connected)
    """


# backend/app/llm.py

def generate_answer(
    prompt: str,
    context: str = "",
    max_tokens: int = 256,
    temperature: float = 0.7,
    model_name: str = "gemini-1.0-pro",  # <--- FIX
    gemini_api_key: str = None
) -> str:
    """
    Generate Bhagavad Gita-specific answer using Gemini
    
    Args:
        question: User's question
        retrieved_context: Retrieved passages from Gita
        max_tokens: Max tokens for answer
        temperature: Sampling temperature
        gemini_api_key: Google Gemini API key
        
    Returns:
        Generated answer
    """
    
    # Bhagavad Gita specific prompt
    system_instruction = """You are a knowledgeable guide to the Bhagavad Gita. 
Answer the question accurately using the provided passages. 
Be concise, thoughtful, and respectful of the sacred text."""
    
    prompt = f"""{system_instruction}

Retrieved passages from the Bhagavad Gita:
{retrieved_context}

Question: {question}

Answer based on the provided passages:"""
    
    return generate_answer(
        prompt=prompt,
        context=retrieved_context,
        max_tokens=max_tokens,
        temperature=temperature,
        gemini_api_key=gemini_api_key
    )


def chat_with_gita(
    user_message: str,
    chat_history: list = None,
    retrieved_context: str = "",
    gemini_api_key: str = None,
    max_tokens: int = 512,
    temperature: float = 0.7
) -> str:
    """
    Chat mode with Bhagavad Gita context using Gemini
    
    Args:
        user_message: User's message
        chat_history: Previous chat messages
        retrieved_context: Gita passages for context
        gemini_api_key: Google Gemini API key
        max_tokens: Max tokens
        temperature: Sampling temperature
        
    Returns:
        Generated response
    """
    client = get_gemini_client(api_key=gemini_api_key)
    
    if not client.is_available():
        return _fallback_answer(retrieved_context)
    
    # Build message list
    messages = chat_history or []
    messages.append({"role": "user", "content": user_message})
    
    # Add system message with context
    system_message = {
        "role": "system",
        "content": f"""You are a knowledgeable guide to the Bhagavad Gita.
Use the following passages to answer questions accurately and thoughtfully.

Relevant passages:
{retrieved_context}

Be concise and respectful of the sacred teachings."""
    }
    
    # Insert system message at beginning
    messages_with_system = [system_message] + messages
    
    try:
        response = client.chat(
            messages=messages_with_system,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return _fallback_answer(retrieved_context)


def get_llm_status() -> dict:
    """Get status of LLM connection"""
    # Use Gemini client for status
    try:
        client = get_gemini_client()
        return {
            "llm_available": client.is_available(),
            "llm_api_url": None,
            "llm_model": getattr(client, 'model_name', getattr(client, 'model', None)),
            "available_models": client.list_models()
        }
    except Exception as e:
        logger.error(f"Error getting LLM status: {e}")
        return {
            "connected": False,
            "llm_api_url": None,
            "llm_model": None,
            "available_models": []
        }
