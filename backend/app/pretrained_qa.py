"""
Pretrained Q&A Database for Krishna RAG
50 Human Problems with Gita-Based Conversational Answers
These answers are optimized for quick responses without requiring Gemini API calls.
"""

import re
from typing import Tuple, Optional

# Comprehensive pretrained Q&A database with keywords and answers
PRETRAINED_ANSWERS = {
    # 1. Fear
    r'\b(fear|scared|afraid|fearless|overcome fear)\b': {
        'keyword': 'fear',
        'answer': '''🙏 Krishna says:

You're scared because your mind is holding onto too many outcomes. Try focusing only on what you can do right now. When you let go of the result, fear loosens its grip.

The Gita teaches that fear arises from attachment to outcomes. Focus on your duty and trust in the divine plan. Fear dissolves when you act with purpose and detach from results.'''
    },
    
    # 2. Anxiety
    r'\b(anxiety|anxious|stressed|worry|worried|overwhelming)\b': {
        'keyword': 'anxiety',
        'answer': '''🙏 Krishna says:

Your mind is jumping ahead. Bring it back to the present and do your duty step-by-step. Let life handle the results.

Anxiety comes from living in the future rather than the present moment. Practice focusing on the current moment and your immediate responsibilities. Perform your actions with dedication and release attachment to outcomes.'''
    },
    
    # 3. Anger
    r'\b(anger|angry|rage|furious|agitated|irritated)\b': {
        'keyword': 'anger',
        'answer': '''🙏 Krishna says:

Your anger is coming from something you're strongly attached to. Pause, breathe, and remind yourself that not everything needs to be controlled.

Anger arises from unmet expectations and desire for control. Remember that you can only control your efforts, not results. Practice equanimity and acceptance of situations beyond your control.'''
    },
    
    # 4. Frustration
    r'\b(frustration|frustrated|annoyance|impatient|agitation)\b': {
        'keyword': 'frustration',
        'answer': '''🙏 Krishna says:

Frustration means you're resisting the flow. Continue your effort, but release the expectation of how fast things must happen.

Frustration comes from wanting things to happen at your pace rather than at nature's pace. Trust the process, maintain steady effort, and let go of rigid timelines. All things unfold in their proper time.'''
    },
    
    # 5. Sadness
    r'\b(sadness|sad|sorrowful|unhappy|melancholy|depressed)\b': {
        'keyword': 'sadness',
        'answer': '''🙏 Krishna says:

This pain feels big because you're focusing on what has changed. Shift your attention to what is still stable and meaningful inside you.

Sadness arises from attachment and loss. Remember that the eternal essence within you and others remains unchanged. Find stability in what is permanent rather than in what changes. Gratitude for what remains can ease sorrow.'''
    },
    
    # 6. Grief
    r'\b(grief|grieving|loss|lost loved one|mourning|bereavement)\b': {
        'keyword': 'grief',
        'answer': '''🙏 Krishna says:

Your loss is real — but remember, the essence of the person you lost hasn't disappeared. Allow yourself to feel, but also trust that their soul continues its journey.

From the Bhagavad Gita: "As the embodied soul continuously passes in this body from childhood to youth to old age, the soul similarly passes into another body at the time of death."

The body changes, but the eternal soul continues. Honor their memory while trusting in their spiritual continuation.'''
    },
    
    # 7. Loneliness
    r'\b(loneliness|lonely|alone|isolated|solitude|disconnected)\b': {
        'keyword': 'loneliness',
        'answer': '''🙏 Krishna says:

You feel alone because you're disconnected from yourself. Spend time in silence; that inner presence will remind you that you're never truly alone.

True companionship begins with understanding yourself. The divine presence exists within you and all beings. Practice meditation, self-reflection, and connection with your inner self—loneliness transforms into peaceful solitude.'''
    },
    
    # 8. Depression
    r'\b(depression|depressed|hopelessness|despair|darkness)\b': {
        'keyword': 'depression',
        'answer': '''🙏 Krishna says:

Your mind is stuck in dark loops. Start with small meaningful actions — even helping someone — even small, positive actions break the cycle and lift the heaviness gradually.

Depression comes from inaction and self-focus. Begin moving—even small steps. Serve others, engage in meaningful work, and remember that this state is temporary. Action, connection, and purpose are powerful antidotes.'''
    },
    
    # 9. Hopelessness
    r'\b(hopeless|hopelessness|no hope|lost all hope|giving up)\b': {
        'keyword': 'hopelessness',
        'answer': '''🙏 Krishna says:

Hope returns when you take one honest step forward. Don't think of the whole journey; just focus on the next right action.

Chapter 2, Verse 47 teaches: "You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions."

Focus on what's in your control—your effort, your character, your daily actions. One step at a time builds the path forward.'''
    },
    
    # 10. Despair
    r'\b(despair|despairing|desperate|helpless|lost)\b': {
        'keyword': 'despair',
        'answer': '''🙏 Krishna says:

You feel like giving up because you're carrying everything alone. Share the load internally — tell yourself, "I'm doing my best, the rest isn't in my hands."

Despair comes from feeling solely responsible for outcomes. Recognize your human limitations. Do your duty with sincerity and trust in a larger order. Surrender the burden of needing to control everything.'''
    },
    
    # 11. Jealousy
    r'\b(jealousy|jealous|envy|envious|comparison)\b': {
        'keyword': 'jealousy',
        'answer': '''🙏 Krishna says:

Jealousy fades when you appreciate your own path. What others have is their journey; yours is uniquely meant for you.

Each soul has its own dharma and purpose. Comparing yourself to others is like comparing different musical instruments for beauty—each has its own excellence. Focus on your unique talents and contributions.'''
    },
    
    # 12. Envy
    r'\b(envy|envious|wishing had|why them|why not me)\b': {
        'keyword': 'envy',
        'answer': '''🙏 Krishna says:

Focus on growth, not comparison. The more you invest in your strengths, the less envy you'll feel.

Envy is the enemy of progress. Channel that energy into developing your own unique gifts and abilities. Celebrate others' success while committed to your own growth—this transforms envy into inspiration.'''
    },
    
    # 13. Greed
    r'\b(greed|greedy|wanting more|insatiable|never enough)\b': {
        'keyword': 'greed',
        'answer': '''🙏 Krishna says:

Greed arises when inner fulfillment is low. Try being content with what you have right now — even briefly — and you'll feel lighter.

The root of greed is seeking external things to fill internal emptiness. Practice gratitude for what you have. Understand that accumulation never brings satisfaction—only inner peace does. Give generously and experience the freedom.'''
    },
    
    # 14. Lust
    r'\b(lust|lustful|temptation|desire|passion)\b': {
        'keyword': 'lust',
        'answer': '''🙏 Krishna says:

Your mind is pulling you toward temporary pleasure. When you start feeding your deeper purpose, this urge naturally becomes weaker.

Desires for temporary pleasures fade when you engage in meaningful pursuits. Direct your energy toward spiritual growth, creative work, and service. The satisfaction from purpose far exceeds momentary gratification.'''
    },
    
    # 15. Attachment
    r'\b(attachment|attached|clinging|holding on|let go)\b': {
        'keyword': 'attachment',
        'answer': '''🙏 Krishna says:

You're holding too tightly. Care deeply, but don't cling — things change, and you don't have to suffer because of it.

Attachment creates suffering when things change. Love freely but hold lightly. Understand that nothing is permanent except the eternal soul. Perform your duties with full heart but without grasping for specific outcomes.'''
    },
    
    # 16. Guilt
    r'\b(guilt|guilty|ashamed|remorse|regret action)\b': {
        'keyword': 'guilt',
        'answer': '''🙏 Krishna says:

You've done something you regret — but guilt won't fix it. Correct yourself, learn, and move forward. Don't stay stuck.

From Bhagavad Gita wisdom: guilt is useful only if it teaches and transforms you. Acknowledge the mistake, make amends if possible, extract the lesson, and release the burden. Self-punishment serves no one.'''
    },
    
    # 17. Regret
    r'\b(regret|regretting|wish|should have|if only)\b': {
        'keyword': 'regret',
        'answer': '''🙏 Krishna says:

What happened is done. What matters now is how you act today. Use regret as a teacher, not a jailer.

The past cannot be changed, but your future can. Extract wisdom from regret—what does it teach you about your values and choices? Then release it and focus your creative energy on the present and future.'''
    },
    
    # 18. Shame
    r'\b(shame|ashamed|shameful|disgraced|humiliated)\b': {
        'keyword': 'shame',
        'answer': '''🙏 Krishna says:

You're identifying with old mistakes. Remember, the real you is much bigger than anything you've done.

Shame comes from total identification with past actions. Remember that you are not your mistakes. You are a evolving, learning being. Every moment is an opportunity to align with your highest self. Release the old identity and step into who you're becoming.'''
    },
    
    # 19. Insecurity
    r'\b(insecurity|insecure|inadequate|not good enough|unworthy)\b': {
        'keyword': 'insecurity',
        'answer': '''🙏 Krishna says:

You're relying too much on external validation. Shift your confidence to who you are inside, not how others see you.

Insecurity stems from seeking your worth in others' opinions. Your value is intrinsic, not dependent on external approval. Develop trust in your inner wisdom, your unique gifts, and your divine essence. Your worth is inherent and unchanging.'''
    },
    
    # 20. Self-doubt
    r'\b(self doubt|doubt myself|doubt abilities|not confident)\b': {
        'keyword': 'self-doubt',
        'answer': '''🙏 Krishna says:

It's okay not to have answers. Ask for guidance where needed, reflect calmly, and trust your inner wisdom to grow.

Self-doubt is normal—it signals growth opportunity. Distinguish between healthy questioning and paralyzing fear. Take action despite doubt, learn from results, and gradually build confidence. Trust develops through experience and reflection.'''
    },
    
    # 21. Spiritual Doubt
    r'\b(spiritual doubt|doubt faith|lost faith|belief crisis)\b': {
        'keyword': 'spiritual doubt',
        'answer': '''🙏 Krishna says:

Doubt means you're thinking. Keep asking questions — genuine seeking will bring clarity over time.

Spiritual doubt is not weakness—it's the beginning of genuine seeking. The Gita welcomes questions. Sincere inquiry leads to deeper understanding. Practice spiritual disciplines, study, meditation, and service while maintaining openness to truth.'''
    },
    
    # 22. Confusion
    r'\b(confusion|confused|unclear|lost|don\'t know)\b': {
        'keyword': 'confusion',
        'answer': '''🙏 Krishna says:

Stop overanalyzing. Sit quietly, breathe, and ask yourself: "What is my responsibility right now?" Act on that.

Confusion comes from excessive analysis and disconnection from intuition. Quiet your mind through meditation. Connect with your inner knowing. Then take the action in front of you. Clarity often comes through action, not just thinking.'''
    },
    
    # 23. Indecision
    r'\b(indecision|can\'t decide|unable to choose|stuck)\b': {
        'keyword': 'indecision',
        'answer': '''🙏 Krishna says:

Pick the option that aligns with your values, not your fears. Once you choose, commit.

Endless deliberation comes from trying to guarantee perfect outcomes. That's impossible. Make decisions based on your values and what feels right. Then commit fully to that path. Growth comes through commitment and learning from choices.'''
    },
    
    # 24. Pride/Ego
    r'\b(pride|ego|arrogance|superiority|proud)\b': {
        'keyword': 'pride',
        'answer': '''🙏 Krishna says:

You feel superior because you're forgetting that everyone is shaped by the same divine force. Stay grounded.

Pride blinds us to our limitations and others' worth. Remember that all beings share the same divine essence. Your gifts are not yours alone—they're expressions of universal consciousness. Humility opens the heart to genuine wisdom.'''
    },
    
    # 25. Hatred
    r'\b(hatred|hate|despise|hostile|enmity)\b': {
        'keyword': 'hatred',
        'answer': '''🙏 Krishna says:

Hate is poisoning you, not them. Release it — not for them, but for your own peace.

Hatred is a poison you drink, expecting the other person to suffer. It harms only you. The spiritual path teaches seeing the divine essence in all beings, even those who've wronged you. Forgiveness and compassion free you from hatred's chains.'''
    },
    
    # 26. Bitterness
    r'\b(bitterness|bitter|resentment|vindictive|hold grudge)\b': {
        'keyword': 'bitterness',
        'answer': '''🙏 Krishna says:

You're replaying old wounds. Heal by accepting that the past can't be changed, but your future can.

Bitterness keeps you trapped in past harm. Healing comes through acceptance, understanding, and moving forward with wisdom gained. Don't let old wounds define your future. Each moment offers the opportunity to choose differently.'''
    },
    
    # 27. Contempt
    r'\b(contempt|contemptuous|disdain|look down|belittle)\b': {
        'keyword': 'contempt',
        'answer': '''🙏 Krishna says:

When you judge others, your heart becomes small. Expand your view and remember you don't know their battles.

Contempt arises from incomplete understanding. Every person has their own struggles, karma, and journey. Practicing empathy and remembering that all beings deserve respect and compassion expands your spiritual understanding.'''
    },
    
    # 28. Selfishness
    r'\b(selfish|selfishness|self centered|greedy|only think)\b': {
        'keyword': 'selfishness',
        'answer': '''🙏 Krishna says:

Start giving a little — even your time or attention. Service opens the heart naturally.

Selfishness comes from identifying only with the individual ego-self. Service to others reveals our interconnection and opens the heart. Begin with small acts of generosity and kindness—these naturally expand your consciousness and reduce self-centeredness.'''
    },
    
    # 29. Materialism
    r'\b(materialism|materialistic|money worship|consumerism|greed)\b': {
        'keyword': 'materialism',
        'answer': '''🙏 Krishna says:

You're chasing things hoping they'll fulfill you. Try balancing outer goals with inner growth — that's where lasting peace comes from.

Material pursuits have their place, but they never bring lasting fulfillment. Balance worldly responsibilities with inner development. Invest equally in your spiritual growth, relationships, and character as you do in material accumulation. True wealth is inner peace.'''
    },
    
    # 30. Restlessness
    r'\b(restlessness|restless|can\'t sit still|hyperactive|agitated)\b': {
        'keyword': 'restlessness',
        'answer': '''🙏 Krishna says:

Your mind is running too fast. Slow down with breath, routine, and discipline.

Restlessness comes from a scattered, uncontrolled mind. Practice meditation, deep breathing, and regular routines. Establish discipline in your daily life. Gradually, the mind settles and inner calm emerges. Consistency is key.'''
    },
    
    # 31. Impatience
    r'\b(impatience|impatient|hurried|rush|wanting now)\b': {
        'keyword': 'impatience',
        'answer': '''🙏 Krishna says:

Life unfolds at its pace, not yours. Stay committed but patient — results take time.

Impatience comes from believing your timeline should be nature's timeline. True mastery and lasting results require time. Stay committed to your practice, trust the process, and release the demand for immediate results. Patience is a spiritual practice.'''
    },
    
    # 32. Boredom
    r'\b(boredom|bored|boring|nothing interesting|dull)\b': {
        'keyword': 'boredom',
        'answer': '''🙏 Krishna says:

Boredom means you're disconnected from purpose. Engage in something meaningful, even small.

Boredom arises from disconnection from purpose and passion. Identify what genuinely interests you and brings meaning. Even small acts performed with full attention and purpose banish boredom. Connect with what matters to you.'''
    },
    
    # 33. Apathy
    r'\b(apathy|apathetic|don\'t care|unmotivated|listless)\b': {
        'keyword': 'apathy',
        'answer': '''🙏 Krishna says:

You've lost emotional energy. Reignite it with something that matters to you or someone you care about.

Apathy comes from disconnection and emotional numbing. Begin with small actions toward something meaningful—helping someone, creating something, learning something new. Engagement gradually reignites your emotional and spiritual energy.'''
    },
    
    # 34. Overthinking
    r'\b(overthinking|overthink|too much thinking|analysis paralysis)\b': {
        'keyword': 'overthinking',
        'answer': '''🙏 Krishna says:

You're trying to control outcomes with thought. Come back to the present and take one simple action.

The mind's job is not to solve everything—it's to inform action. Excessive thinking disconnects you from intuition and present action. Practice mindfulness, take action based on your best understanding, and learn from results rather than endless mental loops.'''
    },
    
    # 35. Obsession
    r'\b(obsession|obsessed|fixated|can\'t stop thinking|consumed)\b': {
        'keyword': 'obsession',
        'answer': '''🙏 Krishna says:

Your mind is fixating. Redirect that intensity into something constructive or spiritual.

Obsessive thoughts arise from emotional hooks or unresolved issues. Redirect your mental energy toward constructive pursuits, spiritual practice, or service. The intensity itself is valuable—it's the object of focus that needs adjustment.'''
    },
    
    # 36. Laziness
    r'\b(laziness|lazy|procrastination|unmotivated|no energy)\b': {
        'keyword': 'laziness',
        'answer': '''🙏 Krishna says:

Start moving — motivation comes after action, not before. Begin with something small.

Laziness comes from inaction, not lack of motivation. Motivation follows action, not the reverse. Take one small step today, then another tomorrow. Momentum builds gradually. Small consistent actions are the antidote to inertia.'''
    },
    
    # 37. Ignorance
    r'\b(ignorance|ignorant|don\'t know|uneducated|unaware)\b': {
        'keyword': 'ignorance',
        'answer': '''🙏 Krishna says:

Don't judge yourself for not knowing — learn, grow, and stay open. Awareness builds power.

Ignorance is simply lack of awareness—everyone starts there. The Gita celebrates genuine seeking and learning. Stay humble and open to knowledge. Each question answered opens doors to deeper understanding. Pursue knowledge with sincere intent.'''
    },
    
    # 38. Emptiness
    r'\b(emptiness|empty|void|hollow|meaningless)\b': {
        'keyword': 'emptiness',
        'answer': '''🙏 Krishna says:

You feel a void because you're disconnected from your inner self. Spend time in silence, gratitude, or meditation.

Inner emptiness comes from disconnection from your true nature. Meditation reveals the fullness already within you. Practice silence, gratitude, and connection with your essence. The void transforms into presence when you turn awareness inward.'''
    },
    
    # 39. Lack of Purpose
    r'\b(lack of purpose|no purpose|purposeless|no meaning|directionless)\b': {
        'keyword': 'lack of purpose',
        'answer': '''🙏 Krishna says:

Your purpose becomes clear when you do what is right in front of you sincerely. Purpose grows from action, not thought.

Purpose isn't found through endless searching—it emerges through engaged action. Focus on your immediate responsibilities and do them with full attention and sincerity. As you work, your deeper purpose gradually reveals itself.'''
    },
    
    # 40. Unforgiveness
    r'\b(unforgiveness|can\'t forgive|won\'t forgive|holding grudge|can\'t let go)\b': {
        'keyword': 'unforgiveness',
        'answer': '''🙏 Krishna says:

Not forgiving keeps you chained to the past. Release it to free your own mind.

Unforgiveness is like drinking poison and expecting the other person to suffer. It harms only you. Forgiveness doesn't mean condoning harm—it means releasing the emotional charge. Forgive for your own freedom and peace, not for them.'''
    },
    
    # 41. Judgmental Attitude
    r'\b(judgmental|judging|critical|judgement|condemnation)\b': {
        'keyword': 'judgmental',
        'answer': '''🙏 Krishna says:

Step back and try to see people as fellow travelers. Everyone is doing the best they can with what they know.

Judgment blinds you to others' circumstances and struggles. Every person is shaped by their karma and conditioning. Cultivate compassion by remembering that all beings deserve understanding. Less judgment opens your heart to wisdom.'''
    },
    
    # 42. Discontentment
    r'\b(discontentment|discontent|dissatisfied|never satisfied|unhappy)\b': {
        'keyword': 'discontentment',
        'answer': '''🙏 Krishna says:

Shift from "what's missing" to "what's present." Gratitude changes everything.

Discontentment comes from constantly focusing on what's lacking. Gratitude for what exists shifts your emotional baseline. Practice noting three things you're grateful for daily. This simple practice transforms your entire experience of life.'''
    },
    
    # 43. Fear of Death
    r'\b(fear of death|death anxiety|afraid of dying|mortality)\b': {
        'keyword': 'fear of death',
        'answer': '''🙏 Krishna says:

The body ends, but the soul continues. Knowing this makes life lighter and death less frightening.

From Bhagavad Gita Chapter 2, Verse 20: "For the soul there is neither birth nor death... it is eternal, immortal, and ageless."

Understanding your true eternal nature—beyond the body—transforms fear of death into peaceful acceptance. The soul is imperishable; only bodies change.'''
    },
    
    # 44. Fear of Failure
    r'\b(fear of failure|afraid to fail|failure anxiety|scared of failing)\b': {
        'keyword': 'fear of failure',
        'answer': '''🙏 Krishna says:

Failure is just part of the process. Focus on doing your best — the rest isn't yours to control.

From Bhagavad Gita Chapter 2, Verse 47: "You have the right to perform your actions, but you have no right to the results of your actions."

Failure and success are both part of life's journey. Focus on your effort and character. Results will follow naturally. Fear of failure paralyzes—action despite fear builds strength and wisdom.'''
    },
    
    # 45. Escapism
    r'\b(escapism|escape|avoidance|avoid|running away)\b': {
        'keyword': 'escapism',
        'answer': '''🙏 Krishna says:

Running away only delays the problem. Face the situation with courage, one step at a time.

Escapism—through substances, distraction, or avoidance—only postpones pain and creates more problems. Courageous facing of challenges, one step at a time, resolves them. The discomfort of facing is temporary; the freedom afterward is lasting.'''
    },
    
    # 46. Attachment to Outcomes
    r'\b(attached to outcomes|outcome focus|results obsession|must succeed)\b': {
        'keyword': 'attachment to outcomes',
        'answer': '''🙏 Krishna says:

Do your work with sincerity, but let go of the obsession with results. That's where peace begins.

Chapter 2, Verse 47 of the Gita teaches: "Perform your duty, but relinquish the fruits thereof."

Peace comes from performing your duty excellently while accepting whatever results emerge. You control your effort and character—not outcomes. This understanding transforms anxiety into peaceful action.'''
    },
    
    # 47. Identifying Only with the Body
    r'\b(body identification|just body|physical|material only|no soul)\b': {
        'keyword': 'body identification',
        'answer': '''🙏 Krishna says:

You're more than this body. When you connect with your inner self, fear and insecurity fade.

You are not just this temporary body—you are the eternal consciousness within. This understanding liberates you from fear, shame, and insecurity. Your true nature is infinite and eternal. Connect with this reality through meditation and self-reflection.'''
    },
    
    # 48. Feeling Spiritually Disconnected
    r'\b(spiritually disconnected|lost connection|spiritual emptiness|no connection)\b': {
        'keyword': 'spiritual disconnection',
        'answer': '''🙏 Krishna says:

Connection returns with attention. Sit quietly, breathe, speak from your heart — the link will come back.

Spiritual disconnection is temporary—it returns when you turn your attention inward. Regular meditation, sincere inquiry, and speaking truth from your heart restore the connection. The divine presence is always there; it's your awareness that wavers.'''
    },
    
    # 49. Fear of Criticism
    r'\b(fear of criticism|afraid criticism|can\'t handle criticism|what people think)\b': {
        'keyword': 'fear of criticism',
        'answer': '''🙏 Krishna says:

People's opinions change constantly. Trust your intention and act with integrity — that's enough.

Fear of criticism comes from making others' opinions your internal compass. People's judgments are constantly shifting and often reflect their own issues. Your only responsibility is acting with integrity and good intention. That is enough.'''
    },
    
    # 50. Ingratitude
    r'\b(ingratitude|ungrateful|thankless|taking for granted|no appreciation)\b': {
        'keyword': 'ingratitude',
        'answer': '''🙏 Krishna says:

Pause and look at what is working in your life — health, breath, people, moments. Gratitude instantly uplifts the heart.

Ingratitude blinds you to life's blessings. Pause daily to notice what's working—your health, breath, relationships, moments of beauty. Gratitude is the fastest path to peace and joy. It shifts your entire experience from scarcity to abundance.'''
    },
}


def get_pretrained_answer(question: str) -> Tuple[bool, Optional[str]]:
    """
    Check if question matches any pretrained keywords and return answer
    
    Args:
        question: User's question
        
    Returns:
        Tuple of (has_answer, answer_text)
    """
    if not question:
        return False, None
    
    question_lower = question.strip().lower()
    
    # Iterate through all keyword patterns
    for pattern, qa_data in PRETRAINED_ANSWERS.items():
        if re.search(pattern, question_lower, re.IGNORECASE):
            return True, qa_data['answer']
    
    return False, None


def get_all_keywords() -> list:
    """Get list of all available keywords for documentation"""
    keywords = []
    for pattern, qa_data in PRETRAINED_ANSWERS.items():
        keywords.append(qa_data['keyword'])
    return sorted(set(keywords))


# For easy reference - mapping of topics
TOPICS_REFERENCE = {
    'emotions': ['fear', 'anxiety', 'anger', 'frustration', 'sadness'],
    'loss_and_grief': ['grief', 'loneliness', 'depression', 'hopelessness', 'despair'],
    'negative_emotions': ['jealousy', 'envy', 'greed', 'lust', 'attachment'],
    'guilt_and_shame': ['guilt', 'regret', 'shame', 'insecurity', 'self-doubt'],
    'spiritual': ['spiritual doubt', 'confusion', 'indecision', 'pride', 'hatred'],
    'darkness_and_pain': ['bitterness', 'contempt', 'selfishness', 'materialism'],
    'mental_states': ['restlessness', 'impatience', 'boredom', 'apathy', 'overthinking'],
    'challenges': ['obsession', 'laziness', 'ignorance', 'emptiness', 'lack of purpose'],
    'relationships': ['unforgiveness', 'judgmental', 'discontentment', 'fear of death'],
    'failures': ['fear of failure', 'escapism', 'attachment to outcomes', 'body identification'],
    'final_lessons': ['spiritual disconnection', 'fear of criticism', 'ingratitude'],
}
