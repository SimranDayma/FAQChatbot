"""
CodeAlpha Internship - Task 2: FAQ Chatbot
Author: Your Name
Description: A GUI-based FAQ Chatbot for Tech Product support using
             NLP techniques like cosine similarity and TF-IDF
"""

import tkinter as tk
from tkinter import scrolledtext
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import random

# ── FAQ DATABASE ──────────────────────────────────────────────────────────────
FAQ_DATA = [
    {"question": "How do I reset my password forgot password cant login",
     "answer": "To reset your password, click 'Forgot Password' on the login page. Enter your registered email and we'll send you a reset link within 2 minutes. Check your spam folder if you don't see it."},
    {"question": "How do I download the app install",
     "answer": "You can download our app from the Google Play Store (Android) or Apple App Store (iOS). Just search for our app name and tap Install. It's completely free!"},
    {"question": "What are the system requirements device compatibility",
     "answer": "Our app requires Android 8.0 or higher, or iOS 13 or higher. For desktop you need Windows 10/11 or macOS 10.14+, with at least 4GB RAM and 2GB free storage."},
    {"question": "How do I update the app new version",
     "answer": "To update the app, go to your Play Store or App Store and search for our app. If an update is available, you'll see an 'Update' button. You can also enable auto-updates in your store settings."},
    {"question": "How do I contact customer support help",
     "answer": "You can reach our support team 24/7 via Email: support@techapp.com, Live Chat on our website, or call 1-800-TECH-HELP. Average response time is under 2 hours."},
    {"question": "How do I cancel my subscription plan",
     "answer": "To cancel your subscription, go to Settings → Subscription → Cancel Plan. Your access continues until the end of your billing period. No cancellation fees apply."},
    {"question": "Is my data secure private safe",
     "answer": "Yes! We use 256-bit AES encryption for all data. We never sell your personal data to third parties. You can request a full data export or deletion at any time from Settings → Privacy."},
    {"question": "How do I create an account sign up register",
     "answer": "Click 'Sign Up' on our homepage, enter your email and a password, verify your email address, and you're ready to go. It takes less than 2 minutes!"},
    {"question": "Why is the app not working crashed broken error",
     "answer": "Try these steps: 1) Check your internet connection, 2) Force close and reopen the app, 3) Clear the app cache in Settings, 4) Uninstall and reinstall. If the issue persists, contact support."},
    {"question": "How do I change my email address update email",
     "answer": "Go to Settings → Account → Edit Profile → Email. Enter your new email and verify it via the confirmation link. Your old email will be deactivated after verification."},
    {"question": "What payment methods do you accept billing",
     "answer": "We accept Visa, Mastercard, Amex, PayPal, Google Pay, Apple Pay, and UPI. All transactions are secured with SSL encryption."},
    {"question": "How do I get a refund money back",
     "answer": "We offer a 30-day money-back guarantee. Go to Settings → Billing → Request Refund, or email billing@techapp.com with your order ID. Refunds are processed within 5-7 business days."},
    {"question": "Can I use the app offline without internet",
     "answer": "Yes! Basic features work offline. However syncing, real-time updates, and cloud backup require internet. Downloaded content stays accessible offline."},
    {"question": "How do I enable dark mode night theme",
     "answer": "Go to Settings → Display → Theme and select 'Dark'. You can also set it to 'Auto' to match your device's system theme automatically."},
    {"question": "How do I delete my account remove profile",
     "answer": "Go to Settings → Account → Delete Account. This permanently removes all your data and cannot be undone. Please export your data first if needed."},
    {"question": "How do I backup my data save",
     "answer": "Your data is automatically backed up to the cloud every 24 hours. For manual backup go to Settings → Data → Backup Now. You can also export as CSV or PDF."},
    {"question": "What is the free trial premium features",
     "answer": "We offer a 14-day free trial with full access to all premium features. No credit card required. You'll be notified 3 days before the trial ends."},
    {"question": "How do I report a bug problem issue feedback",
     "answer": "Go to Settings → Help → Report a Problem. Describe the issue and attach a screenshot if possible. Our tech team reviews all reports within 24 hours."},
    {"question": "Is the app available on all devices platforms",
     "answer": "Yes! Our app is available on Android, iOS, Windows, macOS, and as a web app on any browser. All data syncs across all your devices."},
    {"question": "Which apps are good for learning English language",
     "answer": "Great apps for learning English: 1) Duolingo - fun and free, 2) BBC Learning English - professional content, 3) HelloTalk - chat with native speakers, 4) Grammarly - improve writing, 5) Cambly - live tutors. All available on Android and iOS!"},
    {"question": "What are best productivity apps tools recommended",
     "answer": "Top productivity apps: 1) Notion - notes and projects, 2) Todoist - task management, 3) Google Drive - file storage, 4) Slack - team communication, 5) Trello - kanban boards. All free to get started!"},
    {"question": "How do I improve battery life phone",
     "answer": "To save battery: 1) Lower screen brightness, 2) Turn off WiFi/Bluetooth when unused, 3) Enable battery saver mode, 4) Close background apps, 5) Disable location for unused apps."},
    {"question": "How do I clear cache storage space memory",
     "answer": "On Android: Settings → Apps → Select App → Clear Cache. On iOS: Settings → General → iPhone Storage → Offload App. This frees space without deleting your data."},
    {"question": "What programming languages should I learn coding development",
     "answer": "For beginners start with: 1) Python - easy and great for AI/ML, 2) JavaScript - for web development, 3) Java - for Android apps. For AI specifically, Python with TensorFlow or PyTorch is the best choice!"},
    {"question": "How do I share account family members plan",
     "answer": "Our Family Plan allows up to 5 members. Go to Settings → Subscription → Family Plan → Invite Members. Each member gets their own login and personalized experience."},
]

# ── CONVERSATION PATTERNS ─────────────────────────────────────────────────────
GREETINGS_INPUT  = ["hi", "hello", "hey", "howdy", "hiya", "sup", "good morning", "good evening", "good afternoon"]
GREETINGS_OUTPUT = [
    "Hey there! How can I help you today?",
    "Hello! I'm TechBot. What can I assist you with?",
    "Hi! Got a question? I'm here to help!",
]

FAREWELL_INPUT  = ["bye", "goodbye", "exit", "quit", "see you", "thanks bye", "thank you bye"]
FAREWELL_OUTPUT = [
    "Goodbye! Have a great day!",
    "See you later! Feel free to come back anytime!",
    "Bye! Hope I was helpful!",
]

THANKS_INPUT  = ["thanks", "thank you", "thankyou", "thx", "ty", "great thanks", "perfect", "awesome"]
THANKS_OUTPUT = [
    "You're welcome! Anything else I can help with?",
    "Happy to help! Let me know if you have more questions!",
    "Anytime! Feel free to ask if you need more help!",
]

INTRO_INPUT = ["who are you", "introduce yourself", "what are you",
               "what can you do", "tell me about yourself", "what is techbot",
               "your name", "about you", "what do you do"]

INTRO_OUTPUT = ("I'm TechBot, an AI-powered FAQ Assistant!\n\n"
                "I can help you with:\n"
                "  - Password reset and account issues\n"
                "  - App downloads, updates and compatibility\n"
                "  - Billing, refunds and subscriptions\n"
                "  - Privacy and data security\n"
                "  - App recommendations and tech tips\n"
                "  - Programming and learning resources\n\n"
                "Just type your question and I'll do my best to answer!")

# ── NLP FUNCTIONS ─────────────────────────────────────────────────────────────
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess(text):
    text   = text.lower()
    text   = text.translate(str.maketrans("", "", string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return " ".join(tokens)

def get_best_answer(user_input):
    all_questions  = [preprocess(faq["question"]) for faq in FAQ_DATA]
    user_processed = preprocess(user_input)
    vectorizer     = TfidfVectorizer()
    all_vectors    = vectorizer.fit_transform(all_questions + [user_processed])
    user_vector    = all_vectors[-1]
    similarities   = cosine_similarity(user_vector, all_vectors[:-1]).flatten()
    best_idx       = similarities.argmax()
    best_score     = similarities[best_idx]
    if best_score > 0.2:
        return FAQ_DATA[best_idx]["answer"]
    return None

def chatbot_response(user_input):
    text = user_input.lower().strip()
    if any(greet in text for greet in GREETINGS_INPUT):
        return random.choice(GREETINGS_OUTPUT)
    if any(fare in text for fare in FAREWELL_INPUT):
        return random.choice(FAREWELL_OUTPUT)
    if any(thank in text for thank in THANKS_INPUT):
        return random.choice(THANKS_OUTPUT)
    if any(intro in text for intro in INTRO_INPUT):
        return INTRO_OUTPUT
    answer = get_best_answer(user_input)
    if answer:
        return answer
    return ("I'm not sure about that. Could you rephrase?\n\n"
            "I can help with: password reset, app download, billing,\n"
            "refunds, privacy, dark mode, account settings, and more!\n"
            "Or type 'who are you' to see everything I can do.")

# ── GUI ───────────────────────────────────────────────────────────────────────
class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TechBot - FAQ Assistant | CodeAlpha")
        self.root.configure(bg="#0d1117")
        self.root.state('zoomed')
        self._build_ui()
        self._show_welcome()

    def _build_ui(self):
        BG      = "#0d1117"
        CHAT_BG = "#161b22"
        BTN     = "#238636"
        BTN_HOV = "#2ea043"
        TEXT    = "#e6edf3"
        SUBTEXT = "#8b949e"

        header = tk.Frame(self.root, bg="#161b22", pady=12)
        header.pack(fill="x", side="top")
        tk.Label(header, text="TechBot", font=("Segoe UI", 18, "bold"),
                 bg="#161b22", fg=TEXT).pack(side="left", padx=20)
        tk.Label(header, text="FAQ Assistant — CodeAlpha AI Internship",
                 font=("Segoe UI", 10), bg="#161b22", fg=SUBTEXT).pack(side="left")
        tk.Label(header, text="Online", font=("Segoe UI", 10),
                 bg="#161b22", fg="#3fb950").pack(side="right", padx=20)

        input_frame = tk.Frame(self.root, bg="#161b22", pady=12)
        input_frame.pack(fill="x", side="bottom", padx=15, pady=10)
        send_btn = tk.Button(input_frame, text="Send",
            font=("Segoe UI", 12, "bold"), bg=BTN, fg="white",
            relief="flat", padx=20, pady=8, cursor="hand2",
            command=self._send_message)
        send_btn.pack(side="right", padx=(5, 10))
        send_btn.bind("<Enter>", lambda e: send_btn.config(bg=BTN_HOV))
        send_btn.bind("<Leave>", lambda e: send_btn.config(bg=BTN))
        self.input_field = tk.Entry(input_frame, font=("Segoe UI", 13),
            bg="#21262d", fg=TEXT, insertbackground=TEXT, relief="flat", bd=0)
        self.input_field.pack(side="left", fill="x", expand=True, padx=(10, 5), ipady=10)
        self.input_field.bind("<Return>", lambda e: self._send_message())
        self.input_field.focus()

        suggest_frame = tk.Frame(self.root, bg=BG)
        suggest_frame.pack(fill="x", side="bottom", padx=15, pady=(0, 5))
        tk.Label(suggest_frame, text="Try asking:", font=("Segoe UI", 9),
                 bg=BG, fg=SUBTEXT).pack(side="left")
        for s in ["Who are you", "Reset password", "Get refund", "Learn English", "Best apps"]:
            tk.Button(suggest_frame, text=s, font=("Segoe UI", 9),
                bg="#21262d", fg="#79c0ff", relief="flat", padx=8, pady=3,
                cursor="hand2", command=lambda x=s: self._send_suggestion(x)
            ).pack(side="left", padx=3)

        chat_frame = tk.Frame(self.root, bg=BG)
        chat_frame.pack(fill="both", expand=True, padx=15, pady=5)
        self.chat_display = scrolledtext.ScrolledText(chat_frame,
            font=("Segoe UI", 12), bg=CHAT_BG, fg=TEXT,
            relief="flat", wrap="word", state="disabled",
            padx=15, pady=15, spacing3=8)
        self.chat_display.pack(fill="both", expand=True)
        self.chat_display.tag_config("user",    foreground="#79c0ff", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("bot",     foreground="#3fb950", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("message", foreground=TEXT,      font=("Segoe UI", 12))
        self.chat_display.tag_config("divider", foreground="#30363d", font=("Segoe UI", 8))

    def _show_welcome(self):
        self._add_message("TechBot",
            "Hello! I'm TechBot, your Tech Support Assistant!\n"
            "I can answer questions about passwords, billing, downloads, privacy and more.\n"
            "Type 'who are you' to see everything I can do!\n"
            "What can I help you with today?", "bot")

    def _add_message(self, sender, message, tag):
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", f"\n{sender}\n", tag)
        self.chat_display.insert("end", f"{message}\n", "message")
        self.chat_display.insert("end", "─" * 60 + "\n", "divider")
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

    def _send_message(self):
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        self._add_message("You", user_input, "user")
        self.input_field.delete(0, "end")
        self._add_message("TechBot", chatbot_response(user_input), "bot")

    def _send_suggestion(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)
        self._send_message()

if __name__ == "__main__":
    root = tk.Tk()
    app  = ChatbotApp(root)
    root.mainloop()