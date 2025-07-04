# cbt_content.py

# This dictionary holds all the content for your CBT lessons and quizzes.
# Each key is the lesson title, and its value is a dictionary containing
# the lesson text and a list of quiz questions.

content_data = {
    "Introduction to CBT": {
        "title": "Understanding Cognitive Behavioral Therapy",
        "text": """Cognitive Behavioral Therapy (CBT) is a common type of talk therapy (psychotherapy). You work with a mental health counselor (therapist or psychologist) in a structured way, attending a limited number of sessions. CBT helps you become aware of inaccurate or negative thinking so you can view challenging situations more clearly and respond to them in a more effective way.

CBT is an effective tool to help individuals learn how to manage stressful life situations. In many ways, CBT is about training your brain to think more positively and constructively, which in turn can lead to more positive emotions and behaviors. It's often used for a wide range of problems including depression, anxiety disorders, phobias, PTSD, and eating disorders.

Key principles of CBT include:
1. Identifying troubling situations or conditions in your life.
2. Becoming aware of your thoughts, emotions, and beliefs about these problems.
3. Identifying negative or inaccurate thinking.
4. Reshaping negative or inaccurate thinking.

CBT emphasizes the role of distorted thinking in psychological distress. It's not about ignoring problems or pretending to be happy, but about developing healthier ways to cope and react.""",
        "quiz": [
            {
                "question": "What is a core aim of Cognitive Behavioral Therapy (CBT)?",
                "options": [
                    "To help individuals avoid all negative emotions.",
                    "To uncover repressed childhood memories.",
                    "To identify and reshape inaccurate or negative thinking.",
                    "To provide medication for mental health conditions."
                ],
                "answer": "To identify and reshape inaccurate or negative thinking."
            },
            {
                "question": "Which of these is NOT a typical key principle of CBT?",
                "options": [
                    "Identifying troubling situations.",
                    "Becoming aware of thoughts and emotions.",
                    "Reliving past traumatic experiences repeatedly.",
                    "Reshaping negative thinking."
                ],
                "answer": "Reliving past traumatic experiences repeatedly."
            }
        ]
    },
    "Thoughts, Emotions, and Behaviors": {
        "title": "The CBT Triangle: How They Connect",
        "text": """One of the fundamental concepts in CBT is the "CBT Triangle" or "Cognitive Triangle." This model illustrates how our thoughts, emotions, and behaviors are interconnected and influence each other.

* Thoughts: These are what we say to ourselves, our interpretations of events, beliefs, and assumptions. They can be automatic (quick, unbidden thoughts) or core beliefs (deep-seated ideas about ourselves, others, and the world).
* Emotions: These are our feelings, such as joy, sadness, anger, anxiety, fear, etc. They are often a direct result of our thoughts and perceptions.
* Behaviors: These are the actions we take or avoid taking. Our behaviors are often driven by our thoughts and emotions.

The CBT triangle suggests that if you change one corner of the triangle, the other two will also change. For example:
* If you change a negative thought ("I'm useless") to a more balanced one ("I made a mistake, but I can learn from it"), your emotion might shift from sadness to hope, and your behavior might change from withdrawing to trying again.
* If you change a behavior (e.g., stopping procrastination), you might start to have more positive thoughts about your abilities, which can lead to feelings of mastery.

Understanding this connection empowers you to break negative cycles by intervening at any point in the triangle.""",
        "quiz": [
            {
                "question": "According to the CBT Triangle, what three elements are interconnected?",
                "options": [
                    "Dreams, Reality, and Future",
                    "Thoughts, Emotions, and Behaviors",
                    "Past, Present, and Future",
                    "Friends, Family, and Work"
                ],
                "answer": "Thoughts, Emotions, and Behaviors"
            },
            {
                "question": "If you change a negative thought, what else is likely to change according to the CBT Triangle?",
                "options": [
                    "Only your thoughts",
                    "Your past experiences",
                    "Your emotions and behaviors",
                    "The weather"
                ],
                "answer": "Your emotions and behaviors"
            }
        ]
    },
    "Automatic Thoughts & Core Beliefs": {
        "title": "Identifying Your Thought Patterns",
        "text": """Automatic thoughts are immediate, spontaneous thoughts that pop into our minds in response to situations. They are often fleeting and we might not even be fully aware of them unless we pay close attention. They are typically unhelpful or distorted and can lead to negative emotions.

Examples of automatic thoughts:
* "I'm going to fail this." (when facing a task)
* "They think I'm stupid." (after making a small mistake)
* "It's hopeless." (when feeling down)

Core beliefs are deeper, more fundamental assumptions and beliefs we hold about ourselves, the world, and others. They are often developed early in life and are much more stable and resistant to change than automatic thoughts. Automatic thoughts often spring from our core beliefs.

Examples of core beliefs:
* "I am unlovable."
* "The world is a dangerous place."
* "I must be perfect to be accepted."

In CBT, we first learn to identify automatic thoughts, then challenge them by examining evidence for and against them. Over time, working with automatic thoughts can help to modify underlying core beliefs.""",
        "quiz": [
            {
                "question": "What characterizes an 'automatic thought'?",
                "options": [
                    "They are always positive.",
                    "They are deep-seated, unchanging assumptions.",
                    "They are immediate, spontaneous, and often unhelpful.",
                    "They only occur during sleep."
                ],
                "answer": "They are immediate, spontaneous, and often unhelpful."
            },
            {
                "question": "How do 'core beliefs' relate to 'automatic thoughts'?",
                "options": [
                    "Core beliefs are the result of automatic thoughts.",
                    "Automatic thoughts often spring from core beliefs.",
                    "They are completely unrelated concepts.",
                    "Core beliefs are only formed in adulthood."
                ],
                "answer": "Automatic thoughts often spring from core beliefs."
            }
        ]
    },
    "Cognitive Distortions": {
        "title": "Common Thinking Traps",
        "text": """Cognitive distortions are irrational or biased ways of thinking that can lead us to perceive reality inaccurately and fuel negative emotions. David Burns, a prominent CBT therapist, popularized a list of common distortions. Recognizing these patterns is the first step to challenging them.

Common Cognitive Distortions:
1. All-or-Nothing Thinking (Black-and-White Thinking): Viewing things in absolute terms; if your performance is not perfect, you see it as a total failure.
2. Overgeneralization: Seeing a single negative event as a never-ending pattern of defeat. "I failed this test, so I'm going to fail everything forever."
3. Mental Filter: Picking out a single negative detail and dwelling on it exclusively, so that your vision of all reality becomes darkened, like a drop of ink discoloring a beaker of water.
4. Discounting the Positive: Insisting that your positive qualities or achievements don’t count. "I only got that promotion because I got lucky."
5. Jumping to Conclusions:
    * Mind Reading: Assuming you know what people are thinking without sufficient evidence.
    * Fortune-Telling: Arbitrarily predicting that things will turn out badly.
6. Magnification (Catastrophizing) or Minimization: Exaggerating the importance of shortcomings or problems, or minimizing the importance of desirable qualities.
7. Emotional Reasoning: Assuming that because you feel a certain way, it must be true. "I feel like a failure, therefore I am a failure."
8. "Should" Statements: Trying to motivate yourself with "shoulds" and "shouldn'ts," as if you had to be whipped and punished before you could be expected to do anything.
9. Labeling and Mislabeling: An extreme form of overgeneralization; instead of describing your error, you attach a negative label to yourself. "I'm a loser" instead of "I made a mistake."
10. Personalization: Believing that you are directly responsible for events that are not entirely under your control.

Learning to identify these distortions in your own thinking is a powerful tool in CBT.""",
        "quiz": [
            {
                "question": "Which cognitive distortion involves viewing things in absolute, either/or terms?",
                "options": [
                    "Overgeneralization",
                    "Mental Filter",
                    "All-or-Nothing Thinking",
                    "Emotional Reasoning"
                ],
                "answer": "All-or-Nothing Thinking"
            },
            {
                "question": "What is 'Fortune-Telling' in the context of cognitive distortions?",
                "options": [
                    "Predicting positive outcomes for others.",
                    "Arbitrarily predicting that things will turn out badly.",
                    "Reading someone's past accurately.",
                    "Assuming you know what people are thinking."
                ],
                "answer": "Arbitrarily predicting that things will turn out badly."
            },
            {
                "question": "Saying 'I feel anxious, therefore this situation must be dangerous' is an example of which distortion?",
                "options": [
                    "Discounting the Positive",
                    "Magnification",
                    "Emotional Reasoning",
                    "Labeling"
                ],
                "answer": "Emotional Reasoning"
            }
        ]
    }
}