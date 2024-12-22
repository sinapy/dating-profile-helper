import anthropic
import time
import dotenv

# Load environment variables from a .env file
dotenv.load_dotenv()

class DatingProfileInterviewer:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.responses = {}
        
    def have_conversation(self):
        """Conducts a natural conversation to gather information."""
        print("Hi! I'm going to help you create an amazing dating profile. Let's just have a casual")
        print("chat, and I'll handle turning your responses into a great profile. Ready to begin?")
        input("Press Enter when you're ready...")
        
        # Basic conversation flow
        questions = [
            {
                "id": "introduction",
                "text": "First, tell me a bit about yourself - whatever comes to mind!",
                "follow_ups": ["What do you do for work?", "How do you usually spend your free time?"]
            },
            {
                "id": "personality",
                "text": "What would your closest friends say are your best qualities?",
                "follow_ups": ["Can you give me an example of when you showed those qualities?"]
            },
            {
                "id": "passions",
                "text": "What gets you excited or makes you lose track of time?",
                "follow_ups": ["What drew you to that?", "How long have you been interested in that?"]
            },
            {
                "id": "lifestyle",
                "text": "Describe your perfect weekend - no limitations!",
                "follow_ups": ["What makes those activities special to you?"]
            },
            {
                "id": "relationships",
                "text": "What kind of relationship are you hoping to find?",
                "follow_ups": ["What qualities matter most to you in a partner?"]
            },
            {
                "id": "quirks",
                "text": "What's something unique or surprising about you that people might not guess?",
                "follow_ups": ["That's interesting! Tell me more about that."]
            }
        ]
        
        for question in questions:
            print(f"\n{question['text']}")
            main_response = input("> ").strip()
            self.responses[question['id']] = [main_response]
            
            # Ask follow-ups based on their response
            for follow_up in question['follow_ups']:
                print(f"\n{follow_up}")
                follow_up_response = input("> ").strip()
                self.responses[question['id']].append(follow_up_response)
            
            # Add a small pause between question sets
            time.sleep(1)
            
        print("\nThanks for sharing! Give me a moment to craft your profile...")
    
    def generate_profile(self):
        """Uses Claude to create a profile from the conversation responses."""
        prompt = f"""
You are a skilled dating profile writer who creates authentic, engaging profiles. Use the following 
conversation responses to create a compelling dating profile. Maintain the person's authentic voice 
while making the profile engaging and memorable.

Conversation details:
Introduction: {' | '.join(self.responses['introduction'])}
Personality: {' | '.join(self.responses['personality'])}
Passions: {' | '.join(self.responses['passions'])}
Lifestyle: {' | '.join(self.responses['lifestyle'])}
Relationship Goals: {' | '.join(self.responses['relationships'])}
Unique Qualities: {' | '.join(self.responses['quirks'])}

Please create:
1. A catchy headline/tagline
2. A main profile bio (250-300 words) that tells their story in an engaging way
3. A brief "Looking for" section
4. 3-4 conversation starters that potential matches could use

Write the profile in first person, maintaining their authentic voice while making it engaging 
and polished. Focus on specific details and stories they shared rather than generic statements. 
Use humor or wit if it matches their style from the conversation.

Format the response with clear sections but make it feel natural and flowing.
"""
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content
        except Exception as e:
            return "I encountered an error while generating your profile. Please try again."

def main():
    interviewer = DatingProfileInterviewer()
    
    print("=== Dating Profile Creator ===")
    print("Let's have a conversation to create your perfect dating profile!")
    print("Just chat naturally, and I'll handle turning your responses into a great profile.\n")
    
    interviewer.have_conversation()
    profile = interviewer.generate_profile()
    
    print("\n=== Your Dating Profile ===")
    print(profile)
    
    print("\nWhat do you think? I can regenerate it if you'd like any changes!")
    feedback = input("Would you like me to make any adjustments? (yes/no) > ")
    
    if feedback.lower().startswith('y'):
        print("\nWhat would you like me to adjust? For example:")
        print("- Make it more humorous")
        print("- Focus more on specific interests")
        print("- Adjust the tone")
        adjustments = input("> ")
        
        # Generate a new version with the adjustments
        adjustment_prompt = f"""
Previous profile:
{profile}

Please revise this profile with the following adjustments:
{adjustments}

Maintain the same authentic information while incorporating these changes.
"""
        try:
            revised = interviewer.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": adjustment_prompt}
                ]
            )
            print("\n=== Your Revised Profile ===")
            print(revised.content)
        except Exception as e:
            print("I encountered an error while revising the profile. Please try again.")

if __name__ == "__main__":
    main()