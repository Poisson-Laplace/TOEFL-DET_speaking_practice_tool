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
                "prep_time": 0,
                "instructions": "Listen to the sentence and repeat it exactly as you heard it. No prep time.",
                "instructions_tr": "Cümleyi dinle ve duyduğun şekliyle tekrar et. Hazırlık süresi yok.",
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
                    },
                    {
                        "scenario_name": "student health center visit",
                        "sentences": [
                            "The clinic closes at five.",
                            "Please check in at the front desk.",
                            "A nurse will call your name shortly.",
                            "You can schedule a follow-up appointment online.",
                            "Students should bring their identification and insurance information to every appointment.",
                            "If your symptoms become worse overnight, contact the twenty-four-hour medical advice line.",
                            "Although walk-in visits are sometimes available, booking an appointment in advance will usually reduce your waiting time."
                        ]
                    },
                    {
                        "scenario_name": "academic advising appointment",
                        "sentences": [
                            "Your adviser is ready.",
                            "Bring a copy of your schedule.",
                            "We can review your degree requirements together.",
                            "The registration system opens for seniors on Monday morning.",
                            "Before changing your major, consider how many of your completed credits will transfer.",
                            "Students who are uncertain about their course selection may request another advising appointment next week.",
                            "Because several required seminars fill quickly, you should prepare a few alternative courses before your registration window opens."
                        ]
                    },
                    {
                        "scenario_name": "campus housing orientation",
                        "sentences": [
                            "Your room is upstairs.",
                            "Laundry cards are sold here.",
                            "Guests must leave the building by midnight.",
                            "Report any maintenance problems through the housing website.",
                            "Residents share responsibility for keeping the kitchen and common areas clean.",
                            "If the fire alarm sounds, leave your belongings behind and meet outside by the north gate.",
                            "To avoid additional charges at the end of the semester, complete the room inspection form within forty-eight hours of moving in."
                        ]
                    },
                    {
                        "scenario_name": "research skills workshop",
                        "sentences": [
                            "The workshop begins soon.",
                            "Please open the course website.",
                            "Today we will evaluate several online sources.",
                            "Use quotation marks when searching for an exact phrase.",
                            "Reliable academic sources normally identify their authors, evidence, and publication dates.",
                            "When two studies reach different conclusions, compare their methods before deciding which claim is stronger.",
                            "As you prepare your final paper, keep detailed notes so that every borrowed idea can be cited accurately and consistently."
                        ]
                    },
                    {
                        "scenario_name": "career center session",
                        "sentences": [
                            "Welcome to the career center.",
                            "Upload your résumé before Friday.",
                            "Employers will visit campus next month.",
                            "Practice describing your experience in clear, specific terms.",
                            "You can reserve a private room for an online interview at no cost.",
                            "After the networking event, send each recruiter a brief message thanking them for their time.",
                            "Even if a position does not match every one of your qualifications, a thoughtful application may still lead to an interview."
                        ]
                    }
                ]
            },
            {
                "type": "Take an Interview",
                "tag": "Interview Question (45s)",
                "time_limit": 45,
                "prep_time": 0,
                "instructions": "Respond directly to the interviewer's question. Speak for up to 45 seconds.",
                "instructions_tr": "Görüşmecinin sorusuna doğrudan yanıt ver. En fazla 45 saniye konuş.",
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
                "prep_time": 20,
                "instructions": "Speak for up to 90 seconds describing what is happening in the scene, the setting, and infer details.",
                "instructions_tr": "Sahneyi, ortamı ve çıkarımlarını anlatarak en fazla 90 saniye konuş.",
                "prompts": [
                    {
                        "prompt": "Describe the people, produce, and activity at this farmers market.",
                        "image": "assets/photos/farmers_market.jpg",
                        "credit": "Alabama Extension · CC0",
                        "source": "https://commons.wikimedia.org/wiki/File:Green_Peppers_at_Farmers_Market.jpg"
                    },
                    {
                        "prompt": "Describe the people and study environment shown in this library.",
                        "image": "assets/photos/library.jpg",
                        "credit": "Bjeweld · CC0",
                        "source": "https://commons.wikimedia.org/wiki/File:Students_and_Readers_in_the_Library.jpg"
                    },
                    {
                        "prompt": "Describe the person, setting, and activity in this coffee shop.",
                        "image": "assets/photos/coffee_shop.jpg",
                        "credit": "Tim Wright · CC0",
                        "source": "https://commons.wikimedia.org/wiki/File:Baristas_at_work_(Unsplash).jpg"
                    },
                    {
                        "prompt": "Describe the hikers, trail, and surrounding landscape.",
                        "image": "assets/photos/hikers.jpg",
                        "credit": "Deborah Lee Soltesz · CC0",
                        "source": "https://commons.wikimedia.org/wiki/File:Aspen_loop_hikers_(37050338693).jpg"
                    }
                ]
            },
            {
                "type": "Read, Then Speak",
                "tag": "Read & Speak (90s)",
                "time_limit": 90,
                "prep_time": 20,
                "instructions": "Read the prompt and speak for up to 90 seconds. Develop your ideas with specific reasons and examples.",
                "instructions_tr": "Soruyu oku ve en fazla 90 saniye konuş. Fikirlerini nedenler ve örneklerle geliştir.",
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
                "prep_time": 0,
                "instructions": "Continue a six-turn conversation. Respond naturally to each follow-up within 35 seconds; there is no prep time.",
                "instructions_tr": "Altı turluk konuşmayı sürdür. Her takip sorusuna hazırlık süresi olmadan 35 saniye içinde doğal biçimde yanıt ver.",
                "conversation_sets": [
                    {
                        "topic": "group projects",
                        "questions": [
                            "Do you generally enjoy working on group projects? Why or why not?",
                            "Tell me about a role you usually take when working with a team.",
                            "What would you do if one team member repeatedly missed important deadlines?",
                            "How can a group make sure quieter members have a chance to contribute?",
                            "Do online collaboration tools improve teamwork, or can they create new problems?",
                            "What is the most important lesson students can learn from completing a difficult project together?"
                        ]
                    },
                    {
                        "topic": "learning a new skill",
                        "questions": [
                            "What is a skill you would genuinely like to learn in the near future?",
                            "What first made you interested in developing that skill?",
                            "Would you rather learn it independently or with an instructor? Explain your choice.",
                            "How would you stay motivated when your progress became slow?",
                            "What practical difference could this skill make in your daily life?",
                            "Once you became confident, how might you help someone else learn the same skill?"
                        ]
                    },
                    {
                        "topic": "campus life",
                        "questions": [
                            "Which part of campus life is most important for helping new students feel welcome?",
                            "Describe an activity that could help students make friends more easily.",
                            "Why do some students avoid joining clubs even when they are interested in them?",
                            "How could a university encourage more students to participate in campus events?",
                            "Should students be expected to balance social activities with academic responsibilities on their own?",
                            "If you could create one new campus tradition, what would it be and why?"
                        ]
                    },
                    {
                        "topic": "technology and routines",
                        "questions": [
                            "What piece of technology do you use most often during a normal day?",
                            "In what specific way does it make your routine easier?",
                            "Can relying on that technology too much cause any difficulties?",
                            "Tell me about a time when you had to complete a task without it.",
                            "Do you think people should intentionally spend part of each day away from screens?",
                            "How do you expect your daily use of technology to change over the next five years?"
                        ]
                    }
                ]
            },
            {
                "type": "Speaking Sample",
                "tag": "Speaking Sample (3 min)",
                "time_limit": 180,
                "prep_time": 30,
                "instructions": "Speak in-depth for up to 3 minutes on this complex topic. Present well-structured arguments and insights.",
                "instructions_tr": "Bu konu hakkında en fazla 3 dakika ayrıntılı konuş. Düzenli argümanlar ve görüşler sun.",
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
                "prep_time": 0,
                "instructions": "Speak freely on any topic. Take as much time as you need.",
                "instructions_tr": "İstediğin konuda serbestçe konuş. İhtiyacın kadar süre kullan.",
                "prompts": [
                    "Summarize what you accomplished today and your key priorities for tomorrow.",
                    "Explain a complex concept from your field of study or work in simple terms to a beginner.",
                    "Share your opinion on a recent news event or technological breakthrough that caught your interest."
                ]
            }
        ]
    }
}
