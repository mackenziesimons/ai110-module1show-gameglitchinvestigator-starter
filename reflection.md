# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  
The first time I ran the game, it would not let me press enter to submit my number. It also seemed like the indicators were opposite.(Go higher and lower) Two concrete bugs would be the hints were backwards, and the attempts were off.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used AI as a teammate through the wonders of Copilot. I also occasionally used ChatGPT just to double check to see if I would recieve an opposing answer. An example of AI being correct towards helping me was fixing the display so it never shows that there were more or less attempts remaining then there should've been. An example of AI being incorrect towards helping me was the 'Easy' difficulty range of 1-20. At first it kept allowing the game to run the range 1-100 and would not change until I described the error. Through constently running the website and describing each error, I was able to have the AI assist me properly to solve the issue that I was having.  
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I made the decision of whether the bug was truly fixed through constantly viewing the website for errors, and being very thorough of each code that I was changing. I tested the pytest for the "New Game" button and when I would press it in the website, it would give me this traceback error. AI helped me design and understand the tests from correcting the ranges, correcting the attempts limit, making the "New Game" button actually work, etc. I also was able to use another platform like ChatGPT to explain specific errors to me that were not clicking for CoPilot.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number kept changing because Streamlit reruns the entire script every time the user interacts with the app. Since the number was being generated each run, it kept creating a new secret number. Streamlit reruns the whole program whenever something changes, like clicking a button or entering input. Session state lets the program remember values, like the secret number or score, so they don’t reset every time the app reruns. I stored the secret number in st.session_state so it is only created once and reused during the game. 

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse is adding comments and testing parts of the code step by step to find bugs more easily. Next time I would review the AI-generated code more carefully and test it earlier to catch logic errors sooner. This project showed me that AI can help generate code quickly, but it still needs to be checked and debugged by a developer.
