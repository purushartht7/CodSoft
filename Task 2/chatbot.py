import re
import random
from datetime import datetime

class RuleBasedChatbot:
    def __init__(self):
        self.name = "ChatBot"
        self.rules = {
            # Greetings
            r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b': [
                "Hello! How can I help you today?",
                "Hi there! Nice to meet you!",
                "Hey! What can I do for you?",
                "Greetings! How are you doing?"
            ],
            
            # How are you
            r'\b(how are you|how do you do|are you ok|are you doing well)\b': [
                "I'm doing great, thanks for asking! How about you?",
                "I'm functioning perfectly! How are you?",
                "All systems operational! How's your day going?",
                "I'm good, thank you! How are you feeling today?"
            ],
            
            # Name related
            r'\b(what is your name|what should i call you|who are you|your name)\b': [
                f"My name is {self.name}! Nice to meet you!",
                f"I'm {self.name}, your friendly chatbot assistant!",
                f"You can call me {self.name}!",
                f"I go by {self.name}. How about you?"
            ],
            
            # User's name
            r'\b(my name is|i am|i\'m|call me)\s+(\w+)': [
                "Nice to meet you, {name}!",
                "Hello {name}! That's a great name!",
                "Pleased to meet you, {name}!",
                "Hi {name}! How are you doing?"
            ],
            
            # Time and date
            r'\b(what time|current time|time now|what is the time)\b': [
                lambda: f"The current time is {datetime.now().strftime('%H:%M:%S')}",
                lambda: f"It's {datetime.now().strftime('%I:%M %p')} right now",
                lambda: f"Current time: {datetime.now().strftime('%H:%M')}"
            ],
            
            r'\b(what date|today\'s date|current date|what day)\b': [
                lambda: f"Today is {datetime.now().strftime('%A, %B %d, %Y')}",
                lambda: f"The date is {datetime.now().strftime('%m/%d/%Y')}",
                lambda: f"It's {datetime.now().strftime('%B %d, %Y')} today"
            ],
            
            # Weather (mock responses)
            r'\b(weather|temperature|forecast|is it raining|is it sunny)\b': [
                "I can't check the weather in real-time, but I hope it's nice where you are!",
                "I don't have access to weather data, but I'm sure it's beautiful outside!",
                "You might want to check a weather app for accurate information!",
                "I can't see outside, but I hope the weather is pleasant for you!"
            ],
            
            # Help
            r'\b(help|what can you do|capabilities|features)\b': [
                "I can help you with:\n- Greetings and conversations\n- Telling time and date\n- Answering basic questions\n- Having a friendly chat!",
                "Here's what I can do:\n- Chat with you\n- Tell you the time and date\n- Answer simple questions\n- Keep you company!",
                "My capabilities include:\n- Basic conversation\n- Time and date information\n- Simple Q&A\n- Friendly interaction!"
            ],
            
            # Goodbye
            r'\b(bye|goodbye|see you|farewell|exit|quit)\b': [
                "Goodbye! It was nice chatting with you!",
                "See you later! Have a great day!",
                "Take care! Come back anytime!",
                "Bye! Thanks for the conversation!"
            ],
            
            # Thank you
            r'\b(thank you|thanks|thx|appreciate it)\b': [
                "You're welcome! I'm happy to help!",
                "No problem at all!",
                "Anytime! That's what I'm here for!",
                "My pleasure! Is there anything else I can help with?"
            ],
            
            # Jokes
            r'\b(tell me a joke|joke|funny|humor)\b': [
                "Why don't scientists trust atoms? Because they make up everything!",
                "What do you call a fake noodle? An impasta!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "What do you call a bear with no teeth? A gummy bear!"
            ],
            
            # Math (simple calculations)
            r'\b(what is|calculate|compute)\s+(\d+)\s*([+\-*/])\s*(\d+)': [
                lambda match: self.calculate_math(match),
                lambda match: self.calculate_math(match),
                lambda match: self.calculate_math(match)
            ],
            
            # Default responses for unrecognized input
            r'.*': [
                "I'm not sure I understand. Could you rephrase that?",
                "That's interesting! Tell me more about that.",
                "I'm still learning. Could you try asking something else?",
                "I didn't quite catch that. Can you explain differently?"
            ]
        }
        
        self.user_name = None
        self.conversation_history = []
    
    def calculate_math(self, match):
        """Calculate simple math operations"""
        try:
            num1 = float(match.group(2))
            operator = match.group(3)
            num2 = float(match.group(4))
            
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    return "Sorry, I can't divide by zero!"
                result = num1 / num2
            else:
                return "I can only handle basic math operations (+, -, *, /)"
            
            return f"The result of {num1} {operator} {num2} is {result}"
        except:
            return "Sorry, I couldn't calculate that. Please check your input."
    
    def extract_user_name(self, message):
        """Extract user's name from the message"""
        name_patterns = [
            r'my name is (\w+)',
            r'i am (\w+)',
            r'i\'m (\w+)',
            r'call me (\w+)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, message.lower())
            if match:
                return match.group(1).title()
        return None
    
    def get_response(self, user_input):
        """Get appropriate response based on user input"""
        user_input_lower = user_input.lower()
        
        # Extract user name if mentioned
        if not self.user_name:
            extracted_name = self.extract_user_name(user_input)
            if extracted_name:
                self.user_name = extracted_name
        
        # Check each rule pattern
        for pattern, responses in self.rules.items():
            match = re.search(pattern, user_input_lower)
            if match:
                # Select a random response from the list
                response = random.choice(responses)
                
                # Handle lambda functions (for dynamic responses)
                if callable(response):
                    try:
                        response = response(match)
                    except TypeError:
                        response = response()
                
                # Replace placeholders
                if isinstance(response, str) and '{name}' in response and self.user_name:
                    response = response.format(name=self.user_name)
                
                # Store conversation
                self.conversation_history.append({
                    'user': user_input,
                    'bot': response,
                    'timestamp': datetime.now()
                })
                
                return response
        
        # Fallback response (shouldn't reach here due to catch-all pattern)
        return "I'm not sure how to respond to that."
    
    def get_conversation_history(self):
        """Get the conversation history"""
        return self.conversation_history
    
    def reset_conversation(self):
        """Reset conversation history and user name"""
        self.conversation_history = []
        self.user_name = None

def main():
    """Main function to run the chatbot"""
    chatbot = RuleBasedChatbot()
    
    print("=" * 50)
    print("🤖 Welcome to Rule-Based ChatBot!")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the conversation")
    print("Type 'help' to see what I can do")
    print("Type 'history' to see our conversation")
    print("Type 'reset' to start fresh")
    print("=" * 50)
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"{chatbot.name}: Goodbye! It was nice chatting with you!")
                break
            
            elif user_input.lower() == 'history':
                history = chatbot.get_conversation_history()
                if history:
                    print(f"\n{chatbot.name}: Here's our conversation history:")
                    for entry in history[-5:]:  # Show last 5 exchanges
                        print(f"You: {entry['user']}")
                        print(f"{chatbot.name}: {entry['bot']}")
                        print()
                else:
                    print(f"{chatbot.name}: No conversation history yet!")
                continue
            
            elif user_input.lower() == 'reset':
                chatbot.reset_conversation()
                print(f"{chatbot.name}: Conversation reset! Let's start fresh!")
                continue
            
            elif not user_input:
                print(f"{chatbot.name}: Please say something!")
                continue
            
            response = chatbot.get_response(user_input)
            print(f"{chatbot.name}: {response}")
            print()
            
        except KeyboardInterrupt:
            print(f"\n{chatbot.name}: Goodbye! Thanks for chatting!")
            break
        except Exception as e:
            print(f"{chatbot.name}: Sorry, something went wrong. Please try again!")

if __name__ == "__main__":
    main() 