# 🤖 FAQ Chatbot — CodeAlpha Internship Task 2

A GUI-based FAQ Chatbot for Tech Product support built with Python as part of the **CodeAlpha AI Internship**. Uses NLP techniques like TF-IDF and Cosine Similarity to match user questions with the best answers.


 ✨ Features

- 💬 Answers **25+ Tech Support FAQs** intelligently
- 🔍 **NLP-powered matching** using TF-IDF and Cosine Similarity
- 🧠 **Text preprocessing** — tokenization, stopword removal, lemmatization
- 👋 Handles greetings, farewells, thanks and introductions
- 🖱️ **Quick suggestion buttons** for common questions
- ⌨️ Press **Enter** to send messages
- 🖥️ Opens fullscreen automatically
- 🌙 Dark GitHub-style UI

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core programming language |
| Tkinter | GUI window and chat interface |
| NLTK | Text preprocessing (tokenization, lemmatization) |
| Scikit-learn | TF-IDF vectorization and cosine similarity |

---

## 📦 Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/CodeAlpha_FAQChatbot.git
cd CodeAlpha_FAQChatbot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Download NLTK data (run once)**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

**4. Run the chatbot**
```bash
python task2_faq_chatbot.py
```

---

## 🚀 How It Works

1. User types a question in the chat box
2. The question is **preprocessed** — lowercased, punctuation removed, stopwords filtered, lemmatized
3. **TF-IDF** converts the text into numerical vectors
4. **Cosine Similarity** finds the most similar FAQ question
5. If similarity score > 0.2, the matching answer is returned
6. Otherwise, the bot asks the user to rephrase

---

## 💬 Sample Questions to Try

- *"How do I reset my password?"*
- *"Which apps are good for learning English?"*
- *"Is my data safe?"*
- *"How do I get a refund?"*
- *"Who are you?"*
- *"What programming language should I learn?"*

---

## 📁 Project Structure

```
CodeAlpha_FAQChatbot/
├── task2_faq_chatbot.py    # Main chatbot application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🙋 Author

**Your Name**
AI Intern at CodeAlpha
[LinkedIn](https://linkedin.com/in/your-profile) | [GitHub](https://github.com/your-username)

---

## 🏢 About CodeAlpha

CodeAlpha is a leading software development company providing internship opportunities in AI, web development, and more.
🌐 [www.codealpha.tech](https://www.codealpha.tech)
