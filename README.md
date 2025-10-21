Ancient Rome Interactive
========================

**Ancient Rome Interactive** is an educational and engaging **Streamlit** app that lets users explore the daily life, culture, and responsibilities of various Roman roles. Users can learn through interactive chat and test their knowledge with role-specific quizzes.

Features
--------

**Learn Mode (🏺)**

*   Select a Roman role (e.g., Senator, Consul, Gladiator).
    
*   Chat with a role-specific bot to ask about life, work, holidays, and more.
    
*   Explore key topics for each role, including family, politics, military, and religion.
    

**Quiz Mode (📜)**

*   Take quizzes tailored to each Roman role.
    
*   Receive instant feedback on your answers.
    
*   Unlock a secret phrase by achieving a perfect score.
    

**Interactive UI**

*   Sidebar navigation for easy mode selection.
    
*   Toggle background music for immersive learning.
    
*   Background and styling designed for an authentic Roman experience.
    

Roman Roles Included
--------------------

*   Senator
    
*   Consul
    
*   Child
    
*   Slave
    
*   Gladiator
    
*   Legionary
    
*   Male Citizen
    
*   Female Citizen
    

Installation
------------

1.  Clone the repository:git clone [https://github.com/yourusername/romeapp.git](https://github.com/yourusername/romeapp.git) cd romeapp
    
2.  Install the required dependencies:pip install streamlit pillow
    
3.  Ensure the following files are present in the project folder:
    
    *   roman\_bg.png (background image)
        
    *   roman\_music.mp3 (optional background music)
        

Usage
-----

Run the app locally by typing:streamlit run app.py

*   Use the sidebar to toggle background music and switch between **Learn Mode** and **Quiz Mode**.
    
*   In **Learn Mode**, select a Roman role and ask questions to explore daily life, family, work, holidays, and more.
    
*   In **Quiz Mode**, select a role and answer multiple-choice questions to test your knowledge. Perfect scores reveal a secret phrase.
    

Notes
-----

*   Background music plays only if roman\_music.mp3 is in the project folder.
    
*   Chat and quiz progress are stored in the app’s session state, so you can continue where you left off.
