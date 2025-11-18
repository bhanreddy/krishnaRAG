"""
Test Examples for Pretrained Q&A System
Quick reference for testing the 50 human problems database
"""

# Test Cases - One from each category

FEAR_EXAMPLE = "I am very scared and anxious about my future"
# Expected: Krishna says about letting go of outcomes and focusing on present action

ANXIETY_EXAMPLE = "How do I deal with my constant anxiety?"
# Expected: Krishna says about bringing mind back to present and doing duty step-by-step

ANGER_EXAMPLE = "I feel so angry at people around me"
# Expected: Krishna says about attachment and acceptance

FRUSTRATION_EXAMPLE = "Everything is frustrating me lately"
# Expected: Krishna says about releasing expectation of pace

SADNESS_EXAMPLE = "I feel deep sadness about recent changes in my life"
# Expected: Krishna says about shifting attention to what is stable

GRIEF_EXAMPLE = "How do I cope with losing my loved one?"
# Expected: Krishna says about soul's continuation after death

LONELINESS_EXAMPLE = "I feel so lonely and isolated"
# Expected: Krishna says about connecting with inner self

DEPRESSION_EXAMPLE = "I'm feeling depressed with dark thoughts"
# Expected: Krishna says about taking meaningful small actions

HOPELESSNESS_EXAMPLE = "I've lost all hope, what's the point?"
# Expected: Krishna says about taking one honest step forward

DESPAIR_EXAMPLE = "I feel completely helpless and desperate"
# Expected: Krishna says about sharing burden internally

JEALOUSY_EXAMPLE = "I'm jealous of what others have"
# Expected: Krishna says about appreciating your own path

ENVY_EXAMPLE = "Why do they have everything and I have nothing?"
# Expected: Krishna says about focusing on your own growth

GREED_EXAMPLE = "I want more and more but never feel satisfied"
# Expected: Krishna says about cultivating inner fulfillment

LUST_EXAMPLE = "I struggle with overwhelming desires"
# Expected: Krishna says about feeding deeper purpose

ATTACHMENT_EXAMPLE = "I can't let go of this relationship"
# Expected: Krishna says about holding things lightly

GUILT_EXAMPLE = "I feel guilty about something I did"
# Expected: Krishna says about learning and moving forward

REGRET_EXAMPLE = "I regret my past decisions so much"
# Expected: Krishna says about using regret as a teacher

SHAME_EXAMPLE = "I feel ashamed of my mistakes"
# Expected: Krishna says about not identifying with past

INSECURITY_EXAMPLE = "I feel so inadequate and not good enough"
# Expected: Krishna says about trusting inner worth

SELF_DOUBT_EXAMPLE = "I doubt myself and my abilities"
# Expected: Krishna says about asking for guidance and trusting growth

SPIRITUAL_DOUBT_EXAMPLE = "I'm doubting my spiritual beliefs"
# Expected: Krishna says about genuine seeking leading to clarity

CONFUSION_EXAMPLE = "I'm confused about what to do"
# Expected: Krishna says about quieting mind and acting on responsibility

INDECISION_EXAMPLE = "I can't decide between two options"
# Expected: Krishna says about choosing based on values and committing

PRIDE_EXAMPLE = "I feel superior to those around me"
# Expected: Krishna says about remembering divine essence in all

HATRED_EXAMPLE = "I hate this person so much"
# Expected: Krishna says about releasing hate for your own peace

BITTERNESS_EXAMPLE = "I feel bitter about past wounds"
# Expected: Krishna says about accepting past and shaping future

CONTEMPT_EXAMPLE = "I have contempt for people who don't understand me"
# Expected: Krishna says about cultivating empathy

SELFISHNESS_EXAMPLE = "I'm too self-centered and don't think of others"
# Expected: Krishna says about starting with small acts of service

MATERIALISM_EXAMPLE = "I keep chasing more money and possessions"
# Expected: Krishna says about balancing outer and inner growth

RESTLESSNESS_EXAMPLE = "I can't sit still, my mind races constantly"
# Expected: Krishna says about slowing down with breath and discipline

IMPATIENCE_EXAMPLE = "I want results now, can't wait"
# Expected: Krishna says about staying committed but patient

BOREDOM_EXAMPLE = "Everything seems boring and uninteresting"
# Expected: Krishna says about connecting with meaningful purpose

APATHY_EXAMPLE = "I don't care about anything anymore"
# Expected: Krishna says about reigniting with something meaningful

OVERTHINKING_EXAMPLE = "I overthink everything and can't take action"
# Expected: Krishna says about coming back to present and acting

OBSESSION_EXAMPLE = "I'm obsessed with this thought"
# Expected: Krishna says about redirecting intensity constructively

LAZINESS_EXAMPLE = "I'm too lazy to do anything"
# Expected: Krishna says about starting to move, motivation follows

IGNORANCE_EXAMPLE = "I don't know anything, I feel ignorant"
# Expected: Krishna says about learning and staying open

EMPTINESS_EXAMPLE = "I feel empty inside, like a void"
# Expected: Krishna says about connecting with inner self

PURPOSE_EXAMPLE = "I don't have any purpose in life"
# Expected: Krishna says about purpose emerging through action

UNFORGIVENESS_EXAMPLE = "I can't forgive what they did"
# Expected: Krishna says about forgiving for your freedom

JUDGMENT_EXAMPLE = "I judge people too harshly"
# Expected: Krishna says about seeing all as fellow travelers

DISCONTENTMENT_EXAMPLE = "I'm never satisfied, always wanting more"
# Expected: Krishna says about practicing gratitude

DEATH_FEAR_EXAMPLE = "I'm afraid of death and dying"
# Expected: Krishna says about eternal soul continuing

FAILURE_FEAR_EXAMPLE = "I'm too scared of failing"
# Expected: Krishna says about focusing on effort, not results

ESCAPISM_EXAMPLE = "I want to escape from my problems"
# Expected: Krishna says about facing challenges with courage

OUTCOME_ATTACHMENT_EXAMPLE = "I'm obsessed with getting specific results"
# Expected: Krishna says about performing duty and releasing results

BODY_IDENTIFICATION_EXAMPLE = "I'm just this body, nothing more"
# Expected: Krishna says about connecting with eternal self

SPIRITUAL_DISCONNECTION_EXAMPLE = "I feel disconnected from the divine"
# Expected: Krishna says about meditation and turning inward

CRITICISM_FEAR_EXAMPLE = "I'm afraid of what people will say about me"
# Expected: Krishna says about trusting your integrity

INGRATITUDE_EXAMPLE = "I'm ungrateful for what I have"
# Expected: Krishna says about counting blessings and gratitude


# Python Testing Script

def test_pretrained_answers():
    """Test all 50 keywords"""
    from app.pretrained_qa import get_pretrained_answer
    
    test_questions = [
        FEAR_EXAMPLE,
        ANXIETY_EXAMPLE,
        ANGER_EXAMPLE,
        FRUSTRATION_EXAMPLE,
        SADNESS_EXAMPLE,
        GRIEF_EXAMPLE,
        LONELINESS_EXAMPLE,
        DEPRESSION_EXAMPLE,
        HOPELESSNESS_EXAMPLE,
        DESPAIR_EXAMPLE,
        JEALOUSY_EXAMPLE,
        ENVY_EXAMPLE,
        GREED_EXAMPLE,
        LUST_EXAMPLE,
        ATTACHMENT_EXAMPLE,
        GUILT_EXAMPLE,
        REGRET_EXAMPLE,
        SHAME_EXAMPLE,
        INSECURITY_EXAMPLE,
        SELF_DOUBT_EXAMPLE,
        SPIRITUAL_DOUBT_EXAMPLE,
        CONFUSION_EXAMPLE,
        INDECISION_EXAMPLE,
        PRIDE_EXAMPLE,
        HATRED_EXAMPLE,
        BITTERNESS_EXAMPLE,
        CONTEMPT_EXAMPLE,
        SELFISHNESS_EXAMPLE,
        MATERIALISM_EXAMPLE,
        RESTLESSNESS_EXAMPLE,
        IMPATIENCE_EXAMPLE,
        BOREDOM_EXAMPLE,
        APATHY_EXAMPLE,
        OVERTHINKING_EXAMPLE,
        OBSESSION_EXAMPLE,
        LAZINESS_EXAMPLE,
        IGNORANCE_EXAMPLE,
        EMPTINESS_EXAMPLE,
        PURPOSE_EXAMPLE,
        UNFORGIVENESS_EXAMPLE,
        JUDGMENT_EXAMPLE,
        DISCONTENTMENT_EXAMPLE,
        DEATH_FEAR_EXAMPLE,
        FAILURE_FEAR_EXAMPLE,
        ESCAPISM_EXAMPLE,
        OUTCOME_ATTACHMENT_EXAMPLE,
        BODY_IDENTIFICATION_EXAMPLE,
        SPIRITUAL_DISCONNECTION_EXAMPLE,
        CRITICISM_FEAR_EXAMPLE,
        INGRATITUDE_EXAMPLE,
    ]
    
    passed = 0
    failed = 0
    
    for question in test_questions:
        has_answer, answer = get_pretrained_answer(question)
        if has_answer and answer:
            passed += 1
            print(f"✓ PASS: {question[:50]}...")
        else:
            failed += 1
            print(f"✗ FAIL: {question[:50]}...")
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"Success Rate: {passed*100/(passed+failed):.1f}%")
    return passed, failed


# Testing via curl

CURL_TESTS = """
# Test 1: Fear
curl -X POST http://localhost:8000/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "I am very scared and anxious about my future",
    "top_k": 3,
    "temperature": 0.7,
    "max_tokens": 512
  }'

# Test 2: Anxiety  
curl -X POST http://localhost:8000/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "How do I deal with my constant anxiety?",
    "top_k": 3,
    "temperature": 0.7,
    "max_tokens": 512
  }'

# Test 3: Grief
curl -X POST http://localhost:8000/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "How do I cope with losing my loved one?",
    "top_k": 3,
    "temperature": 0.7,
    "max_tokens": 512
  }'

# Test 4: Judgment
curl -X POST http://localhost:8000/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "I judge people too harshly for their mistakes",
    "top_k": 3,
    "temperature": 0.7,
    "max_tokens": 512
  }'

# Test 5: Gratitude
curl -X POST http://localhost:8000/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "I am ungrateful for what I have",
    "top_k": 3,
    "temperature": 0.7,
    "max_tokens": 512
  }'
"""

# Expected Response Format

EXPECTED_RESPONSE = {
    "question": "I am very scared and anxious about my future",
    "answer": "🙏 Krishna says:\n\nYou're scared because your mind is holding onto too many outcomes...",
    "retrieved": [],
    "passage_count": 0
}

# Notes: Retrieved will be empty for pretrained answers, only filled when using RAG+Gemini

print(__doc__)
