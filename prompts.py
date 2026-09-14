"""
Curated question & prompt bank for TOEFL 2026 and Duolingo English Test (DET).
"""

PROMPTS = {
    "toefl": {
        "name": "TOEFL iBT (2026 Format)",
        "badge": "TOEFL 2026",
        "color": "#3b82f6",
        "description": "7 Listen & Repeat + 4 Take an Interview tasks focusing on spontaneous spoken English.",
        "tasks": [
            {
                "type": "Listen & Repeat",
                "tag": "Repeat Sentence",
                "time_limit": 10,
                "instructions": "Listen to the sentence and repeat it exactly as you heard it. No prep time.",
                "scenarios": [
                    {
                        "scenario_name": "university laboratory orientation",
                        "sentences": [
                            "The lab opens at nine.",
                            "Please leave your bags at the door.",
                            "You must wear safety goggles at all times.",
                            "The emergency exit is located at the back of the room.",
                            "Make sure to clean your workstation before leaving the laboratory.",
                            "If you have any questions, raise your hand and the instructor will assist you.",
                            "Please make sure your student identification card is visible when entering the laboratory."
                        ]
                    },
                    {
                        "scenario_name": "campus library tour",
                        "sentences": [
                            "This is the main library.",
                            "We have over two million books.",
                            "The quiet study areas are on the third floor.",
                            "You can check out laptops at the front desk.",
                            "The library will extend its operating hours during the final examination week.",
                            "Students who wish to reserve a private study room must book it online in advance.",
                            "Please remember that eating and drinking are strictly prohibited in the rare book collection area."
                        ]
                    }
                ]
            },
            {
                "type": "Take an Interview",
                "tag": "Interview Question (45s)",
                "time_limit": 45,
                "instructions": "Respond directly to the interviewer's question. Speak for up to 45 seconds.",
                "prompts": [
                    "Some people prefer living in big cities with diverse entertainment, while others prefer quiet towns. Which do you prefer and why?",
                    "Do you agree or disagree with the idea that university students should be required to take physical education classes?",
                    "Tell me about a challenging project or assignment you recently worked on. How did you handle it?",
                    "Do you believe remote working from home is more productive than working in a traditional office? Give reasons for your opinion.",
                    "If you had the opportunity to learn any new skill or hobby this year, what would you choose and why?",
                    "Some people think technology has made personal relationships more distant. What is your perspective on this?"
                ]
            }
        ]
    },
    "det": {
        "name": "Duolingo English Test (DET)",
        "badge": "DET Format",
        "color": "#10b981",
        "description": "Speak About the Photo, Read Then Speak, Interactive Speaking, and Speaking Sample.",
        "tasks": [
            {
                "type": "Speak About the Photo",
                "tag": "Photo Description (90s)",
                "time_limit": 90,
                "instructions": "Speak for up to 90 seconds describing what is happening in the scene, the setting, and infer details.",
                "prompts": [
                    "A bustling outdoor farmers market on a sunny morning. Vendors are arranging fresh organic vegetables and fruits under colorful canvas awnings while shoppers interact warmly.",
                    "A modern university research library where diverse students are collaborating around a large wooden table with laptops, notebooks, and reference materials.",
                    "A cozy urban coffee shop interior where a barista is steaming milk behind a marble counter, and patrons are reading books and working near a rain-streaked window.",
                    "A serene mountain hiking trail at sunrise with two backpackers looking out over a misty valley and forested peaks."
                ]
            },
            {
                "type": "Read, Then Speak",
                "tag": "Read & Speak (90s)",
                "time_limit": 90,
                "instructions": "Read the prompt and speak for up to 90 seconds. Develop your ideas with specific reasons and examples.",
                "prompts": [
                    "Describe a memorable trip you took in the past. Where did you go, who did you go with, and why was it so significant to you?",
                    "Talk about a teacher or mentor who had a strong positive influence on your life. What qualities made them exceptional?",
                    "What is one environmental issue in your region or country that needs urgent attention? How should it be addressed?",
                    "Do you think public transportation should be completely free for all citizens? Explain your viewpoint."
                ]
            },
            {
                "type": "Interactive Speaking",
                "tag": "Interactive Turn (35s)",
                "time_limit": 35,
                "instructions": "Answer the conversational question directly and spontaneously within 35 seconds.",
                "prompts": [
                    "How do you usually unwind and recharge after an exhausting week of work or study?",
                    "Have you ever experienced a sudden change of plans while traveling? How did you adapt to it?",
                    "What role does music or art play in your daily routine?",
                    "If you could invite any historical figure to dinner, who would you choose and what would you ask them?",
                    "Do you prefer reading physical printed books or digital e-books? What drives your choice?"
                ]
            },
            {
                "type": "Speaking Sample",
                "tag": "Speaking Sample (3 min)",
                "time_limit": 180,
                "instructions": "Speak in-depth for up to 3 minutes on this complex topic. Present well-structured arguments and insights.",
                "prompts": [
                    "Some people argue that universities should focus exclusively on preparing students for specific careers, while others believe education should focus on broad intellectual curiosity. Discuss both perspectives and state your own view.",
                    "Artificial intelligence is rapidly transforming various industries. In your opinion, what are the most significant benefits and potential risks of this transformation for the global workforce?",
                    "Do you believe that personal happiness is primarily determined by external circumstances or internal mindset? Justify your position with relevant observations."
                ]
            }
        ]
    },
    "free": {
        "name": "Freestyle Practice",
        "badge": "Freestyle",
        "color": "#8b5cf6",
        "description": "Speak freely without time constraints or strict prompts. Perfect for impromptu speaking drills.",
        "tasks": [
            {
                "type": "Free Topic",
                "tag": "Impromptu Speech",
                "time_limit": None,
                "instructions": "Speak freely on any topic. Take as much time as you need.",
                "prompts": [
                    "Summarize what you accomplished today and your key priorities for tomorrow.",
                    "Explain a complex concept from your field of study or work in simple terms to a beginner.",
                    "Share your opinion on a recent news event or technological breakthrough that caught your interest."
                ]
            }
        ]
    }
}
