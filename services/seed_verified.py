"""
Seed the Verified ChromaDB collection with comprehensive examination papers.

Coverage (Pakistan boards ONLY):
  Pakistan > Punjab Boards  > Class 9, 10, 11, 12
  Pakistan > Federal Board  > Class 9, 10, 11, 12
  Pakistan > Cambridge      > O Level, A Level

Subjects: Mathematics, Physics, Chemistry, Biology, Computer Science,
          English, Urdu, Islamiat, Pakistan Studies

Each question is stored as a SEPARATE vector with full metadata.
Run automatically on startup (idempotent) or manually:
    python -m services.seed_verified
"""

import os
import json
import datetime
import hashlib
from typing import List, Dict

_DATA_PATH  = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mock_data.json")
_TIMESTAMP  = datetime.datetime.utcnow().isoformat()


# ═══════════════════════════════════════════════════════════════════════════════
# Seed data — every question becomes one ChromaDB vector
# ═══════════════════════════════════════════════════════════════════════════════

SEED_PAPERS: List[Dict] = [

    # ══════════════════════════════════════════════════════════════════════════
    # PAKISTAN > PUNJAB BOARDS > CLASS 9
    # ══════════════════════════════════════════════════════════════════════════

    # ── Class 9 > Physics ────────────────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Physics", "paper_id": "pk_punjab_c9_phy_01",
        "mcqs": [
            "The SI unit of force is: A) Newton  B) Joule  C) Watt  D) Pascal",
            "A body moving with uniform velocity has: A) Zero acceleration  B) Increasing acceleration  C) Decreasing acceleration  D) Constant non-zero acceleration",
            "The speed of sound in air at 0°C is approximately: A) 332 m/s  B) 500 m/s  C) 300 m/s  D) 450 m/s",
            "Which of the following is a scalar quantity? A) Force  B) Velocity  C) Speed  D) Momentum",
            "The unit of pressure is: A) Pascal  B) Newton  C) Joule  D) Ampere",
            "Which law states that action and reaction are equal and opposite? A) Newton's 1st Law  B) Newton's 2nd Law  C) Newton's 3rd Law  D) Law of Gravitation",
            "The instrument used to measure atmospheric pressure is: A) Barometer  B) Thermometer  C) Manometer  D) Hydrometer",
            "Work done is zero when force and displacement are: A) Parallel  B) Anti-parallel  C) Perpendicular  D) Equal",
            "The SI unit of power is: A) Watt  B) Joule  C) Newton  D) Pascal",
            "The pitch of a sound depends on its: A) Frequency  B) Amplitude  C) Speed  D) Wavelength",
        ],
        "short_questions": [
            "Define Newton's First Law of Motion. Give one example from daily life.",
            "What is the difference between mass and weight? Give their SI units.",
            "State the law of conservation of momentum with a mathematical expression.",
            "Define work done and write its SI unit. When is work done zero?",
            "What is meant by the centre of gravity? Why is it important?",
            "Differentiate between speed and velocity with examples.",
            "Define kinetic energy and write its formula.",
            "What is Archimedes' Principle? State its one application.",
        ],
        "long_questions": [
            "State and explain Newton's Three Laws of Motion with real-life examples. Derive the relationship F = ma from Newton's Second Law.",
            "Explain the concept of energy. Describe the different forms of energy and state the Law of Conservation of Energy with an example.",
            "Define pressure in liquids. Derive an expression for liquid pressure at a depth h. Explain Pascal's Law and its applications.",
        ],
    },
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Physics", "paper_id": "pk_punjab_c9_phy_02",
        "mcqs": [
            "Gravitational potential energy depends on: A) Height  B) Speed  C) Temperature  D) Density",
            "A wave that requires a material medium to travel is called: A) Mechanical wave  B) Electromagnetic wave  C) Radio wave  D) Light wave",
            "The bending of light when passing from one medium to another is called: A) Reflection  B) Refraction  C) Diffraction  D) Interference",
            "Which mirror is used in a car's rear-view mirror? A) Plane mirror  B) Convex mirror  C) Concave mirror  D) Parabolic mirror",
            "The unit of frequency is: A) Hertz  B) Decibel  C) Metre  D) Second",
        ],
        "short_questions": [
            "Define refraction of light. State Snell's Law.",
            "What is meant by total internal reflection? State its conditions.",
            "Define simple harmonic motion (SHM). Give two examples.",
            "What is the difference between longitudinal and transverse waves?",
            "State Hooke's Law and write its mathematical form.",
        ],
        "long_questions": [
            "What is reflection of light? State the laws of reflection. Describe the image formed by a plane mirror and a concave mirror for different positions of the object.",
            "Explain the working of a simple pendulum. Derive an expression for its time period and state the factors that affect it.",
        ],
    },

    # ── Class 9 > Chemistry ───────────────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Chemistry", "paper_id": "pk_punjab_c9_chem_01",
        "mcqs": [
            "The atomic number of an element represents the number of: A) Protons  B) Neutrons  C) Electrons in outer shell  D) Nucleons",
            "Which of the following is a noble gas? A) Neon  B) Chlorine  C) Sodium  D) Oxygen",
            "The chemical formula of water is: A) H2O  B) H2O2  C) HO  D) HO2",
            "Isotopes of an element have the same: A) Atomic number  B) Mass number  C) Number of neutrons  D) Atomic mass",
            "The pH of a neutral solution is: A) 7  B) 0  C) 14  D) 1",
            "Which type of bond is formed by the transfer of electrons? A) Ionic bond  B) Covalent bond  C) Metallic bond  D) Hydrogen bond",
            "The process of converting ore into metal is called: A) Smelting  B) Roasting  C) Reduction  D) Oxidation",
            "Avogadro's number is: A) 6.022 × 10²³  B) 6.022 × 10²⁴  C) 3.011 × 10²³  D) 1.204 × 10²⁴",
        ],
        "short_questions": [
            "Define atomic number and mass number. How do they differ?",
            "What are isotopes? Give two examples with their uses.",
            "Differentiate between ionic and covalent bonds with one example each.",
            "Define the mole concept. How many atoms are in 2 moles of carbon?",
            "What is the difference between an acid and a base? Give examples.",
            "State the periodic law and explain how elements are arranged in the periodic table.",
        ],
        "long_questions": [
            "Explain the structure of the atom. Describe Bohr's atomic model and its postulates. What are its limitations?",
            "Describe the ionic bond formation between sodium and chlorine. Explain the properties of ionic compounds.",
            "What is chemical equilibrium? State Le Chatelier's Principle and explain how temperature, pressure, and concentration affect equilibrium.",
        ],
    },

    # ── Class 9 > Biology ─────────────────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Biology", "paper_id": "pk_punjab_c9_bio_01",
        "mcqs": [
            "The powerhouse of the cell is: A) Mitochondria  B) Nucleus  C) Ribosome  D) Chloroplast",
            "Photosynthesis occurs in: A) Chloroplast  B) Mitochondria  C) Ribosome  D) Nucleus",
            "The basic structural and functional unit of life is: A) Cell  B) Tissue  C) Organ  D) Organism",
            "DNA stands for: A) Deoxyribonucleic acid  B) Diribonucleic acid  C) Deoxyribonicotinic acid  D) Diribose nucleic acid",
            "Which blood group is the universal donor? A) O  B) A  C) B  D) AB",
            "The process by which plants make their own food using sunlight is: A) Photosynthesis  B) Respiration  C) Transpiration  D) Digestion",
            "Chromosomes are found in: A) Nucleus  B) Cytoplasm  C) Ribosome  D) Vacuole",
            "The study of living organisms is called: A) Biology  B) Chemistry  C) Physics  D) Geology",
        ],
        "short_questions": [
            "What is the difference between prokaryotic and eukaryotic cells?",
            "Define osmosis and diffusion. How do they differ?",
            "What are enzymes? Explain their role in digestion.",
            "Describe the structure of a plant cell and an animal cell.",
            "What is mitosis? Briefly describe its stages.",
            "Explain the importance of photosynthesis for life on Earth.",
        ],
        "long_questions": [
            "Describe the process of photosynthesis in detail. Write the chemical equation for photosynthesis. Explain the light-dependent and light-independent reactions.",
            "What is cellular respiration? Compare aerobic and anaerobic respiration with examples and chemical equations.",
            "Explain the levels of biological organization from cell to organism. Give examples of each level.",
        ],
    },

    # ── Class 9 > Mathematics ─────────────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Mathematics", "paper_id": "pk_punjab_c9_math_01",
        "mcqs": [
            "The solution of the equation 2x + 4 = 10 is: A) x = 3  B) x = 7  C) x = 2  D) x = 5",
            "The value of sin 30° is: A) 1/2  B) √3/2  C) 1/√2  D) 1",
            "If a set has 5 elements, the number of subsets is: A) 32  B) 25  C) 10  D) 16",
            "The distance formula between two points (x₁,y₁) and (x₂,y₂) is: A) √[(x₂-x₁)² + (y₂-y₁)²]  B) [(x₂-x₁) + (y₂-y₁)]  C) (x₂-x₁)² + (y₂-y₁)²  D) √(x₂+y₂)",
            "The sum of angles in a triangle is: A) 180°  B) 360°  C) 90°  D) 270°",
            "Which of the following is a rational number? A) √2  B) π  C) 3/4  D) √3",
            "The slope of a horizontal line is: A) 0  B) 1  C) Undefined  D) -1",
            "A quadratic equation has degree: A) 2  B) 1  C) 3  D) 0",
        ],
        "short_questions": [
            "Define a set and give two examples. What is the difference between a finite and infinite set?",
            "Solve the quadratic equation x² - 5x + 6 = 0 by factorization.",
            "Prove that the sum of all angles of a triangle is 180°.",
            "Find the distance between the points A(3, 4) and B(0, 0).",
            "Define a function. Give an example and identify its domain and range.",
            "What is the Pythagoras theorem? Write it mathematically and state its converse.",
        ],
        "long_questions": [
            "Define logarithm. State and prove the laws of logarithm. Use logarithms to evaluate: log₂ 8 + log₂ 4.",
            "Prove that the line segment joining the midpoints of two sides of a triangle is parallel to the third side and equal to half its length.",
            "Explain algebraic expressions and factorization. Factorize: 4x² - 9, 6x² + 7x - 3, and a³ + b³.",
        ],
    },

    # ── Class 9 > Computer Science ────────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Computer Science", "paper_id": "pk_punjab_c9_cs_01",
        "mcqs": [
            "Which of the following is an input device? A) Keyboard  B) Monitor  C) Printer  D) Speaker",
            "The full form of CPU is: A) Central Processing Unit  B) Computer Processing Unit  C) Control Processing Unit  D) Central Program Unit",
            "Binary number system uses: A) 2 digits  B) 8 digits  C) 10 digits  D) 16 digits",
            "The language directly understood by a computer is: A) Machine language  B) Assembly language  C) C++  D) Python",
            "1 Byte = ? Bits: A) 8  B) 4  C) 16  D) 2",
            "RAM stands for: A) Random Access Memory  B) Read Access Memory  C) Read Arithmetic Memory  D) Random Arithmetic Memory",
            "Which of the following is an example of system software? A) Operating System  B) MS Word  C) Adobe Photoshop  D) VLC Player",
        ],
        "short_questions": [
            "What is the difference between hardware and software? Give two examples of each.",
            "Define an algorithm. Write an algorithm to find the largest of three numbers.",
            "What is the difference between RAM and ROM?",
            "Convert the binary number 1011₂ to decimal.",
            "Define a flowchart. What are its advantages in programming?",
            "What is an operating system? Name three popular operating systems.",
        ],
        "long_questions": [
            "Describe the generations of computers. What are the characteristics of each generation?",
            "Explain the number systems: binary, octal, decimal, and hexadecimal. Convert 25 (decimal) to binary, octal, and hexadecimal.",
            "What is a programming language? Describe the types of programming languages with examples and their advantages and disadvantages.",
        ],
    },

    # ── Class 9 > English ─────────────────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "English", "paper_id": "pk_punjab_c9_eng_01",
        "mcqs": [
            "Which of the following is a noun? A) Run  B) Beautiful  C) Happiness  D) Quickly",
            "The plural of 'child' is: A) Childs  B) Children  C) Childes  D) Childrens",
            "Which sentence is in the passive voice? A) She wrote the letter  B) The letter was written by her  C) She is writing the letter  D) She will write the letter",
            "A word that modifies a verb is called: A) Adjective  B) Adverb  C) Noun  D) Preposition",
            "Choose the correct article: ___ apple a day keeps the doctor away. A) A  B) An  C) The  D) No article",
        ],
        "short_questions": [
            "Write a paragraph of 80–100 words on 'The Importance of Education'.",
            "Use the following words in your own sentences: perseverance, diligent, benevolent.",
            "Change the following sentences from active to passive voice: (a) The teacher taught the lesson. (b) She is reading a book.",
            "Write a dialogue between two friends discussing their plans for summer vacation.",
            "What is a metaphor? Give two examples from literature.",
        ],
        "long_questions": [
            "Write an essay of about 250 words on 'Science and Technology in Modern Life'. Include an introduction, body paragraphs, and a conclusion.",
            "Read the following passage and answer the questions: [A passage on environmental conservation]. (a) What is the main idea? (b) What solutions are suggested? (c) What does the word 'conservation' mean?",
        ],
    },

    # ── Class 9 > Islamiat ────────────────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Islamiat", "paper_id": "pk_punjab_c9_isl_01",
        "mcqs": [
            "The first revelation of the Holy Quran was revealed in: A) Cave Hira  B) Cave Thaur  C) Masjid al-Haram  D) Madinah",
            "The number of Surahs in the Holy Quran is: A) 114  B) 100  C) 120  D) 110",
            "Salat is obligatory for Muslims: A) 5 times a day  B) 3 times a day  C) 7 times a day  D) Once a day",
            "The Hijri calendar is based on: A) Lunar calendar  B) Solar calendar  C) Both  D) Julian calendar",
            "Zakat is obligatory on savings held for: A) One lunar year  B) One solar year  C) Six months  D) Two years",
        ],
        "short_questions": [
            "What are the Five Pillars of Islam? Briefly explain each.",
            "Define Iman. What are the articles of faith in Islam?",
            "Write a note on the importance of Salat in a Muslim's life.",
            "Who is a Prophet? What qualities did the Holy Prophet (PBUH) possess?",
            "What is the significance of the month of Ramadan in Islam?",
        ],
        "long_questions": [
            "Write a detailed note on the life of the Holy Prophet Muhammad (PBUH) before prophethood. What qualities made him an ideal human being?",
            "Explain the importance of the Holy Quran in the life of a Muslim. How should a Muslim follow its teachings in daily life?",
        ],
    },

    # ── Class 9 > Pakistan Studies ────────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Pakistan Studies", "paper_id": "pk_punjab_c9_pst_01",
        "mcqs": [
            "Pakistan came into existence on: A) 14 August 1947  B) 23 March 1940  C) 14 August 1948  D) 14 August 1946",
            "The first Governor General of Pakistan was: A) Quaid-e-Azam  B) Liaquat Ali Khan  C) Ayub Khan  D) Iskander Mirza",
            "The capital of Pakistan is: A) Islamabad  B) Lahore  C) Karachi  D) Rawalpindi",
            "The highest peak in Pakistan is: A) K-2  B) Nanga Parbat  C) Tirich Mir  D) Rakaposhi",
            "Which river passes through Lahore? A) Ravi  B) Chenab  C) Jhelum  D) Sutlej",
            "The Lahore Resolution was passed in: A) 1940  B) 1930  C) 1945  D) 1935",
        ],
        "short_questions": [
            "Write a short note on the Two-Nation Theory.",
            "What are the main features of the geography of Pakistan?",
            "Who was Quaid-e-Azam? Write five qualities of his personality.",
            "Describe the main rivers of Pakistan and their economic importance.",
            "What is the significance of the 23rd March (Pakistan Day)?",
        ],
        "long_questions": [
            "Describe the role of Quaid-e-Azam Muhammad Ali Jinnah in the creation of Pakistan. How did he unite the Muslims of the subcontinent?",
            "Explain the climate of Pakistan. What are the major climatic regions? How does climate affect agriculture?",
        ],
    },

    # ── Class 9 > Urdu ────────────────────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Urdu", "paper_id": "pk_punjab_c9_urdu_01",
        "mcqs": [
            "اردو زبان کا موجد کسے کہا جاتا ہے؟ الف) امیر خسرو  ب) میر تقی میر  ج) غالب  د) اقبال",
            "غزل کا آخری شعر کہلاتا ہے: الف) مقطع  ب) مطلع  ج) ردیف  د) قافیہ",
            "اردو کا پہلا ناول کون سا ہے؟ الف) مراۃ العروس  ب) امراؤ جان ادا  ج) توبۃ النصوح  د) فسانۂ آزاد",
            "نظم میں ہر مصرع کے آخر میں ایک ہی قافیہ ہو تو اسے کہتے ہیں: الف) مسلسل نظم  ب) ہر بند نظم  ج) قصیدہ  د) غزل",
        ],
        "short_questions": [
            "اردو زبان کی تاریخ مختصراً بیان کریں۔",
            "غزل اور نظم میں فرق بیان کریں۔",
            "علامہ اقبال کی شاعری کا موضوع بیان کریں۔",
            "درج ذیل محاورات کے جملوں میں استعمال کریں: ہاتھ پاؤں مارنا، آنکھیں کھلنا۔",
        ],
        "long_questions": [
            "اردو ادب میں مرزا غالب کے مقام و مرتبے پر روشنی ڈالیے۔ ان کی شاعری کی خصوصیات بیان کریں۔",
            "علامہ اقبال کے فلسفہ خودی کو اپنے الفاظ میں بیان کریں اور اس کی عملی زندگی میں اہمیت واضح کریں۔",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # PAKISTAN > PUNJAB BOARDS > CLASS 10
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 10", "subject": "Physics", "paper_id": "pk_punjab_c10_phy_01",
        "mcqs": [
            "The SI unit of electric charge is: A) Coulomb  B) Ampere  C) Volt  D) Ohm",
            "According to Ohm's Law, V = ? A) IR  B) I/R  C) R/I  D) I²R",
            "A device that converts electrical energy into mechanical energy is: A) Motor  B) Generator  C) Transformer  D) Capacitor",
            "The critical angle is the angle of incidence for which the angle of refraction is: A) 90°  B) 45°  C) 0°  D) 180°",
            "Which type of radiation has the highest penetrating power? A) Gamma rays  B) Alpha particles  C) Beta particles  D) X-rays",
            "The half-life of a radioactive element is the time taken for half of the atoms to: A) Decay  B) Double  C) Triple  D) Remain unchanged",
            "The formula for electrical power is: A) P = VI  B) P = V/I  C) P = I/V  D) P = V²I",
            "Alternating current (AC) changes its direction: A) Periodically  B) Never  C) Once  D) Randomly",
        ],
        "short_questions": [
            "Define Ohm's Law. Under what conditions does a conductor obey Ohm's Law?",
            "What is meant by total internal reflection? State the conditions required for it.",
            "What is radioactivity? Name three types of radiation and their properties.",
            "Define electric current and potential difference. Write their SI units.",
            "What is a transformer? How does it work? Distinguish between step-up and step-down transformers.",
            "State Faraday's Laws of Electromagnetic Induction.",
        ],
        "long_questions": [
            "Describe the construction and working of a DC electric motor. Draw a labeled diagram. Explain how it converts electrical energy into mechanical energy.",
            "What is nuclear fission and nuclear fusion? Compare them in terms of energy release, conditions required, and their uses.",
            "Explain the working of a simple AC generator. Draw its diagram and describe how EMF is generated.",
        ],
    },
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 10", "subject": "Physics", "paper_id": "pk_punjab_c10_phy_02",
        "mcqs": [
            "The lens formula is: A) 1/f = 1/v - 1/u  B) 1/f = 1/v + 1/u  C) f = v - u  D) f = v + u",
            "Which color of light has the highest frequency? A) Violet  B) Red  C) Green  D) Yellow",
            "The process by which a substance changes from liquid to gas at boiling point is called: A) Vaporization  B) Condensation  C) Sublimation  D) Fusion",
            "In a series circuit, the current through each component is: A) Same  B) Different  C) Zero  D) Maximum",
            "The energy stored in a capacitor is: A) ½CV²  B) CV²  C) ½CV  D) C/V",
        ],
        "short_questions": [
            "Define the terms: focal length, principal axis, and centre of curvature for a lens.",
            "Explain the photoelectric effect. What did Einstein propose to explain it?",
            "What is meant by specific heat capacity? Write its formula and SI unit.",
            "Define parallel and series circuits. State one advantage of each.",
        ],
        "long_questions": [
            "Explain the human eye. Describe the defects of vision (myopia, hyperopia) and how they are corrected using lenses.",
            "Describe the nuclear reactor. Explain the roles of moderator, control rods, and coolant. What are the advantages and disadvantages of nuclear energy?",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 10", "subject": "Chemistry", "paper_id": "pk_punjab_c10_chem_01",
        "mcqs": [
            "The process of removing oxygen from a compound is called: A) Reduction  B) Oxidation  C) Displacement  D) Decomposition",
            "Which acid is present in gastric juice? A) Hydrochloric acid  B) Sulphuric acid  C) Nitric acid  D) Acetic acid",
            "The chemical formula of washing soda is: A) Na₂CO₃·10H₂O  B) NaOH  C) NaHCO₃  D) Na₂SO₄",
            "Rusting of iron is an example of: A) Oxidation  B) Reduction  C) Sublimation  D) Neutralization",
            "The pH of a strong acid is: A) Less than 7  B) Equal to 7  C) Greater than 7  D) Exactly 0",
            "Which gas is produced when zinc reacts with dilute H₂SO₄? A) H₂  B) O₂  C) CO₂  D) SO₂",
            "An organic compound containing only carbon and hydrogen is called: A) Hydrocarbon  B) Carbohydrate  C) Alcohol  D) Amine",
        ],
        "short_questions": [
            "Define oxidation and reduction. Give one example of each.",
            "What are alkanes? Write the general formula of alkanes and give two examples.",
            "Explain the industrial preparation of sulphuric acid (Contact Process).",
            "What is saponification? How is soap made from fats and NaOH?",
            "Define electrolysis. Give an example and write the reactions at each electrode.",
        ],
        "long_questions": [
            "Describe the Haber Process for the industrial manufacture of ammonia. Write the chemical equation, state the conditions, and explain why these conditions are used.",
            "What are acids and bases? Explain the pH scale. Describe the neutralization reaction and its industrial importance.",
            "Explain coal, petroleum, and natural gas as fossil fuels. Describe the fractional distillation of petroleum and its products.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 10", "subject": "Biology", "paper_id": "pk_punjab_c10_bio_01",
        "mcqs": [
            "The functional unit of the kidney is called: A) Nephron  B) Neuron  C) Alveolus  D) Villus",
            "Insulin is produced by: A) Pancreas  B) Liver  C) Thyroid gland  D) Adrenal gland",
            "Which part of the brain controls balance and coordination? A) Cerebellum  B) Cerebrum  C) Medulla  D) Hypothalamus",
            "The genetic material present in chromosomes is: A) DNA  B) RNA  C) Protein  D) Lipid",
            "Mendel's Law of Segregation states that: A) Alleles separate during gamete formation  B) Genes are linked  C) Traits are blended  D) Chromosomes cross over",
            "The process of removing metabolic wastes from the body is called: A) Excretion  B) Secretion  C) Respiration  D) Digestion",
            "Blood flows from the heart to the lungs via the: A) Pulmonary artery  B) Pulmonary vein  C) Aorta  D) Vena cava",
        ],
        "short_questions": [
            "What is homeostasis? Why is it important for the survival of organisms?",
            "Describe the structure and function of the nephron.",
            "Explain Mendel's Law of Dominance with an example.",
            "What is meant by the endocrine system? Name four endocrine glands and their hormones.",
            "Explain the mechanism of the reflex arc.",
        ],
        "long_questions": [
            "Describe the human excretory system. Explain how the kidney filters blood and produces urine. Mention the role of the ureter, bladder, and urethra.",
            "Explain the nervous system. Describe the structure of a neuron and the mechanism of nerve impulse conduction.",
            "What is genetics? Explain Mendel's laws of inheritance with examples. Describe a monohybrid cross using a Punnett square.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 10", "subject": "Mathematics", "paper_id": "pk_punjab_c10_math_01",
        "mcqs": [
            "The standard form of a quadratic equation is: A) ax² + bx + c = 0  B) ax + b = 0  C) ax² + b = 0  D) ax³ + bx² = 0",
            "The discriminant of ax² + bx + c = 0 is: A) b² - 4ac  B) b² + 4ac  C) 4ac - b²  D) √(b² - 4ac)",
            "sin²θ + cos²θ = : A) 1  B) 0  C) 2  D) -1",
            "The value of cos 0° is: A) 1  B) 0  C) -1  D) 1/2",
            "If the sum of a geometric series is infinite, then the common ratio r must satisfy: A) |r| < 1  B) |r| > 1  C) r = 1  D) r = 0",
            "The number of diagonals in a hexagon is: A) 9  B) 6  C) 12  D) 15",
            "The area of a triangle with base b and height h is: A) ½bh  B) bh  C) 2bh  D) ¼bh",
        ],
        "short_questions": [
            "Solve the quadratic equation 2x² - 5x + 3 = 0 using the quadratic formula.",
            "Prove the identity: (sin θ + cos θ)² + (sin θ - cos θ)² = 2.",
            "Find the sum of the first 10 terms of the arithmetic series: 2, 5, 8, 11...",
            "Define similar triangles. State the conditions for two triangles to be similar.",
            "Find the area and circumference of a circle with radius 7 cm.",
        ],
        "long_questions": [
            "Prove that if two chords of a circle are equal, they are equidistant from the centre. Also prove the converse.",
            "Solve the system of equations: 3x + 2y = 12 and 2x - y = 1. Verify your solution.",
            "Derive the formula for the volume and total surface area of a cylinder. Calculate both for a cylinder with radius 5 cm and height 10 cm.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 10", "subject": "Computer Science", "paper_id": "pk_punjab_c10_cs_01",
        "mcqs": [
            "HTML stands for: A) HyperText Markup Language  B) High Text Markup Language  C) HyperText Making Language  D) High Transfer Markup Language",
            "Which data structure uses LIFO (Last In First Out)? A) Stack  B) Queue  C) Array  D) Tree",
            "Which of the following is a high-level language? A) Python  B) Assembly  C) Machine language  D) Binary",
            "The Internet is an example of: A) WAN  B) LAN  C) MAN  D) PAN",
            "A function that calls itself is called: A) Recursive function  B) Iterative function  C) Inline function  D) Virtual function",
        ],
        "short_questions": [
            "What is a database? Define primary key and foreign key.",
            "Write a Python program to find the factorial of a given number.",
            "Explain the difference between a compiler and an interpreter.",
            "What is networking? Describe the types of networks (LAN, MAN, WAN).",
            "Define a loop. Write a program using a while loop to print the first 10 natural numbers.",
        ],
        "long_questions": [
            "Explain object-oriented programming (OOP). Describe the concepts of class, object, inheritance, and polymorphism with examples.",
            "What is a database management system (DBMS)? Compare relational and non-relational databases. Describe SQL operations: SELECT, INSERT, UPDATE, DELETE.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # PAKISTAN > PUNJAB BOARDS > CLASS 11 (FSc)
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 11", "subject": "Physics", "paper_id": "pk_punjab_c11_phy_01",
        "mcqs": [
            "The dimension of angular momentum is: A) [ML²T⁻¹]  B) [MLT⁻¹]  C) [ML²T⁻²]  D) [MLT⁻²]",
            "At the highest point of projectile motion, the vertical component of velocity is: A) Zero  B) Maximum  C) Equal to initial velocity  D) Negative",
            "The work-energy theorem states that the net work done on an object equals its: A) Change in kinetic energy  B) Change in potential energy  C) Total energy  D) Change in momentum",
            "Which force acts on a satellite in circular orbit? A) Gravitational force  B) Normal force  C) Frictional force  D) Electromagnetic force",
            "The relationship between linear and angular velocity is: A) v = rω  B) v = r/ω  C) v = ω/r  D) v = rω²",
            "Young's modulus is defined as: A) Stress/Strain  B) Strain/Stress  C) Force/Area  D) Extension/Length",
        ],
        "short_questions": [
            "State and derive the equation of motion v = u + at using calculus.",
            "Define projectile motion. Derive the equation for the range of a projectile.",
            "What is the law of gravitation? Define gravitational field strength.",
            "Explain Hooke's Law. Define elastic limit and yield point.",
            "What is the Doppler effect? Write the formula for apparent frequency.",
        ],
        "long_questions": [
            "Derive the equations of uniformly accelerated motion from first principles. Apply them to solve: A ball is thrown vertically upward with velocity 20 m/s. Find the maximum height and time of flight.",
            "State and prove the conservation of momentum. Explain its application to elastic and inelastic collisions.",
            "What is Simple Harmonic Motion? Derive the equation of displacement as a function of time. Find the velocity and acceleration expressions.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 11", "subject": "Chemistry", "paper_id": "pk_punjab_c11_chem_01",
        "mcqs": [
            "According to VSEPR theory, the shape of CH₄ is: A) Tetrahedral  B) Linear  C) Trigonal planar  D) Octahedral",
            "The quantum number that determines the shape of an orbital is: A) Azimuthal  B) Principal  C) Magnetic  D) Spin",
            "Raoult's Law applies to: A) Ideal solutions  B) Real solutions  C) Electrolytes  D) Colloids",
            "Which of the following has the highest lattice energy? A) NaCl  B) CsCl  C) LiF  D) KBr",
            "The first ionization energy generally increases across a period because: A) Atomic number increases  B) Atomic radius decreases  C) Electron affinity decreases  D) Metallic character increases",
        ],
        "short_questions": [
            "Explain the concept of hybridization. Describe sp, sp², and sp³ hybridization with examples.",
            "State and explain Raoult's Law. Define ideal solution.",
            "What is electronegativity? How does it vary across a period and down a group?",
            "Define quantum numbers. Explain the significance of each quantum number.",
            "What is lattice energy? How is it calculated using Born-Haber cycle?",
        ],
        "long_questions": [
            "Explain the electronic configuration of elements. Describe Aufbau principle, Pauli exclusion principle, and Hund's rule. Write the configuration of Fe (Z=26).",
            "Describe intermolecular forces: London dispersion, dipole-dipole, and hydrogen bonding. How do they affect boiling point and solubility?",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 11", "subject": "Biology", "paper_id": "pk_punjab_c11_bio_01",
        "mcqs": [
            "The organelle responsible for protein synthesis is: A) Ribosome  B) Golgi apparatus  C) Lysosome  D) Peroxisome",
            "Which stage of meiosis involves crossing over? A) Prophase I  B) Metaphase I  C) Anaphase I  D) Telophase I",
            "The transport of molecules against a concentration gradient requires: A) Active transport  B) Passive diffusion  C) Osmosis  D) Facilitated diffusion",
            "Enzymes are biological: A) Catalysts  B) Substrates  C) Products  D) Reactants",
            "The term 'half-life' is used in: A) Radioisotope biology  B) Enzyme kinetics  C) Both  D) Neither",
        ],
        "short_questions": [
            "Distinguish between mitosis and meiosis. State the biological significance of each.",
            "Explain the fluid mosaic model of the cell membrane.",
            "What is enzyme specificity? Explain the lock-and-key and induced-fit models.",
            "Define turgidity and plasmolysis. Under what conditions do they occur?",
        ],
        "long_questions": [
            "Describe the process of mitosis in detail. Explain each phase: prophase, metaphase, anaphase, and telophase.",
            "Explain photosynthesis in detail: light reactions (Z-scheme) and the Calvin cycle. How are ATP and NADPH used?",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 11", "subject": "Mathematics", "paper_id": "pk_punjab_c11_math_01",
        "mcqs": [
            "The value of limₓ→0 (sin x / x) is: A) 1  B) 0  C) ∞  D) -1",
            "The derivative of eˣ is: A) eˣ  B) xe^(x-1)  C) e^(x-1)  D) 1/eˣ",
            "If f(x) = x², then f'(x) = : A) 2x  B) x²  C) 2  D) x",
            "The integral of cos x is: A) sin x + C  B) -sin x + C  C) -cos x + C  D) tan x + C",
            "A matrix with equal number of rows and columns is called: A) Square matrix  B) Row matrix  C) Column matrix  D) Identity matrix",
            "The value of 3! is: A) 6  B) 3  C) 9  D) 12",
        ],
        "short_questions": [
            "Find the derivative of f(x) = x³ - 3x² + 2x - 5 using differentiation rules.",
            "Evaluate the integral ∫(2x + 3)dx.",
            "Solve the system of equations using matrices: x + y = 5, 2x - y = 1.",
            "Define function limits. Evaluate limₓ→2 (x² - 4)/(x - 2).",
        ],
        "long_questions": [
            "State and prove the Binomial Theorem for positive integer exponent n. Expand (1 + x)⁵ using the theorem.",
            "Explain permutations and combinations. Derive the formulas ⁿPᵣ and ⁿCᵣ. In how many ways can 4 books be selected from 10?",
        ],
    },

    # ── Class 11 > English ────────────────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 11", "subject": "English", "paper_id": "pk_punjab_c11_eng_01",
        "mcqs": [
            "A sentence that expresses a question is called: A) Interrogative  B) Declarative  C) Imperative  D) Exclamatory",
            "The word 'benevolent' means: A) Kind and generous  B) Cruel and harsh  C) Shy and quiet  D) Strong and fearless",
            "Which literary device involves giving human qualities to non-human things? A) Personification  B) Metaphor  C) Simile  D) Alliteration",
        ],
        "short_questions": [
            "Write a summary of the poem 'The Road Not Taken' by Robert Frost.",
            "Explain the themes of courage and perseverance in literature with examples.",
            "Write a paragraph on 'The Role of Youth in Nation Building'.",
            "Correct the following sentences: (a) She don't know the answer. (b) He is more taller than me.",
        ],
        "long_questions": [
            "Write an argumentative essay of 300 words on: 'Social media has a negative impact on youth'. Present both sides and give your opinion.",
            "Write a letter to the editor of a newspaper complaining about the lack of public parks in your city. Suggest solutions.",
        ],
    },

    # ── Class 11 > Pakistan Studies ───────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 11", "subject": "Pakistan Studies", "paper_id": "pk_punjab_c11_pst_01",
        "mcqs": [
            "The Constitution of Pakistan was first enacted in: A) 1956  B) 1962  C) 1973  D) 1947",
            "The national language of Pakistan is: A) Urdu  B) Punjabi  C) Sindhi  D) English",
            "Pakistan's economy is primarily based on: A) Agriculture  B) Industry  C) Services  D) Mining",
            "The Indus Waters Treaty was signed in: A) 1960  B) 1947  C) 1965  D) 1970",
        ],
        "short_questions": [
            "What are the major agricultural crops of Pakistan? Describe any two in detail.",
            "Describe the federal structure of Pakistan's government.",
            "What is CPEC? What are its benefits for Pakistan?",
            "Write a note on the Water Accord 1991 and its significance.",
        ],
        "long_questions": [
            "Describe the economic challenges facing Pakistan today. Suggest measures for sustainable economic development.",
            "Explain the agricultural system of Pakistan. Describe land reforms and their impact on rural economy.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # PAKISTAN > PUNJAB BOARDS > CLASS 12 (FSc)
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 12", "subject": "Physics", "paper_id": "pk_punjab_c12_phy_01",
        "mcqs": [
            "The speed of light in vacuum is approximately: A) 3×10⁸ m/s  B) 3×10⁶ m/s  C) 3×10¹⁰ m/s  D) 3×10⁵ m/s",
            "In a p-n junction diode, the depletion region is formed due to: A) Diffusion of charge carriers  B) External battery  C) Reverse bias  D) Forward bias",
            "The phenomenon of emission of electrons from a metal surface when light falls on it is called: A) Photoelectric effect  B) Compton effect  C) Raman effect  D) Hall effect",
            "Which particles are found in the nucleus of an atom? A) Protons and neutrons  B) Protons and electrons  C) Neutrons and electrons  D) Only protons",
            "De Broglie wavelength is given by: A) λ = h/mv  B) λ = mv/h  C) λ = hv/m  D) λ = m/hv",
        ],
        "short_questions": [
            "Explain the working of a semiconductor diode in forward and reverse bias.",
            "State the postulates of Bohr's model of the hydrogen atom.",
            "What is meant by wave-particle duality? Explain de Broglie's hypothesis.",
            "Define the work function of a metal. How does photoelectric emission depend on frequency?",
        ],
        "long_questions": [
            "Explain Einstein's photoelectric equation. How does it support the quantum nature of light? Describe Millikan's experiment to verify this equation.",
            "Describe the structure of the atom. Explain Rutherford's atomic model and its limitations. How did Bohr's model improve upon Rutherford's model?",
            "Explain the principle and working of a transistor. Describe its use as a switch and as an amplifier.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 12", "subject": "Chemistry", "paper_id": "pk_punjab_c12_chem_01",
        "mcqs": [
            "Which of the following is an aldehyde? A) HCHO  B) CH₃OH  C) CH₃COCH₃  D) C₆H₅OH",
            "The reaction of an acid with an alcohol to form ester is called: A) Esterification  B) Saponification  C) Hydrolysis  D) Fermentation",
            "The monomer of nylon-6,6 is: A) Hexamethylenediamine and adipic acid  B) Ethylene  C) Vinyl chloride  D) Propylene",
            "Benzene is represented by: A) C₆H₆  B) C₆H₁₂  C) C₃H₆  D) C₄H₁₀",
            "An amino group is: A) -NH₂  B) -COOH  C) -OH  D) -CHO",
        ],
        "short_questions": [
            "Define aldehydes and ketones. How are they distinguished using Tollens' reagent?",
            "Explain the mechanism of nucleophilic addition to carbonyl compounds.",
            "What are carboxylic acids? Describe their preparation and reactions.",
            "Define polymers. Distinguish between addition and condensation polymerization.",
        ],
        "long_questions": [
            "Describe the structure of benzene. Explain electrophilic aromatic substitution reactions: nitration, halogenation, and sulfonation.",
            "What are amino acids? Describe the formation of a peptide bond. Explain the primary, secondary, tertiary, and quaternary structures of proteins.",
            "What is carbohydrate chemistry? Classify carbohydrates and explain the structure of glucose. Describe the biochemical role of carbohydrates.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 12", "subject": "Biology", "paper_id": "pk_punjab_c12_bio_01",
        "mcqs": [
            "Which process produces ATP in the mitochondria? A) Oxidative phosphorylation  B) Glycolysis  C) Fermentation  D) Photophosphorylation",
            "The site of protein synthesis in a cell is: A) Ribosome  B) Nucleus  C) Mitochondria  D) Golgi body",
            "Which base is found in RNA but not in DNA? A) Uracil  B) Thymine  C) Cytosine  D) Adenine",
            "The enzyme that unwinds DNA during replication is: A) Helicase  B) Ligase  C) Polymerase  D) Primase",
            "Natural selection was proposed by: A) Charles Darwin  B) Gregor Mendel  C) Louis Pasteur  D) Watson and Crick",
        ],
        "short_questions": [
            "Explain the process of DNA replication. Name the enzymes involved.",
            "What is translation? Describe the role of mRNA, tRNA, and ribosomes.",
            "Define evolution. Explain Darwin's theory of natural selection.",
            "What is an ecosystem? Describe the energy flow through a food chain.",
        ],
        "long_questions": [
            "Describe the process of transcription and translation. Explain how genetic information flows from DNA to protein (Central Dogma).",
            "Explain Darwin's theory of evolution by natural selection. Describe the evidence for evolution: fossil record, comparative anatomy, and molecular biology.",
            "Describe the carbon cycle and nitrogen cycle. Explain the role of microorganisms in these cycles.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 12", "subject": "Mathematics", "paper_id": "pk_punjab_c12_math_01",
        "mcqs": [
            "The integral of 1/x is: A) ln|x| + C  B) x² + C  C) eˣ + C  D) 1/x² + C",
            "The area under the curve y = f(x) from a to b is given by: A) ∫ₐᵇ f(x)dx  B) f(b) - f(a)  C) f'(x)  D) ∑f(x)",
            "A vector with magnitude 1 is called: A) Unit vector  B) Null vector  C) Position vector  D) Free vector",
            "The dot product of perpendicular vectors is: A) 0  B) 1  C) -1  D) |A||B|",
            "The general solution of dy/dx = y is: A) y = Ceˣ  B) y = Cx  C) y = Cx²  D) y = C/x",
        ],
        "short_questions": [
            "Evaluate the definite integral: ∫₀¹ x² dx.",
            "Find the area enclosed between the curve y = x² and the line y = x.",
            "Add the vectors A = 3i + 4j and B = 2i - j. Find the magnitude of the resultant.",
            "Solve the differential equation: dy/dx + y = eˣ.",
        ],
        "long_questions": [
            "Explain the Fundamental Theorem of Calculus. Evaluate ∫₀² (3x² - 2x + 1) dx and verify using the anti-derivative method.",
            "Describe conic sections: circle, ellipse, parabola, and hyperbola. Derive the standard equation of an ellipse.",
        ],
    },

    # ── Class 12 > Computer Science ───────────────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 12", "subject": "Computer Science", "paper_id": "pk_punjab_c12_cs_01",
        "mcqs": [
            "Big O notation O(n log n) describes the complexity of: A) Merge sort  B) Bubble sort  C) Linear search  D) Binary search",
            "Which protocol is used to send emails? A) SMTP  B) HTTP  C) FTP  D) TCP",
            "A deadlock occurs when: A) Processes wait indefinitely for resources  B) CPU runs too fast  C) Memory overflows  D) Disk is full",
            "Artificial Intelligence is a branch of: A) Computer Science  B) Mathematics  C) Biology  D) Physics",
            "Which sorting algorithm has O(n²) worst-case complexity? A) Bubble sort  B) Merge sort  C) Quick sort  D) Heap sort",
        ],
        "short_questions": [
            "Explain the concept of recursion with an example. Write a recursive function for Fibonacci series.",
            "What is a binary search tree (BST)? Explain insertion and deletion operations.",
            "Describe the client-server architecture. How does HTTP work?",
            "Define artificial intelligence. Describe machine learning and its types.",
        ],
        "long_questions": [
            "Explain the OSI model. Describe the function of each of the 7 layers.",
            "What are data structures? Compare arrays, linked lists, stacks, and queues with their operations and time complexity.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # PAKISTAN > CAMBRIDGE > O LEVEL
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "O Level", "subject": "Physics", "paper_id": "pk_cam_olevel_phy_01",
        "mcqs": [
            "A body is in equilibrium when: A) The resultant force on it is zero  B) It is moving with uniform acceleration  C) No forces act on it  D) It is at rest only",
            "The pressure at a depth h in a liquid of density ρ is: A) ρgh  B) ρg/h  C) gh/ρ  D) ρh/g",
            "Which type of thermometer uses the expansion of a liquid to measure temperature? A) Mercury thermometer  B) Thermocouple  C) Resistance thermometer  D) Infrared thermometer",
            "The unit of resistance is: A) Ohm  B) Siemens  C) Farad  D) Henry",
            "In a series circuit of three resistors, the total resistance is: A) R₁ + R₂ + R₃  B) 1/(1/R₁ + 1/R₂ + 1/R₃)  C) R₁ × R₂ × R₃  D) R₁/R₂/R₃",
        ],
        "short_questions": [
            "State the principle of moments. Apply it to explain how a see-saw balances.",
            "Explain the difference between heat and temperature. Define specific heat capacity.",
            "Describe the electromagnetic spectrum. State two properties common to all electromagnetic waves.",
            "Define Boyle's Law. State the conditions under which it applies.",
        ],
        "long_questions": [
            "Explain the concept of energy. Describe the principle of conservation of energy with an example involving a swinging pendulum. Calculate the KE and PE at various points.",
            "Describe the properties and uses of different parts of the electromagnetic spectrum. Explain how radio waves are transmitted and received.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "O Level", "subject": "Chemistry", "paper_id": "pk_cam_olevel_chem_01",
        "mcqs": [
            "Which type of bonding occurs between a metal and a non-metal? A) Ionic  B) Covalent  C) Metallic  D) Dative",
            "The process of splitting a large molecule into smaller ones using water is called: A) Hydrolysis  B) Condensation  C) Polymerization  D) Neutralization",
            "The relative molecular mass of H₂SO₄ is: A) 98  B) 48  C) 64  D) 80",
            "Which gas is produced at the anode during electrolysis of dilute sulfuric acid? A) Oxygen  B) Hydrogen  C) Chlorine  D) Sulfur dioxide",
        ],
        "short_questions": [
            "Explain the process of fractional distillation of air. What gases are obtained?",
            "Describe the laboratory preparation of hydrogen chloride gas. How is it tested?",
            "Define oxidation and reduction in terms of electron transfer. Give an example of a redox reaction.",
            "What is a catalyst? Explain its effect on a chemical reaction with an example.",
        ],
        "long_questions": [
            "Describe the extraction of iron using a blast furnace. Write the relevant chemical equations and explain the role of each ingredient.",
            "Explain the industrial manufacture of ammonia (Haber Process) and sulphuric acid (Contact Process). Compare the conditions used and explain why they are chosen.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "O Level", "subject": "Biology", "paper_id": "pk_cam_olevel_bio_01",
        "mcqs": [
            "Transpiration mainly occurs through: A) Stomata  B) Lenticels  C) Epidermis  D) Bark",
            "The enzyme amylase breaks down: A) Starch  B) Protein  C) Fat  D) DNA",
            "Haemoglobin is found in: A) Red blood cells  B) White blood cells  C) Platelets  D) Plasma",
            "Which gas is exchanged during respiration in leaves? A) CO₂ and O₂  B) N₂ and O₂  C) H₂ and CO₂  D) O₂ and N₂",
        ],
        "short_questions": [
            "Describe the role of the liver in metabolism.",
            "Explain how the kidney regulates blood composition (osmoregulation).",
            "What is the function of the guard cells? How do they open and close stomata?",
            "Describe sexual reproduction in flowering plants.",
        ],
        "long_questions": [
            "Describe the human digestive system. Explain the roles of enzymes at each stage of digestion.",
            "Explain the process of blood circulation in humans. Describe the pulmonary and systemic circuits with a diagram.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "O Level", "subject": "Mathematics", "paper_id": "pk_cam_olevel_math_01",
        "mcqs": [
            "The gradient of the line y = 3x - 5 is: A) 3  B) -5  C) -3  D) 5",
            "The probability of getting heads when a fair coin is tossed is: A) 1/2  B) 1  C) 0  D) 1/4",
            "If x² = 25, then x = : A) ±5  B) 5  C) -5  D) 25",
            "The volume of a sphere with radius r is: A) (4/3)πr³  B) 4πr²  C) πr²h  D) (2/3)πr³",
        ],
        "short_questions": [
            "Solve for x: 3x + 7 = 22.",
            "A bag contains 4 red and 6 blue balls. What is the probability of drawing a red ball?",
            "Find the equation of the line with gradient 2 passing through (1, 3).",
            "Calculate the surface area of a cylinder with radius 4 cm and height 9 cm.",
        ],
        "long_questions": [
            "Solve the simultaneous equations: 3x + 2y = 16 and x - y = 2. Show all working.",
            "A car travels 180 km in 2 hours. A bus travels the same distance in 2.5 hours. Find the speed of each. If they start from the same point in opposite directions, how far apart are they after 1 hour?",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "O Level", "subject": "Computer Science", "paper_id": "pk_cam_olevel_cs_01",
        "mcqs": [
            "A flowchart symbol for a decision is: A) Diamond  B) Rectangle  C) Oval  D) Parallelogram",
            "The binary equivalent of decimal 10 is: A) 1010  B) 1100  C) 1001  D) 1110",
            "Which of the following is secondary storage? A) Hard disk  B) RAM  C) CPU registers  D) Cache",
            "Pseudocode is: A) An informal high-level description of algorithm  B) A programming language  C) Machine code  D) Binary code",
        ],
        "short_questions": [
            "Describe three input and three output devices with their uses.",
            "Explain the fetch-decode-execute cycle in a CPU.",
            "Convert 11001010 (binary) to decimal and hexadecimal.",
            "Define validation and verification in data entry. Give examples.",
        ],
        "long_questions": [
            "Explain the difference between high-level and low-level programming languages. Describe the role of a compiler and an interpreter.",
            "Describe database management systems. Explain how data is stored, retrieved, and manipulated using SQL.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "O Level", "subject": "English Language", "paper_id": "pk_cam_olevel_eng_01",
        "mcqs": [
            "The sentence 'The cat sat on the mat' is an example of: A) Simple sentence  B) Compound sentence  C) Complex sentence  D) Compound-complex sentence",
            "Which of the following is a conjunction? A) Although  B) Quickly  C) Beautiful  D) The",
        ],
        "short_questions": [
            "Write a directed writing task: You are writing a report for the school principal about the need for a new library. Include: current situation, benefits, and recommendations.",
            "Read the following article about climate change and identify: (a) the main argument, (b) two pieces of evidence, (c) the tone of the writer.",
            "Summarize the following passage in 80–100 words: [A passage about digital literacy in the modern world].",
        ],
        "long_questions": [
            "Write a discursive essay (350–400 words) on: 'Online learning is more beneficial than traditional classroom learning.' Discuss advantages and disadvantages and state your view.",
            "Write an article for a school magazine titled 'The Importance of Mental Health Awareness Among Teenagers'. Include statistics, causes, effects, and recommendations.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # PAKISTAN > CAMBRIDGE > A LEVEL
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "A Level", "subject": "Physics", "paper_id": "pk_cam_alevel_phy_01",
        "mcqs": [
            "Which principle explains the formation of standing waves? A) Superposition principle  B) Huygens' principle  C) Bernoulli's principle  D) Archimedes' principle",
            "The Heisenberg uncertainty principle states that: A) Δx·Δp ≥ ℏ/2  B) Δx·Δp = 0  C) Δx = Δp  D) Δx·Δp ≤ ℏ/2",
            "A p-type semiconductor is produced by doping silicon with: A) Boron  B) Phosphorus  C) Arsenic  D) Antimony",
            "The work function of a metal is 4.0 eV. What is the threshold frequency? A) 9.7×10¹⁴ Hz  B) 4.0×10¹⁴ Hz  C) 6.6×10¹⁴ Hz  D) 1.2×10¹⁵ Hz",
        ],
        "short_questions": [
            "Derive an expression for the electric potential at a point due to a point charge.",
            "Explain the concept of gravitational potential energy. Derive the escape velocity from Earth's surface.",
            "Describe the Hall effect. How is it used to determine the type of charge carriers in a semiconductor?",
            "Explain the quantum mechanical model of the hydrogen atom. What are the allowed energy levels?",
        ],
        "long_questions": [
            "Derive Maxwell's equations (in integral form). Explain how they predict the existence of electromagnetic waves. Calculate the speed of light from Maxwell's equations.",
            "Describe the photoelectric effect and Compton scattering. How do they together establish the particle nature of light? Discuss the wave-particle duality.",
            "Explain the band theory of solids. Distinguish between conductors, semiconductors, and insulators using energy band diagrams.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "A Level", "subject": "Chemistry", "paper_id": "pk_cam_alevel_chem_01",
        "mcqs": [
            "The mechanism of addition of HBr to propene follows: A) Markovnikov's rule  B) Anti-Markovnikov's rule  C) E2 mechanism  D) SN2 mechanism",
            "Which compound undergoes nucleophilic substitution more readily? A) Alkyl halides  B) Alkanes  C) Alkenes  D) Arenes",
            "The rate-determining step in a reaction is: A) The slowest step  B) The fastest step  C) The first step  D) The last step",
            "Buffer solutions resist changes in: A) pH  B) Temperature  C) Pressure  D) Volume",
        ],
        "short_questions": [
            "Explain the nucleophilic substitution reactions SN1 and SN2. Compare their mechanisms and stereochemistry.",
            "Derive the Henderson-Hasselbalch equation for buffer solutions. Calculate the pH of a buffer containing 0.1 M acetic acid and 0.1 M sodium acetate (Ka = 1.8×10⁻⁵).",
            "Explain the concept of reaction kinetics. How is the rate constant k related to temperature (Arrhenius equation)?",
            "Describe the structure and reactions of benzene. Explain why benzene undergoes substitution rather than addition.",
        ],
        "long_questions": [
            "Explain the thermodynamics of chemical reactions. Define enthalpy, entropy, and Gibbs free energy. Under what conditions is a reaction spontaneous?",
            "Describe the mechanisms of electrophilic aromatic substitution: Friedel-Crafts alkylation and acylation, nitration, and sulfonation.",
            "Explain electrochemistry: electrode potential, electrochemical cells, and electrolysis. Describe the applications of electrolysis in industry.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "A Level", "subject": "Biology", "paper_id": "pk_cam_alevel_bio_01",
        "mcqs": [
            "Which enzyme is responsible for DNA repair? A) DNA ligase  B) DNA polymerase I  C) Helicase  D) Topoisomerase",
            "Apoptosis is: A) Programmed cell death  B) Cell division  C) Cell growth  D) DNA replication",
            "The Hardy-Weinberg equilibrium assumes: A) No mutation, migration, selection  B) Small population  C) Natural selection  D) Genetic drift",
            "Which molecule acts as the energy currency of the cell? A) ATP  B) ADP  C) NADH  D) FADH₂",
        ],
        "short_questions": [
            "Explain the mechanism of enzyme inhibition: competitive, non-competitive, and allosteric inhibition.",
            "Describe the role of ATP in cellular processes. How is ATP regenerated during aerobic respiration?",
            "Explain gene expression regulation in eukaryotes. Describe the role of transcription factors.",
            "What is the Hardy-Weinberg principle? Describe the conditions that maintain genetic equilibrium.",
        ],
        "long_questions": [
            "Describe the detailed mechanism of oxidative phosphorylation and the electron transport chain. How is ATP synthesized by ATP synthase (chemiosmosis)?",
            "Explain the immune system in detail: innate and adaptive immunity, B and T lymphocytes, antibodies, and vaccines.",
            "Describe the process of genetic engineering. Explain the use of restriction enzymes, vectors, and PCR in recombinant DNA technology.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "A Level", "subject": "Mathematics", "paper_id": "pk_cam_alevel_math_01",
        "mcqs": [
            "The derivative of ln(x) is: A) 1/x  B) x  C) 1/x²  D) -1/x",
            "Maclaurin series for eˣ is: A) 1 + x + x²/2! + x³/3! + ...  B) x + x²/2 + x³/3 + ...  C) 1 - x + x²/2! - ...  D) x - x³/3! + ...",
            "The modulus of the complex number 3 + 4i is: A) 5  B) 7  C) 3  D) 4",
            "∫eˣ cos x dx equals: A) eˣ(sin x + cos x)/2 + C  B) eˣ sin x + C  C) eˣ cos x + C  D) eˣ/cos x + C",
        ],
        "short_questions": [
            "Use integration by parts to evaluate: ∫x eˣ dx.",
            "Express the complex number (3 + 4i)/(1 - 2i) in the form a + bi.",
            "Find the general solution of the differential equation: d²y/dx² - 3dy/dx + 2y = 0.",
            "Use the Maclaurin series to expand sin x up to the x⁵ term. Use it to estimate sin(0.1 rad).",
        ],
        "long_questions": [
            "Derive the Taylor and Maclaurin series. Expand f(x) = (1+x)^n using the binomial series. State the range of validity.",
            "Explain vectors in 3D space. Define dot product and cross product. Find the angle between a = 2i + j - k and b = i - 2j + 3k.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "A Level", "subject": "Computer Science", "paper_id": "pk_cam_alevel_cs_01",
        "mcqs": [
            "Which sorting algorithm has O(n log n) average and worst-case complexity? A) Merge sort  B) Bubble sort  C) Insertion sort  D) Selection sort",
            "Which data structure is used for BFS traversal of a graph? A) Queue  B) Stack  C) Array  D) Tree",
            "Turing completeness means: A) A system can perform any computation  B) A program has no bugs  C) A system is fast  D) A language is compiled",
            "Public key cryptography uses: A) Two different keys  B) One shared key  C) No key  D) A hash function only",
        ],
        "short_questions": [
            "Explain the P vs NP problem. Give one example of an NP-complete problem.",
            "Describe the RSA encryption algorithm. Explain how public and private keys are generated.",
            "Write pseudocode for a binary search algorithm and state its time complexity.",
            "Explain garbage collection in programming languages. Compare reference counting and mark-and-sweep.",
        ],
        "long_questions": [
            "Describe the architecture of a relational database. Explain normalisation (1NF, 2NF, 3NF) with examples. Write SQL queries for complex operations (JOIN, GROUP BY, HAVING).",
            "Explain concurrency in operating systems. Describe deadlock conditions, prevention, and avoidance using Banker's algorithm.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # PAKISTAN > FEDERAL BOARD > CLASS 9 & 10
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 9", "subject": "Physics", "paper_id": "pk_fbise_c9_phy_01",
        "mcqs": [
            "Which instrument is used to measure very small lengths? A) Vernier callipers  B) Metre rule  C) Tape measure  D) Scale",
            "The gravitational acceleration on Earth's surface is approximately: A) 9.8 m/s²  B) 10 m/s²  C) 8.9 m/s²  D) 11 m/s²",
            "Friction always acts in a direction: A) Opposite to motion  B) Same as motion  C) Perpendicular to motion  D) At 45° to motion",
        ],
        "short_questions": [
            "Define physical quantities. Distinguish between fundamental and derived quantities.",
            "Explain the concept of friction. What are its advantages and disadvantages?",
            "State and explain Bernoulli's principle with one real-life application.",
        ],
        "long_questions": [
            "Describe the motion graphs: distance-time and speed-time. Explain how to determine velocity, acceleration, and distance from these graphs.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 10", "subject": "Physics", "paper_id": "pk_fbise_c10_phy_01",
        "mcqs": [
            "The phenomenon of self-inductance occurs due to: A) Changing current in a coil  B) Constant current  C) Static charges  D) Light waves",
            "Which mirror forms a virtual, diminished image for any position of the object? A) Convex mirror  B) Concave mirror  C) Plane mirror  D) Parabolic mirror",
            "The energy equivalent of 1 atomic mass unit (1 u) is: A) 931.5 MeV  B) 931.5 eV  C) 9.315 MeV  D) 1 MeV",
        ],
        "short_questions": [
            "Explain electromagnetic induction using Lenz's Law.",
            "What is meant by nuclear binding energy? Why are heavier nuclei less stable?",
            "Describe the construction of a convex mirror. State its applications.",
        ],
        "long_questions": [
            "Explain the production of X-rays. Describe their properties and medical applications.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 9", "subject": "Chemistry", "paper_id": "pk_fbise_c9_chem_01",
        "mcqs": [
            "The symbol of gold is: A) Au  B) Ag  C) Fe  D) Cu",
            "Which of the following is an exothermic reaction? A) Combustion  B) Photosynthesis  C) Electrolysis  D) Evaporation",
            "A heterogeneous mixture is one in which: A) Components are not uniformly distributed  B) Components cannot be separated  C) All components are the same  D) Only one component is present",
        ],
        "short_questions": [
            "Define electrovalent bond. Write the formation of NaCl using electron dot structure.",
            "Distinguish between exothermic and endothermic reactions with examples.",
            "What is Dalton's Atomic Theory? State its main postulates.",
        ],
        "long_questions": [
            "Explain the Modern Atomic Theory. Describe the positions of subatomic particles and write electronic configurations of Na, Cl, and Ca.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 10", "subject": "Chemistry", "paper_id": "pk_fbise_c10_chem_01",
        "mcqs": [
            "Which type of reaction is CH₄ + 2O₂ → CO₂ + 2H₂O? A) Combustion  B) Decomposition  C) Double displacement  D) Single displacement",
            "Ethanol has the formula: A) C₂H₅OH  B) CH₃OH  C) C₃H₇OH  D) C₄H₉OH",
        ],
        "short_questions": [
            "Define saturated and unsaturated hydrocarbons. Give examples.",
            "What is the difference between fermentation and combustion?",
        ],
        "long_questions": [
            "Describe the properties and uses of ethanol. How is it produced by fermentation? Write the chemical equation.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 9", "subject": "Biology", "paper_id": "pk_fbise_c9_bio_01",
        "mcqs": [
            "The study of classification of organisms is called: A) Taxonomy  B) Ecology  C) Physiology  D) Morphology",
            "Bacteria are: A) Prokaryotes  B) Eukaryotes  C) Viruses  D) Fungi",
        ],
        "short_questions": [
            "Define and explain the five-kingdom system of classification.",
            "What are the differences between plant and animal cells?",
            "Describe the role of cell membrane in controlling transport.",
        ],
        "long_questions": [
            "Explain biological diversity. Describe the factors that threaten biodiversity and suggest conservation measures.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 10", "subject": "Biology", "paper_id": "pk_fbise_c10_bio_01",
        "mcqs": [
            "The largest organ in the human body is: A) Skin  B) Liver  C) Brain  D) Lung",
            "The male gamete in humans is called: A) Sperm  B) Ovum  C) Zygote  D) Embryo",
        ],
        "short_questions": [
            "What is the role of the placenta in human development?",
            "Explain the process of protein synthesis in a cell.",
        ],
        "long_questions": [
            "Describe the human reproductive system. Explain the menstrual cycle and the role of hormones.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 11", "subject": "Physics", "paper_id": "pk_fbise_c11_phy_01",
        "mcqs": [
            "The centre of mass of a uniform rod is at: A) Its midpoint  B) One end  C) One-third length  D) Two-thirds length",
            "Centripetal acceleration is directed: A) Toward the centre  B) Away from the centre  C) Tangentially  D) Radially outward",
        ],
        "short_questions": [
            "Derive the formula for the time period of a satellite in circular orbit.",
            "Define angular momentum. State the law of conservation of angular momentum.",
        ],
        "long_questions": [
            "Explain rotational motion. Derive the equations of rotational motion analogous to linear motion equations.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 12", "subject": "Physics", "paper_id": "pk_fbise_c12_phy_01",
        "mcqs": [
            "The output of a full-wave rectifier uses: A) Both half cycles of AC  B) Only positive half  C) Only negative half  D) No cycles",
            "In an NPN transistor, the majority carriers in the base are: A) Holes  B) Electrons  C) Protons  D) Neutrons",
        ],
        "short_questions": [
            "Explain the operation of a Zener diode. Describe its use as a voltage regulator.",
            "Define alpha and beta decay. Write example nuclear equations.",
        ],
        "long_questions": [
            "Explain digital electronics: logic gates (AND, OR, NOT, NAND, NOR, XOR). Draw truth tables and describe their applications in computers.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 11", "subject": "Mathematics", "paper_id": "pk_fbise_c11_math_01",
        "mcqs": [
            "The number of solutions of sin x = 1/2 in [0, 2π] is: A) 2  B) 1  C) 4  D) 0",
            "The inverse of matrix [[1,2],[3,4]] has determinant: A) -1/2  B) -2  C) 2  D) 1/2",
        ],
        "short_questions": [
            "Solve the equation 2sin²θ - sinθ - 1 = 0 for 0° ≤ θ ≤ 360°.",
            "Find the inverse of the matrix [[2,3],[1,4]].",
        ],
        "long_questions": [
            "Prove the compound angle formulae: sin(A+B) = sinAcosB + cosAsinB and cos(A+B) = cosAcosB - sinAsinB. Use them to derive double angle formulae.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 12", "subject": "Mathematics", "paper_id": "pk_fbise_c12_math_01",
        "mcqs": [
            "The sum of an infinite geometric series with |r| < 1 is: A) a/(1-r)  B) a/(1+r)  C) ar/(1-r)  D) a(1-r)",
            "The partial fraction of 1/(x²-1) involves: A) 1/(x-1) and 1/(x+1)  B) 1/x²  C) 1/(x-1)²  D) x/(x²-1)",
        ],
        "short_questions": [
            "Resolve into partial fractions: (3x+5)/((x-1)(x+2)).",
            "Evaluate: limₓ→0 (1 - cos x)/x².",
        ],
        "long_questions": [
            "Describe the trapezoidal rule and Simpson's rule for numerical integration. Apply them to estimate ∫₀¹ eˣ dx using 4 intervals.",
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# Seeder function
# ═══════════════════════════════════════════════════════════════════════════════

def _make_id(prefix: str, index: int, text: str) -> str:
    return hashlib.md5(f"{prefix}_{index}_{text[:40]}".encode()).hexdigest()


def _seed_inline_papers(documents, metadatas):
    """Expand SEED_PAPERS into individual question vectors."""
    for paper in SEED_PAPERS:
        country    = paper["country"]
        category   = paper["category"]
        class_name = paper["class_name"]
        subject    = paper["subject"]
        paper_id   = paper.get("paper_id", "unknown")

        base_meta = {
            "country":    country,
            "category":   category,
            "class_name": class_name,
            "subject":    subject,
            "paper_type": "verified",
            "paper_id":   paper_id,
            "filename":   f"{paper_id}.pdf",
            "timestamp":  _TIMESTAMP,
        }

        for q in paper.get("mcqs", []):
            if q.strip():
                documents.append(q.strip())
                metadatas.append({**base_meta, "question_type": "mcq"})

        for q in paper.get("short_questions", []):
            if q.strip():
                documents.append(q.strip())
                metadatas.append({**base_meta, "question_type": "short"})

        for q in paper.get("long_questions", []):
            if q.strip():
                documents.append(q.strip())
                metadatas.append({**base_meta, "question_type": "long"})


def _seed_from_mock_data(documents, metadatas):
    """Load questions from mock_data.json and append to lists."""
    if not os.path.exists(_DATA_PATH):
        return
    try:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[Seed] Failed to load mock_data.json: {e}")
        return

    entries = data if isinstance(data, list) else data.get("papers", [data])
    for paper in entries:
        subject    = str(paper.get("subject",    "General"))
        class_name = str(paper.get("class",      paper.get("class_name", paper.get("exam_type", "General"))))
        country    = str(paper.get("country",    "General"))
        category   = str(paper.get("category",   paper.get("exam_type",  "General")))

        base_meta = {
            "country":    country,
            "category":   category,
            "class_name": class_name,
            "subject":    subject,
            "paper_type": "verified",
            "paper_id":   paper.get("hash", "mock"),
            "filename":   "mock_data.json",
            "timestamp":  _TIMESTAMP,
        }

        for mcq in paper.get("mcqs", []):
            text = mcq if isinstance(mcq, str) else mcq.get("text", mcq.get("question", ""))
            if text.strip():
                documents.append(text.strip())
                metadatas.append({**base_meta, "question_type": "mcq"})

        for sq in paper.get("short_questions", []):
            text = sq if isinstance(sq, str) else sq.get("text", sq.get("question", ""))
            if text.strip():
                documents.append(text.strip())
                metadatas.append({**base_meta, "question_type": "short"})

        for lq in paper.get("long_questions", []):
            text = lq if isinstance(lq, str) else lq.get("text", lq.get("question", ""))
            if text.strip():
                documents.append(text.strip())
                metadatas.append({**base_meta, "question_type": "long"})


def seed_verified_store() -> None:
    """
    Load all questions into the verified ChromaDB collection.
    Sources: SEED_PAPERS (inline) + mock_data.json (legacy).
    Idempotent — skips if collection already populated.
    """
    from services.vector_store import verified_col, add_to_verified

    existing_count = verified_col.count()
    if existing_count > 0:
        print(f"[Seed] Verified store already has {existing_count} documents — skipping.")
        return

    print("[Seed] Building verified store …")
    documents = []
    metadatas = []

    # 1. Inline structured papers (all classes/boards)
    _seed_inline_papers(documents, metadatas)
    print(f"[Seed] Inline papers: {len(documents)} questions")

    # 2. Legacy mock_data.json
    before = len(documents)
    _seed_from_mock_data(documents, metadatas)
    print(f"[Seed] mock_data.json: {len(documents) - before} additional questions")

    if not documents:
        print("[Seed] No documents to seed.")
        return

    # Cap to avoid excessive memory on startup
    MAX_DOCS = 8000
    if len(documents) > MAX_DOCS:
        print(f"[Seed] Capping at {MAX_DOCS} docs (total={len(documents)}).")
        documents = documents[:MAX_DOCS]
        metadatas = metadatas[:MAX_DOCS]

    ids = [_make_id("verified", i, d) for i, d in enumerate(documents)]
    print(f"[Seed] Upserting {len(documents)} questions into verified store …")
    add_to_verified(documents, metadatas, ids)
    print(f"[Seed] Done. Verified store now has {verified_col.count()} documents.")


if __name__ == "__main__":
    seed_verified_store()
