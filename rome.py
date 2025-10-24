import streamlit as st
from PIL import Image
import random
import io
import base64
import os

# Initialize session state
if "music_playing" not in st.session_state:
    st.session_state.music_playing = True

# Sidebar toggle
st.sidebar.markdown("🎵 **Background Music**")
toggle = st.sidebar.toggle("Play music", value=st.session_state.music_playing)

if toggle:
    st.session_state.music_playing = True
else:
    st.session_state.music_playing = False

# Load and play music if enabled
if st.session_state.music_playing:
    try:
        audio_file = open("roman_music.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    except FileNotFoundError:
        st.sidebar.warning("🎶 Music file not found: place 'roman_music.mp3' in this folder.")


books = {
    "Senator": [
        ("Senators were members of Rome's governing council.",
         "Where did the Senate usually meet?",
         ["Colosseum", "Curia", "Forum"], 1),
        ("They advised consuls and debated laws.",
         "How long did senators serve?",
         ["1 year", "10 years", "For life"], 2),
        ("Senators often controlled finances and provincial oversight.",
         "Which body often supervised Rome's finances and provinces?",
         ["Popular Assembly", "Senate", "Guilds"], 1),
        ("Senators often sponsored or oversaw major public festivals such as Saturnalia.",
         "Which December festival celebrated Saturn with feasting and role reversals?",
         ["Lupercalia", "Saturnalia", "Matronalia"], 1),
        ("Even soldiers enjoyed special holidays.",
         "Which spring festival saw Roman soldiers decorate their standards with roses?",
         ["Saturnalia", "Rosalia", "Lupercalia"], 1),
        ("Senators celebrated public holidays by sponsoring festivities for citizens.",
         "As a senator, what is one way I participate in holidays like Saturnalia?",
         ["By giving gifts and sponsoring games", "By fasting and staying home", "By leading armies"], 0),
        ("End of book!", None, None, None)
    ],
    "Consul": [
        ("Consuls were the highest elected officials in Rome.",
         "How many consuls served at the same time?",
         ["1", "2", "3"], 1),
        ("They led the army and the government.",
         "How long was a consul’s term?",
         ["1 year", "5 years", "For life"], 0),
        ("Consuls presided over assemblies and commanded troops in war.",
         "What special chair and escort symbolized a consul's office?",
         ["Curule chair and lictors", "Sella turcica and guards", "Curia and senators"], 0),
        ("Consuls participated in public festivals and state holidays.",
         "Which of the following is an activity a consul might do during Saturnalia?",
         ["Lead ceremonies and sacrifices", "Ignore citizens", "Train gladiators"], 0),
        ("End of book!", None, None, None)
    ],
    "Child": [
        ("Roman children learned Latin, Greek, and math.",
         "Where did wealthy children study?",
         ["At home", "Public schools", "Libraries"], 0),
        ("Boys often prepared for public life; girls for marriage.",
         "What age did Roman boys usually become adults?",
         ["Around 10", "Around 15-16", "Around 20"], 1),
        ("Children from elite families had tutors and learned rhetoric.",
         "What subject was especially important for boys who planned public careers?",
         ["Rhetoric", "Carpentry", "Painting"], 0),
        ("Children enjoyed festivals and holidays.",
         "Which holiday might a Roman child celebrate with games and treats?",
         ["Saturnalia", "Caristia", "Both"], 2),
        ("End of book!", None, None, None)
    ],
    "Slave": [
        ("Slaves were common in Roman households, farms, and mines.",
         "How did most slaves come to Rome?",
         ["Born into slavery", "Captured in war", "Volunteered"], 1),
        ("Some slaves could be freed (manumitted).",
         "What was a freed slave called?",
         ["Libertus", "Servus", "Civis"], 0),
        ("Slaves had many origins: others were born into slavery, some were prisoners of war — I was born into slavery.",
         "Which of these was a legal path for a slave to become free?",
         ["Earning or buying freedom (manumission)", "Voting in assemblies", "Being elected consul"], 0),
        ("Slaves sometimes enjoyed small benefits during holidays.",
         "Which holiday might give a slave a gift or day of rest?",
         ["Saturnalia", "Lupercalia", "Matronalia"], 0),
        ("End of book!", None, None, None)
    ],
    "Gladiator": [
        ("Gladiators fought for entertainment in arenas.",
         "What was the Colosseum’s Latin name?",
         ["Amphitheatrum", "Forum", "Circus"], 0),
        ("They trained in schools called ludi.",
         "What was the referee of a gladiator fight called?",
         ["Editor", "Lanista", "Doctore"], 1),
        ("Gladiators followed strict diets and medical care to stay fit.",
         "Which diet element was common for many gladiators?",
         ["High-protein meat diet", "High-energy vegetarian diet (barley/beans)", "Only fruit"], 1),
        ("Gladiators often performed during public holidays.",
         "During which festival might gladiators fight in larger crowds?",
         ["Saturnalia", "Lupercalia", "Matronalia"], 0),
        ("End of book!", None, None, None)
    ],
    "Legionary": [
        ("Legionaries were Rome’s professional soldiers.",
         "How long did a legionary usually serve?",
         ["2 years", "10 years", "25 years"], 2),
        ("They carried a short sword called a gladius.",
         "What was their large rectangular shield called?",
         ["Scutum", "Pelta", "Aspis"], 0),
        ("Legionaries trained daily, built infrastructure, and used pila and gladius in battle.",
         "Which two weapons gave Roman legions flexibility in battle?",
         ["Pilum and gladius", "Spear and longbow", "Axe and mace"], 0),
        ("Legionaries decorated standards during holidays.",
         "Which festival involved legionaries adorning their standards with flowers?",
         ["Rosalia", "Saturnalia", "Caristia"], 0),
        ("End of book!", None, None, None)
    ],
    "Male Citizen": [
        ("Roman male citizens had rights like voting and owning property.",
         "Who could become a Roman citizen?",
         ["Only Patricians", "Only Italians", "Men and some outsiders"], 2),
        ("Citizens wore togas as a mark of status.",
         "What special toga did boys wear?",
         ["Toga praetexta", "Toga virilis", "Toga candida"], 0),
        ("Male citizens were expected to serve in the army and participate politically.",
         "Which duty was expected of many male citizens?",
         ["Military service", "Becoming a gladiator", "Joining the Senate automatically"], 0),
        ("Male citizens participated fully in public holidays.",
         "Which of the following might a male citizen do during Saturnalia?",
         ["Give gifts, attend games, and feast", "Stay home quietly", "Ignore laws"], 0),
        ("End of book!", None, None, None)
    ],
    "Female Citizen": [
        ("Roman women were citizens but could not vote or hold office.",
         "What was a common role for Roman women?",
         ["Priestess", "Senator", "Consul"], 0),
        ("Wealthy women managed households and owned property.",
         "What garment did Roman women wear?",
         ["Tunic", "Stola", "Toga"], 1),
        ("Women could own property and sometimes influence politics through family ties.",
         "Which of the following is true about Roman women?",
         ["They could never own property", "They could own property in some cases", "They could vote"], 1),
        ("Roman women celebrated Matronalia each March to honor mothers and wives.",
         "Which goddess was Matronalia dedicated to?",
         ["Venus", "Iuno", "Minerva"], 1),
        ("Women participated in public holidays and family festivals.",
         "During which holiday might women dress specially and celebrate with family?",
         ["Matronalia", "Lupercalia", "Caristia"], 0),
        ("End of book!", None, None, None)
    ]
}

key_words = {
    "Senator": "Tampa (1st word in secret phrase)",
    "Consul": "Prep (2nd word in secret phrase)",
    "Child": "Students (3rd word in secret phrase)",
    "Slave": "Love (4th word in secret phrase)",
    "Gladiator": "To (5th word in secret phrase)",
    "Legionary": "Learn (6th word in secret phrase)",
    "Male Citizen": "About (7th word in secret phrase)",
    "Female Citizen": "Rome (8th word in secret phrase)"
}

chatbot_facts = {
    "Senator": {
        "life": "I serve for life in the Roman Senate, the most powerful council in the Republic and Empire. We senators are men of wealth and heritage, usually from noble patrician families. Our position brings honor and influence, but also duty to maintain Rome’s stability.",
        "family": "Most senators come from elite Roman families. Sons often follow their fathers into politics after gaining military or legal experience. Family alliances, marriages, and patronage shape our political success.",
        "work": "Our daily work involves debating laws, advising consuls, and managing state finances. We meet in the Curia within the Roman Forum to vote on policies that affect every citizen and province.",
        "food": "We enjoy lavish meals of roasted meats, seafood, and imported delicacies like dates and figs from across the Empire. Wine flows freely at our banquets.",
        "clothing": "I wear a toga with a broad purple stripe — the latus clavus — marking my senatorial rank. Only members of the Senate are permitted this distinction.",
        "politics": "The Senate is the heart of Roman politics. We manage provincial governors, control the treasury, and often guide or challenge the consuls’ decisions.",
        "games": "Public games and gladiatorial shows are part of our duty to sponsor. They please the people and show our generosity.",
        "power": "Our influence over law and government decisions gives us immense power, especially in the Republic era.",
        "law": "We help draft decrees and shape legislation — the senatus consultum — which guides Rome’s magistrates.",
        "holidays": "As a senator, I help oversee public festivals like Saturnalia and Lupercalia. I ensure the ceremonies honor the gods and delight the citizens, including banquets, games, and feasts where social roles may be reversed."
    },
    "Consul": {
        "life": "I am one of two consuls, the highest magistrates of the Roman Republic. My co-consul and I share power equally to prevent tyranny. We command armies, preside over the Senate, and enforce the laws.",
        "family": "Only those from the most prestigious families can rise to the consulship. Many of us come from generations of statesmen, but some new men — novi homines — reach this rank through ambition and talent.",
        "work": "We oversee Rome’s administration and lead armies in war. We also chair the Senate and direct public business. Every year, two consuls are elected by the citizens.",
        "food": "At feasts, we eat fine bread, meats, cheeses, and fruits while entertaining ambassadors and dignitaries.",
        "clothing": "I wear the toga praetexta, edged with purple, and am accompanied by twelve lictors carrying fasces, symbols of my authority.",
        "politics": "We are elected by the people but often serve the interests of the Senate and aristocracy. Power is always shared to ensure balance.",
        "religion": "We perform major state rituals, offering sacrifices to Jupiter and Mars before battle or ceremonies.",
        "military": "We command Rome’s legions in war, sometimes gaining great glory and triumphal parades upon returning victorious.",
        "election": "Each year, citizens vote for new consuls in the Comitia Centuriata assembly. Few achieve this rank twice in their lifetime.",
        "holidays": "As a consul, I take part in state festivals like Lupercalia and Saturnalia, performing ceremonies and sacrifices to honor the gods. These holidays allow the people to celebrate, relax, and participate in public games."
    },
    "Child": {
        "life": "As a Roman child, my days are filled with learning and family duties. Boys and girls grow up differently — boys train for citizenship and girls for marriage and household management.",
        "family": "Family is the center of Roman life. My father, the paterfamilias, has authority over us all, but my mother guides my upbringing with care and discipline.",
        "work": "Children rarely work, but we are taught discipline, respect, and Roman virtues. Wealthy families prepare their sons for politics or law.",
        "food": "I eat bread, cheese, olives, and fruit. Honey is a rare treat! Meals are simple but nourishing.",
        "education": "If we are wealthy, tutors teach us Latin, Greek, arithmetic, history, and rhetoric. Poor children learn trades from parents instead.",
        "games": "I love to play with dolls, hoops, knucklebones, or marbles. Some of us even stage mock battles or races!",
        "clothing": "I wear a tunic, and boys wear a bulla (a protective charm) until they become adults.",
        "rites": "When I come of age — around 15 — I exchange my child’s toga praetexta for the toga virilis and am presented at the Forum.",
        "school": "We learn reading and writing with wax tablets and styluses, repeating lessons aloud to memorize them.",
        "holidays": "I enjoy festivals like Saturnalia, Matronalia, and Caristia. These holidays mean days off from school, treats, games, and family gatherings, and sometimes I help decorate our home or watch public celebrations."
    },
    "Slave": {
        "life": "I am a slave in Rome. My days depend on my master’s will — I might clean, cook, farm, or work in workshops and mines. Some slaves serve in wealthy homes, others labor in terrible conditions underground or on ships.",
        "family": "I have little legal right to family, but among other slaves we form strong emotional bonds. Some masters allow marriages or children, though the law considers them the master’s property.",
        "work": "I serve from dawn until night. In a household, I might be a tutor, cook, cleaner, or secretary. Skilled slaves — like teachers and artisans — are valuable and often treated better.",
        "food": "Our meals are simple: bread, porridge, olives, and sometimes scraps from the master’s table.",
        "freedom": "If I am loyal and skilled, I may be manumitted — freed — to become a libertus, a freedman. Freed slaves can work for pay and even prosper.",
        "punishment": "Disobedience brings harsh punishment, from beatings to being sold. Some masters, however, show fairness or affection.",
        "religion": "I worship the same gods as my master. In hardship, faith gives us hope.",
        "origin": "Others were born into slavery, some were prisoners of war — I was born into slavery. Rome’s conquests bring many foreigners into bondage.",
        "rights": "As a slave I have no legal rights, but if freed, I gain limited citizenship and can raise my own family.",
        "holidays": "Even as a slave, I notice when the city celebrates. During Saturnalia or Caristia, I may get small gifts or some freedom, and I enjoy the rare chance to rest, eat well, and celebrate with my master or family."
    },
    "Gladiator": {
        "life": "I train daily to fight before cheering crowds. Glory and death walk side by side in the arena. Though once a slave, I can earn fame and sometimes even freedom.",
        "family": "Most of us were slaves, prisoners, or criminals, though a few free men join voluntarily for money and fame. We live together in training schools called ludi.",
        "work": "Fighting is my work — my life. I practice swordsmanship, endurance, and tactics under the watch of my lanista.",
        "food": "We eat a high-energy vegetarian diet of barley, beans, and dried fruit — it builds muscle and protects us from wounds.",
        "training": "We train with wooden swords before facing real combat. The best among us learn special fighting styles: murmillo, retiarius, or secutor.",
        "games": "Our matches are part of festivals and political events. The crowds chant our names — victory means honor; defeat may mean death.",
        "death": "Death is common, but a skilled or merciful fighter may be spared by the crowd’s gesture — thumbs up or down.",
        "weapons": "Each gladiator has a class and weapon — sword and shield, net and trident, or spear and armor.",
        "ludi": "The ludus is both prison and home. We train, eat, and dream there, hoping to see another sunrise.",
        "holidays": "Many of our fights coincide with public holidays like Saturnalia or Ludi Romani. The crowds are larger, and the celebrations make our victories more glorious, though the danger is even greater."
    },
    "Legionary": {
        "life": "I am a professional soldier of Rome, serving 25 years for glory and citizenship. Discipline rules every part of my life.",
        "family": "I leave my family behind while I serve. After retirement, I may receive land and settle as a farmer or veteran colonist.",
        "work": "Beyond fighting, we build roads, forts, and aqueducts. Our engineering skills spread Roman civilization everywhere.",
        "food": "We eat coarse bread, cheese, and porridge, washed down with vinegar wine. Simplicity keeps us strong.",
        "weapons": "My main arms are the pilum — a heavy javelin — and the gladius, a short sword. Our rectangular scutum shields protect us in close formation.",
        "training": "We train constantly — running in armor, throwing pila, and sparring daily. Only the toughest endure.",
        "clothing": "We wear iron armor, a red tunic, sandals with nails, and a crested helmet. The uniform is both protection and pride.",
        "service": "Our service lasts 25 years. Some die in battle; others retire with honor and land.",
        "discipline": "Strict obedience keeps us unbeatable. Cowardice or desertion is punished by death, but loyalty earns lifelong respect.",
        "holidays": "We soldiers honor festivals like Rosalia and Saturnalia. Even while on campaign, we decorate our standards with flowers and take time to rest, eat, and celebrate briefly with comrades."
    },
    "Male Citizen": {
        "life": "As a Roman citizen, I enjoy rights and duties unknown to foreigners. I can vote, marry legally, and appeal to Roman courts.",
        "family": "As paterfamilias, I am head of my household, with authority over my wife, children, and slaves. My reputation reflects upon them.",
        "work": "I may farm my land, trade goods, or practice law or politics. All citizens contribute to Rome’s greatness.",
        "food": "I eat bread, olives, cheese, and wine daily. Wealthy men enjoy meats and imported fruits.",
        "clothing": "I wear a toga — a symbol of citizenship — over a tunic. Only citizens may wear it in public assemblies.",
        "education": "I studied rhetoric, philosophy, and law to prepare for public life. Clear speech is a citizen’s weapon.",
        "politics": "I vote in assemblies and can run for office. My voice helps shape Rome’s laws and destiny.",
        "rights": "As a citizen, I’m protected from torture and can only be judged by Roman law.",
        "holidays": "I enjoy public holidays like Lupercalia, Caristia, Matronalia, and Saturnalia. These days are for family gatherings, feasting, and games. I participate fully, sometimes giving gifts or joining in the revelry and decorations."
    },
    "Female Citizen": {
        "life": "As a Roman woman, I am a citizen but cannot vote or hold public office. My life centers on family, household management, and religious duties. My reputation and virtue reflect on my family’s honor.",
        "family": "Family is the foundation of Roman life. I owe obedience to my father or husband, yet within the home, I manage servants, finances, and daily affairs. Wealthy women often oversee large estates and host social gatherings.",
        "work": "Most women work within the home, spinning, weaving, or managing domestic tasks. Wealthier women supervise slaves, while poorer women may sell goods in markets or assist in family businesses.",
        "food": "My meals are simple—bread, olives, cheese, and fruit. On special occasions, we enjoy meats or sweets. Women prepare and oversee food for the household, ensuring offerings are made to the household gods.",
        "clothing": "I wear a long tunic beneath a stola, a garment that shows my status as a respectable married woman. For public outings, I cover myself with a palla, a cloak draped gracefully over the shoulders.",
        "religion": "Religion fills my life. I honor the household gods, Lares and Penates, and take part in festivals like Matronalia, which celebrates mothers and wives in honor of the goddess Iuno.",
        "education": "Girls learn reading, writing, and household management. Wealthy women may study literature or philosophy at home, though formal education focuses more on preparing us to manage households and uphold family virtue.",
        "rights": "As a woman, I am a Roman citizen but cannot vote or serve in office. However, I can own property, make wills, and manage dowries. Influential women sometimes shape politics indirectly through family ties.",
        "marriage": "Marriage joins families and secures alliances. A wife brings a dowry, manages the home, and bears children. In some forms of marriage, I remain under my father’s authority; in others, my husband becomes my legal guardian.",
        "holidays": "I celebrate festivals such as Matronalia, when husbands give gifts to wives and mothers. During Caristia, families reunite to honor love and harmony. Women join in public feasts and wear festive clothing on such days."
    }
}

keywords_intro = {
    "Senator": ["life", "family", "work", "food", "clothing", "politics", "games", "power", "law", "holidays"],
    "Consul": ["life", "family", "work", "food", "clothing", "politics", "religion", "military", "election", "holidays"],
    "Child": ["life", "family", "work", "food", "education", "games", "clothing", "rites", "school", "holidays"],
    "Slave": ["life", "family", "work", "food", "freedom", "punishment", "religion", "origin", "rights", "holidays"],
    "Gladiator": ["life", "family", "work", "food", "training", "games", "death", "weapons", "ludi", "holidays"],
    "Legionary": ["life", "family", "work", "food", "weapons", "training", "clothing", "service", "discipline", "holidays"],
    "Male Citizen": ["life", "family", "work", "food", "clothing", "education", "politics", "rights", "duties", "holidays"],
    "Female Citizen": ["life", "family", "work", "food", "clothing", "religion", "education", "rights", "marriage", "holidays"]
}


# --- STREAMLIT APP START ---

st.set_page_config(page_title="Ancient Rome Interactive", layout="centered")

# Background / Title
st.markdown(
    """
    <style>
    /* Main app area */
    .stApp {
        background-color: #8B0000;
        color: #000000;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #D4AF37;
        color: #000000;
    }

    /* Top menu & hamburger */
    header, .css-18e3th9 {
        background-color: #8e001c;
    }

    /* Optional: buttons, selects, etc. text color */
    .stButton>button, .stSelectbox>div, .stRadio>div {
        color: #000000;
    }

    button[kind="primary"], button {
        background-color: #c8b39b !important;
        color: black !important;
        border: none !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("roman_bg.jpg", use_container_width=True)
st.title("🏛 The Voice of Rome")
st.markdown("Welcome to Ancient Rome! Learn, chat, and test your knowledge.")

# Sidebar navigation
mode = st.sidebar.radio("Choose Mode", ["🏺 Learn", "📜 Quiz"])
st.sidebar.markdown("Toggle between learning and quiz modes.")

# Keep session state for quiz/chat progress
if "role" not in st.session_state:
    st.session_state.role = None
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []


# ============== LEARN MODE ==============
if mode == "🏺 Learn":
    st.header("Learn About Roman Society")

    role = st.selectbox("Select a Roman Role:", list(chatbot_facts.keys()))
    st.session_state.role = role

    st.markdown(f"### You are talking to a {role}")
    st.markdown(f"Ask about: `{', '.join(keywords_intro[role])}`")

    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    def send_message():
        user_message = st.session_state.user_input.strip()
        if user_message:
            st.session_state.chat_log.append(("user", user_message))
            matched = [k for k in chatbot_facts[role] if k in user_message.lower()]
            if matched:
                reply = chatbot_facts[role][matched[0]]
            else:
                reply = "I’m not sure about that — make sure you include one of the keywords listed above in your question."
            st.session_state.chat_log.append(("bot", reply, role))
            st.session_state.user_input = ""

    chat_container = st.container()
    for item in st.session_state.chat_log:
        if item[0] == "user":
            chat_container.markdown(f"**You:** {item[1]}")
        else:
            chat_container.markdown(f"**{item[2]}:** {item[1]}")

    st.text_input(
        "Ask me something...",
        key="user_input",
        placeholder="Type your question here...",
        on_change=send_message
    )

    st.button("Send", on_click=send_message)
    st.button("Clear Conversation", on_click=lambda: st.session_state.chat_log.clear())




# ============== QUIZ MODE ==============
elif mode == "📜 Quiz":
    st.header("Roman Role Quiz")

    role = st.selectbox("Select a role for your quiz:", list(books.keys()))
    st.session_state.role = role

    if st.button("Start Quiz"):
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.rerun()

    # Load quiz if started
    if st.session_state.quiz_index < len(books[role]):
        q = books[role][st.session_state.quiz_index]
        if q[1] is None:
            st.session_state.quiz_index = len(books[role])
            st.rerun()
        else:
            text, question, options, correct_index = q
            st.write(f"**{text}**")
            st.subheader(question)

            choice = st.radio("Your answer:", options, key=f"q{st.session_state.quiz_index}")
            if st.button("Submit Answer"):
                if options.index(choice) == correct_index:
                    st.success("✅ Correct!")
                    st.session_state.quiz_score += 1
                else:
                    st.error("❌ Incorrect!")
                st.session_state.quiz_index += 1
                st.rerun()

    else:
        total = len([q for q in books[role] if q[1] is not None])
        score = st.session_state.quiz_score
        if score == total:
            st.success(f"🎉 You scored {score}/{total}! Secret phrase: {key_words[role]}")
        else:
            st.warning(f"You scored {score}/{total}. Try again for the secret phrase!")

        if st.button("Restart Quiz"):
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.rerun()
