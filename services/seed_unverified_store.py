"""
Seed the Unverified ChromaDB collection with international sample exam papers.

Coverage:
  UK         > Board Exam, Mid Term, Final Term, Quiz  > O Level, A Level
  USA        > Board Exam, Mid Term, Final Term, Quiz  > Grade 9-12
  India      > Board Exam, Mid Term, Final Term, Quiz  > Class 9-12
  Australia  > Board Exam, Mid Term, Final Term, Quiz  > Year 10-12
  Canada     > Board Exam, Mid Term, Final Term, Quiz  > Grade 10-12

Subjects: Mathematics, Physics, Chemistry, Biology, Computer Science, English

Papers are stored DIRECTLY in the Unverified Vector DB
(no file system storage required).

IMPORTANT: Pakistan boards (Punjab Boards, Cambridge, Federal Board) belong
ONLY in the Verified DB and must NOT appear here.

Run automatically on startup or manually:
    python -m services.seed_unverified_store
"""

import os
import hashlib
import datetime
from typing import List, Dict

_TIMESTAMP = datetime.datetime.utcnow().isoformat()


# ═══════════════════════════════════════════════════════════════════════════════
# Seed papers — international boards only
# Countries: UK, USA, India, Australia, Canada
# Categories: Board Exam, Mid Term, Final Term, Quiz
# ═══════════════════════════════════════════════════════════════════════════════

UNVERIFIED_SEED_PAPERS: List[Dict] = [

    # ══════════════════════════════════════════════════════════════════════════
    # UK — Board Exam
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "UK", "category": "Board Exam", "class_name": "O Level", "subject": "Physics",
        "paper_id": "uk_board_olevel_phy_01",
        "mcqs": [
            "Which quantity is a vector? A) Speed  B) Mass  C) Velocity  D) Temperature",
            "The unit of electrical resistance is: A) Ohm  B) Ampere  C) Volt  D) Watt",
            "Light travels fastest in: A) Vacuum  B) Water  C) Glass  D) Air",
            "Which type of wave requires a medium to travel? A) Sound  B) Light  C) X-rays  D) Radio waves",
        ],
        "short_questions": [
            "State Ohm's Law. Under what conditions does a conductor obey Ohm's Law?",
            "Explain the difference between series and parallel circuits. Give one advantage of each.",
            "Define work done. When is work done zero even if force is applied?",
        ],
        "long_questions": [
            "Describe the photoelectric effect. What evidence does it provide for the particle nature of light? Explain Einstein's photoelectric equation.",
            "Explain how a transformer works. Derive the turns ratio equation. Distinguish between step-up and step-down transformers.",
        ],
    },

    {
        "country": "UK", "category": "Board Exam", "class_name": "A Level", "subject": "Chemistry",
        "paper_id": "uk_board_alevel_chem_01",
        "mcqs": [
            "Which of the following is a nucleophile? A) NH₃  B) BF₃  C) AlCl₃  D) H⁺",
            "The IUPAC name of CH₃CHO is: A) Ethanal  B) Ethanol  C) Ethanoic acid  D) Methanol",
            "The rate-determining step is: A) The slowest step  B) The first step  C) The last step  D) The fastest step",
        ],
        "short_questions": [
            "Explain the mechanism of nucleophilic addition to carbonyl compounds. Give one example.",
            "Define buffer solution. Calculate the pH of a buffer made from 0.2 M CH₃COOH and 0.2 M CH₃COONa (Ka = 1.8×10⁻⁵).",
            "What is enthalpy of neutralization? Why is it approximately constant for strong acid-base reactions?",
        ],
        "long_questions": [
            "Describe the mechanism of electrophilic aromatic substitution. Explain nitration and halogenation of benzene with reaction conditions.",
            "Explain reaction kinetics. Define rate constant, activation energy, and Arrhenius equation. How does temperature affect reaction rate?",
        ],
    },

    {
        "country": "UK", "category": "Board Exam", "class_name": "A Level", "subject": "Biology",
        "paper_id": "uk_board_alevel_bio_01",
        "mcqs": [
            "The site of oxidative phosphorylation is: A) Inner mitochondrial membrane  B) Cytoplasm  C) Nucleus  D) Ribosome",
            "Which molecule carries amino acids to the ribosome during translation? A) tRNA  B) mRNA  C) rRNA  D) DNA",
            "Hardy-Weinberg equilibrium requires: A) No mutation, migration, or selection  B) Small population  C) Random genetic drift  D) Natural selection",
        ],
        "short_questions": [
            "Describe the structure and function of the nephron. How is urine concentrated?",
            "Explain gene expression regulation in eukaryotes. What is the role of transcription factors?",
            "Define population genetics. What are the assumptions of the Hardy-Weinberg principle?",
        ],
        "long_questions": [
            "Describe the electron transport chain and chemiosmosis. How is ATP synthesized during aerobic respiration?",
            "Explain the immune system: innate vs. adaptive immunity, role of B and T cells, and the mechanism of vaccination.",
        ],
    },

    {
        "country": "UK", "category": "Board Exam", "class_name": "O Level", "subject": "Mathematics",
        "paper_id": "uk_board_olevel_math_01",
        "mcqs": [
            "The sum of interior angles of a hexagon is: A) 720°  B) 360°  C) 540°  D) 900°",
            "If f(x) = 2x + 3, then f⁻¹(x) = : A) (x-3)/2  B) (x+3)/2  C) 2x-3  D) x/2",
            "The HCF of 24 and 36 is: A) 12  B) 6  C) 8  D) 4",
        ],
        "short_questions": [
            "Solve the quadratic equation x² - 7x + 12 = 0 by factorisation.",
            "A rectangle has length (2x+3) cm and width (x-1) cm. Write an expression for the area. If area = 18 cm², find x.",
            "Calculate the nth term and the 20th term of the sequence: 3, 7, 11, 15, ...",
        ],
        "long_questions": [
            "Prove that the angle in a semicircle is 90°. Apply this to solve: Given a circle with diameter AB, C is a point on the circle. Find ∠ACB.",
            "Describe and apply trigonometry: In a triangle ABC, AB = 8 cm, BC = 6 cm, ∠B = 90°. Find AC, sin A, and cos A.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # UK — Mid Term
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "UK", "category": "Mid Term", "class_name": "A Level", "subject": "Physics",
        "paper_id": "uk_mid_alevel_phy_01",
        "mcqs": [
            "The dimension of electric field intensity is: A) MLT⁻³A⁻¹  B) MLT⁻²A⁻¹  C) ML²T⁻²A  D) MT⁻¹A",
            "At which point in SHM is kinetic energy maximum? A) Mean position  B) Extreme position  C) Midway  D) At equilibrium always",
        ],
        "short_questions": [
            "Derive the expression for the energy stored in a capacitor.",
            "Explain what is meant by the work function of a metal.",
        ],
        "long_questions": [
            "Explain Faraday's laws of electromagnetic induction. Describe Lenz's law and its significance for energy conservation.",
        ],
    },

    {
        "country": "UK", "category": "Mid Term", "class_name": "O Level", "subject": "Biology",
        "paper_id": "uk_mid_olevel_bio_01",
        "mcqs": [
            "Which organ produces bile? A) Liver  B) Pancreas  C) Stomach  D) Small intestine",
            "Anaerobic respiration in yeast produces: A) Ethanol and CO₂  B) Lactic acid  C) Water and CO₂  D) ATP only",
        ],
        "short_questions": [
            "Explain the process of osmosis. How does it affect plant cells in different solutions?",
            "Describe the function of the alveoli in gas exchange.",
        ],
        "long_questions": [
            "Describe how the human heart pumps blood. Explain the cardiac cycle including systole and diastole.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # UK — Final Term
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "UK", "category": "Final Term", "class_name": "A Level", "subject": "Mathematics",
        "paper_id": "uk_final_alevel_math_01",
        "mcqs": [
            "The derivative of tan x is: A) sec²x  B) cosec²x  C) -sec²x  D) sin x",
            "The integral of 1/(1+x²) is: A) arctan x + C  B) arcsin x + C  C) ln(1+x²) + C  D) -arctan x + C",
        ],
        "short_questions": [
            "Find the stationary points of f(x) = x³ - 3x² - 9x + 5 and classify them.",
            "Use integration by parts to evaluate ∫ x cos x dx.",
        ],
        "long_questions": [
            "Explain the Fundamental Theorem of Calculus. Evaluate ∫₀π sin x dx and interpret geometrically.",
        ],
    },

    {
        "country": "UK", "category": "Final Term", "class_name": "O Level", "subject": "Computer Science",
        "paper_id": "uk_final_olevel_cs_01",
        "mcqs": [
            "Which data structure is used for BFS? A) Queue  B) Stack  C) Tree  D) Linked list",
            "The two's complement of 0101 is: A) 1011  B) 1010  C) 1100  D) 1001",
        ],
        "short_questions": [
            "Write pseudocode to find the largest element in an array of n integers.",
            "Explain the difference between a compiler and an interpreter.",
        ],
        "long_questions": [
            "Describe the OSI model. Explain the role of each layer and how data is encapsulated as it moves down the stack.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # UK — Quiz
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "UK", "category": "Quiz", "class_name": "A Level", "subject": "Chemistry",
        "paper_id": "uk_quiz_alevel_chem_01",
        "mcqs": [
            "Grignard reagents are: A) Organomagnesium halides  B) Organolithium compounds  C) Sodium amalgams  D) Boron compounds",
            "The reaction of alkene with HBr follows: A) Markovnikov's rule  B) Anti-Markovnikov's rule  C) Zaitsev's rule  D) Hückel's rule",
            "Which acid is used in nitration of benzene? A) H₂SO₄  B) HCl  C) HNO₃  D) Both A and C",
            "SN2 reactions are favoured by: A) Primary substrates  B) Tertiary substrates  C) Polar protic solvents  D) Carbocation stability",
        ],
        "short_questions": [
            "Distinguish between SN1 and SN2 mechanisms. Which substrate favours each?",
        ],
        "long_questions": [],
    },

    {
        "country": "UK", "category": "Quiz", "class_name": "O Level", "subject": "Physics",
        "paper_id": "uk_quiz_olevel_phy_01",
        "mcqs": [
            "Which electromagnetic wave has the shortest wavelength? A) Gamma rays  B) X-rays  C) Ultraviolet  D) Radio waves",
            "The density of water is: A) 1000 kg/m³  B) 100 kg/m³  C) 10000 kg/m³  D) 500 kg/m³",
            "An object moving in a circle at constant speed has: A) Constant acceleration  B) Zero acceleration  C) Zero velocity  D) Constant velocity",
            "Which instrument measures atmospheric pressure? A) Barometer  B) Manometer  C) Ammeter  D) Voltmeter",
        ],
        "short_questions": [
            "Explain the difference between mass and weight.",
        ],
        "long_questions": [],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # USA — Board Exam
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "USA", "category": "Board Exam", "class_name": "Grade 11", "subject": "Physics",
        "paper_id": "usa_board_g11_phy_01",
        "mcqs": [
            "Newton's second law states that F = : A) ma  B) mv  C) m/a  D) a/m",
            "The unit of frequency is: A) Hertz  B) Newton  C) Joule  D) Pascal",
            "Which type of energy is stored in a compressed spring? A) Elastic potential energy  B) Kinetic energy  C) Thermal energy  D) Chemical energy",
            "The speed of light in a vacuum is: A) 3×10⁸ m/s  B) 3×10⁶ m/s  C) 3×10¹⁰ m/s  D) 3×10⁵ m/s",
        ],
        "short_questions": [
            "A 5 kg object is accelerated at 4 m/s². Calculate the net force acting on it.",
            "Define projectile motion. What is the shape of the projectile's path?",
            "Explain the conservation of energy using the example of a roller coaster.",
        ],
        "long_questions": [
            "Describe Newton's Laws of Motion with real-world examples. Derive the impulse-momentum theorem from Newton's Second Law.",
            "Explain the concept of work, energy, and power. Derive the work-energy theorem. Calculate the power output of an engine that lifts 200 kg by 10 m in 5 seconds.",
        ],
    },

    {
        "country": "USA", "category": "Board Exam", "class_name": "Grade 12", "subject": "Chemistry",
        "paper_id": "usa_board_g12_chem_01",
        "mcqs": [
            "Which of the following is a Lewis acid? A) BF₃  B) NH₃  C) H₂O  D) OH⁻",
            "The molar mass of NaCl is: A) 58.5 g/mol  B) 23 g/mol  C) 35.5 g/mol  D) 40 g/mol",
            "Entropy is a measure of: A) Disorder in a system  B) Energy content  C) Temperature  D) Pressure",
        ],
        "short_questions": [
            "Explain Le Chatelier's Principle with an example involving the Haber Process.",
            "Define electronegativity. How does it trend across a period and down a group?",
            "What is a buffer solution? Describe how it resists pH changes.",
        ],
        "long_questions": [
            "Describe the thermodynamics of chemical reactions. Define ΔH, ΔS, and ΔG. Under what conditions is a reaction spontaneous?",
            "Explain electrochemical cells. Describe the Daniell cell, write half-reactions, and calculate EMF using standard electrode potentials.",
        ],
    },

    {
        "country": "USA", "category": "Board Exam", "class_name": "Grade 10", "subject": "Biology",
        "paper_id": "usa_board_g10_bio_01",
        "mcqs": [
            "Photosynthesis takes place in: A) Chloroplasts  B) Mitochondria  C) Ribosomes  D) Vacuoles",
            "Which molecule carries genetic information? A) DNA  B) Protein  C) Lipid  D) Carbohydrate",
            "The process by which cells divide to produce gametes is: A) Meiosis  B) Mitosis  C) Binary fission  D) Budding",
        ],
        "short_questions": [
            "Explain the difference between aerobic and anaerobic respiration with equations.",
            "Describe the structure of DNA. What does the base-pairing rule state?",
            "What is natural selection? Give an example of adaptation.",
        ],
        "long_questions": [
            "Describe the cell cycle including mitosis phases. Why is mitosis important for organisms?",
            "Explain the flow of energy through an ecosystem. Describe producers, consumers, and decomposers with examples.",
        ],
    },

    {
        "country": "USA", "category": "Board Exam", "class_name": "Grade 12", "subject": "Mathematics",
        "paper_id": "usa_board_g12_math_01",
        "mcqs": [
            "The derivative of sin x is: A) cos x  B) -cos x  C) -sin x  D) tan x",
            "limₓ→∞ (1/x) = : A) 0  B) 1  C) ∞  D) -1",
            "∫ eˣ dx = : A) eˣ + C  B) eˣ·x + C  C) 1/eˣ + C  D) ln x + C",
        ],
        "short_questions": [
            "Find the derivative of f(x) = x⁴ - 3x³ + 2x - 7.",
            "Evaluate the definite integral ∫₀² (x² + 1) dx.",
            "Solve the system: 2x + y = 5 and x - y = 1.",
        ],
        "long_questions": [
            "Explain limits and continuity. Evaluate lim_{x→2} (x²-4)/(x-2) and explain the concept of indeterminate forms.",
            "Describe sequences and series. Derive the formula for the sum of a geometric series. Find the sum of 1 + 1/2 + 1/4 + ... to infinity.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # USA — Mid Term
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "USA", "category": "Mid Term", "class_name": "Grade 11", "subject": "Chemistry",
        "paper_id": "usa_mid_g11_chem_01",
        "mcqs": [
            "An exothermic reaction: A) Releases heat  B) Absorbs heat  C) Produces light only  D) Has no energy change",
            "The number of protons in an atom determines its: A) Atomic number  B) Mass number  C) Neutron count  D) Electron count",
        ],
        "short_questions": [
            "What is the difference between ionic and covalent bonds? Give one example of each.",
            "Calculate the molarity of a solution containing 5.85 g of NaCl dissolved in 500 mL of water.",
        ],
        "long_questions": [
            "Explain the periodic table trends: atomic radius, ionization energy, and electronegativity. Describe why these trends occur.",
        ],
    },

    {
        "country": "USA", "category": "Mid Term", "class_name": "Grade 10", "subject": "Mathematics",
        "paper_id": "usa_mid_g10_math_01",
        "mcqs": [
            "The slope of a vertical line is: A) Undefined  B) 0  C) 1  D) -1",
            "The quadratic formula is: A) x = (-b ± √(b²-4ac))/2a  B) x = -b/2a  C) x = b/a  D) x = √(b²-4ac)",
        ],
        "short_questions": [
            "Solve the equation 3x² - 12 = 0.",
            "Find the distance between points (3, 4) and (0, 0).",
        ],
        "long_questions": [
            "Explain functions and their graphs. Describe domain, range, and identify if f(x) = x² is even, odd, or neither.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # USA — Final Term
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "USA", "category": "Final Term", "class_name": "Grade 12", "subject": "Computer Science",
        "paper_id": "usa_final_g12_cs_01",
        "mcqs": [
            "Big-O notation O(log n) represents: A) Logarithmic time  B) Linear time  C) Quadratic time  D) Constant time",
            "A linked list node contains: A) Data and a pointer  B) Only data  C) Only a pointer  D) An array",
        ],
        "short_questions": [
            "Explain the concept of recursion with the factorial function as an example.",
            "What is a hash table? Explain collision resolution using chaining.",
        ],
        "long_questions": [
            "Compare sorting algorithms: bubble sort, merge sort, and quicksort. Analyze their time complexity for best, average, and worst cases.",
        ],
    },

    {
        "country": "USA", "category": "Final Term", "class_name": "Grade 11", "subject": "Biology",
        "paper_id": "usa_final_g11_bio_01",
        "mcqs": [
            "Which organelle is known as the powerhouse of the cell? A) Mitochondria  B) Nucleus  C) Ribosome  D) Chloroplast",
            "The Central Dogma of molecular biology states that information flows: A) DNA → RNA → Protein  B) Protein → RNA → DNA  C) RNA → DNA → Protein  D) DNA → Protein → RNA",
        ],
        "short_questions": [
            "Describe the process of transcription. Where does it occur in eukaryotes?",
            "Explain the difference between dominant and recessive alleles with a Punnett square example.",
        ],
        "long_questions": [
            "Describe genetic engineering and biotechnology. Explain the use of restriction enzymes, PCR, and gel electrophoresis in recombinant DNA technology.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # USA — Quiz
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "USA", "category": "Quiz", "class_name": "Grade 11", "subject": "Physics",
        "paper_id": "usa_quiz_g11_phy_01",
        "mcqs": [
            "The unit of electric charge is: A) Coulomb  B) Ampere  C) Volt  D) Ohm",
            "Ohm's Law states: A) V = IR  B) V = I/R  C) I = V²/R  D) R = VI",
            "Which type of wave is a light wave? A) Transverse  B) Longitudinal  C) Both  D) Neither",
            "The period of a pendulum depends on: A) Length only  B) Mass only  C) Both length and mass  D) Amplitude",
        ],
        "short_questions": [
            "Calculate the resistance of a wire if V = 12 V and I = 3 A.",
        ],
        "long_questions": [],
    },

    {
        "country": "USA", "category": "Quiz", "class_name": "Grade 10", "subject": "Chemistry",
        "paper_id": "usa_quiz_g10_chem_01",
        "mcqs": [
            "The pH of a neutral solution is: A) 7  B) 0  C) 14  D) 1",
            "Which of the following is a noble gas? A) Argon  B) Sodium  C) Chlorine  D) Oxygen",
            "An acid turns litmus paper: A) Red  B) Blue  C) Green  D) Yellow",
            "The chemical formula of water is: A) H₂O  B) H₂O₂  C) HO  D) OH₂",
        ],
        "short_questions": [
            "Define an element and a compound. Give one example of each.",
        ],
        "long_questions": [],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # India — Board Exam
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "India", "category": "Board Exam", "class_name": "Class 10", "subject": "Physics",
        "paper_id": "india_board_c10_phy_01",
        "mcqs": [
            "Ohm's Law is valid when temperature is: A) Constant  B) Increasing  C) Decreasing  D) Changing rapidly",
            "The SI unit of magnetic flux density is: A) Tesla  B) Weber  C) Gauss  D) Henry",
            "A convex lens is also called a: A) Converging lens  B) Diverging lens  C) Flat lens  D) Concave lens",
        ],
        "short_questions": [
            "State and explain Fleming's Left Hand Rule.",
            "What is electromagnetic induction? State Faraday's first law.",
            "Explain the working of a simple electric motor.",
        ],
        "long_questions": [
            "Describe the construction and working of an AC generator. Explain how sinusoidal EMF is produced.",
            "Explain refraction of light through a glass prism. Describe dispersion and the formation of a spectrum.",
        ],
    },

    {
        "country": "India", "category": "Board Exam", "class_name": "Class 12", "subject": "Chemistry",
        "paper_id": "india_board_c12_chem_01",
        "mcqs": [
            "The process of making glucose from CO₂ and H₂O using sunlight is: A) Photosynthesis  B) Glycolysis  C) Fermentation  D) Respiration",
            "Which type of isomerism is shown by optical isomers? A) Stereoisomerism  B) Structural isomerism  C) Position isomerism  D) Chain isomerism",
            "The IUPAC name of glycerol is: A) Propan-1,2,3-triol  B) Ethanol  C) Propan-1-ol  D) Glycerine",
        ],
        "short_questions": [
            "Explain the Cannizzaro reaction with an example.",
            "What is Fehling's test? What does it detect?",
            "Describe the preparation of ethanol by fermentation.",
        ],
        "long_questions": [
            "Describe the mechanisms of substitution reactions: SN1 and SN2. Compare stereochemical outcomes of each.",
            "Explain polymers: addition and condensation polymerization. Give two examples of each with monomers and uses.",
        ],
    },

    {
        "country": "India", "category": "Board Exam", "class_name": "Class 11", "subject": "Mathematics",
        "paper_id": "india_board_c11_math_01",
        "mcqs": [
            "The number of ways to arrange 6 people in a row is: A) 720  B) 120  C) 360  D) 60",
            "The value of cos 2θ in terms of cos θ is: A) 2cos²θ - 1  B) 2sinθcosθ  C) 1 - 2sin²θ  D) Both A and C",
            "The general term of AP is: A) a + (n-1)d  B) arⁿ⁻¹  C) n(a+l)/2  D) a/(1-r)",
        ],
        "short_questions": [
            "Find the number of permutations of the letters in 'MATHEMATICS'.",
            "Prove: sin(A + B)·sin(A - B) = sin²A - sin²B.",
            "The 5th term of an AP is 17 and the 10th term is 32. Find the AP.",
        ],
        "long_questions": [
            "State and prove the binomial theorem for positive integer n. Expand (1 + x)⁶ and find the coefficient of x³.",
            "Explain trigonometric functions. Derive the formula for sin(A + B). Use it to find sin 75°.",
        ],
    },

    {
        "country": "India", "category": "Board Exam", "class_name": "Class 12", "subject": "Biology",
        "paper_id": "india_board_c12_bio_01",
        "mcqs": [
            "The technique used to amplify DNA is: A) PCR  B) Gel electrophoresis  C) ELISA  D) Southern blotting",
            "Which enzyme cuts DNA at specific sequences? A) Restriction endonuclease  B) DNA polymerase  C) RNA polymerase  D) Ligase",
            "The antisense RNA approach is used in: A) Gene silencing  B) Translation  C) DNA replication  D) Transcription",
        ],
        "short_questions": [
            "Explain the process of cloning a gene into a plasmid vector.",
            "What is biodiversity? Describe its types and significance.",
            "Explain ex situ conservation. Give two examples.",
        ],
        "long_questions": [
            "Describe the human reproductive system. Explain the menstrual cycle including the role of FSH, LH, estrogen, and progesterone.",
            "Explain the application of biotechnology in medicine and agriculture. Give specific examples of genetically modified organisms.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # India — Mid Term
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "India", "category": "Mid Term", "class_name": "Class 10", "subject": "Mathematics",
        "paper_id": "india_mid_c10_math_01",
        "mcqs": [
            "The roots of ax² + bx + c = 0 are real and equal when: A) b²= 4ac  B) b² > 4ac  C) b² < 4ac  D) b = 0",
            "tan 45° = : A) 1  B) 0  C) √3  D) 1/√2",
        ],
        "short_questions": [
            "If the sum of zeroes of x² - kx + 6 is 3, find k.",
            "Find the roots of the equation 2x² - 5x + 3 = 0.",
        ],
        "long_questions": [
            "State and prove the Pythagoras theorem. Apply it to determine if a triangle with sides 5, 12, 13 is right-angled.",
        ],
    },

    {
        "country": "India", "category": "Mid Term", "class_name": "Class 11", "subject": "Physics",
        "paper_id": "india_mid_c11_phy_01",
        "mcqs": [
            "The dimension of velocity is: A) LT⁻¹  B) LT  C) L²T⁻¹  D) MLT⁻²",
            "A scalar quantity has: A) Magnitude only  B) Direction only  C) Both magnitude and direction  D) Neither",
        ],
        "short_questions": [
            "Derive the equation of motion v² = u² + 2as from Newton's laws.",
            "Define projectile motion. Find the angle for maximum range.",
        ],
        "long_questions": [
            "Describe the law of universal gravitation. Derive expressions for gravitational field strength and potential.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # India — Final Term
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "India", "category": "Final Term", "class_name": "Class 12", "subject": "Computer Science",
        "paper_id": "india_final_c12_cs_01",
        "mcqs": [
            "In Python, which keyword is used to define a function? A) def  B) func  C) define  D) function",
            "Which SQL command removes a table from a database? A) DROP  B) DELETE  C) REMOVE  D) ERASE",
        ],
        "short_questions": [
            "What is a stack? Write Python code to implement push and pop operations.",
            "Explain the difference between primary key and foreign key in SQL.",
        ],
        "long_questions": [
            "Describe network topologies: bus, ring, star, and mesh. Compare their advantages and disadvantages.",
        ],
    },

    {
        "country": "India", "category": "Final Term", "class_name": "Class 10", "subject": "Biology",
        "paper_id": "india_final_c10_bio_01",
        "mcqs": [
            "The functional unit of the kidney is: A) Nephron  B) Neuron  C) Alveolus  D) Follicle",
            "Which part of the brain controls voluntary actions? A) Cerebrum  B) Cerebellum  C) Medulla  D) Hypothalamus",
        ],
        "short_questions": [
            "Describe the process of urine formation in the nephron.",
            "What is a reflex arc? Describe its components with a diagram description.",
        ],
        "long_questions": [
            "Explain the human digestive system. Describe the role of each organ and the enzymes involved in digestion.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # India — Quiz
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "India", "category": "Quiz", "class_name": "Class 11", "subject": "Chemistry",
        "paper_id": "india_quiz_c11_chem_01",
        "mcqs": [
            "Which of the following has the highest ionization energy? A) Ne  B) Na  C) K  D) Li",
            "The bond angle in water is approximately: A) 104.5°  B) 90°  C) 109.5°  D) 120°",
            "Which law states that at constant pressure, volume is proportional to temperature? A) Charles's Law  B) Boyle's Law  C) Avogadro's Law  D) Dalton's Law",
            "The molar volume of an ideal gas at STP is: A) 22.4 L  B) 22.4 mL  C) 11.2 L  D) 44.8 L",
        ],
        "short_questions": [
            "State Avogadro's Law. Calculate the volume of 3 mol of ideal gas at STP.",
        ],
        "long_questions": [],
    },

    {
        "country": "India", "category": "Quiz", "class_name": "Class 12", "subject": "Physics",
        "paper_id": "india_quiz_c12_phy_01",
        "mcqs": [
            "A diode in forward bias allows: A) Current to flow easily  B) No current to flow  C) Current in reverse direction  D) None of these",
            "The wavelength associated with a particle is: A) De Broglie wavelength  B) Compton wavelength  C) X-ray wavelength  D) Sound wavelength",
            "Which gate is called a universal gate? A) NAND  B) AND  C) OR  D) NOT",
            "The half-life of a radioactive element is the time for: A) Half the atoms to decay  B) All atoms to decay  C) Double the atoms  D) One atom to decay",
        ],
        "short_questions": [
            "What is photoelectric effect? What is threshold frequency?",
        ],
        "long_questions": [],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Australia — Board Exam
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Australia", "category": "Board Exam", "class_name": "Year 12", "subject": "Physics",
        "paper_id": "aus_board_y12_phy_01",
        "mcqs": [
            "A proton moving through a magnetic field experiences: A) Magnetic force  B) Gravitational force  C) Electrostatic force  D) No force",
            "Young's double-slit experiment demonstrates: A) Wave nature of light  B) Particle nature of light  C) Speed of light  D) Colour of light",
            "The half-life of Carbon-14 is approximately: A) 5730 years  B) 1000 years  C) 100 years  D) 10000 years",
        ],
        "short_questions": [
            "Explain the phenomenon of diffraction. Under what conditions is it most pronounced?",
            "Derive the expression for the time period of a mass-spring system undergoing SHM.",
            "What is the photoelectric effect? Explain how it supports the quantum theory of light.",
        ],
        "long_questions": [
            "Explain Einstein's theory of special relativity. Describe time dilation and length contraction with mathematical expressions.",
            "Describe fission and fusion reactions. Compare their energy outputs and discuss their use in power generation.",
        ],
    },

    {
        "country": "Australia", "category": "Board Exam", "class_name": "Year 11", "subject": "Chemistry",
        "paper_id": "aus_board_y11_chem_01",
        "mcqs": [
            "Which of the following is an empirical formula? A) CH₂O  B) C₆H₁₂O₆  C) C₂H₄  D) H₂O₂",
            "Molar concentration is measured in: A) mol/L  B) g/L  C) mol/kg  D) L/mol",
            "An indicator is used to detect: A) The end point of a titration  B) Concentration of solution  C) Temperature change  D) Density change",
        ],
        "short_questions": [
            "Explain the difference between strong and weak acids. Give one example of each.",
            "Calculate the concentration of NaOH if 25 mL neutralises 20 mL of 0.1 M H₂SO₄.",
            "Describe the collision theory of reaction rates.",
        ],
        "long_questions": [
            "Explain the industrial significance of the Haber Process. Describe how equilibrium principles are applied to optimise ammonia production.",
            "Describe acid-base theories: Arrhenius, Brønsted-Lowry, and Lewis. Give one example for each theory.",
        ],
    },

    {
        "country": "Australia", "category": "Board Exam", "class_name": "Year 10", "subject": "Mathematics",
        "paper_id": "aus_board_y10_math_01",
        "mcqs": [
            "The gradient of the line y = -2x + 5 is: A) -2  B) 5  C) 2  D) -5",
            "The solution of |x - 3| = 4 is: A) x = 7 or x = -1  B) x = 7 only  C) x = -1 only  D) x = 1",
            "A circle with equation x² + y² = 25 has radius: A) 5  B) 25  C) 10  D) 5π",
        ],
        "short_questions": [
            "Expand and simplify (3x - 2)².",
            "Solve the simultaneous equations: y = 2x - 3 and y = -x + 6.",
            "Find the 15th term and sum of the first 15 terms of AP: 4, 9, 14, 19, ...",
        ],
        "long_questions": [
            "Prove the cosine rule: c² = a² + b² - 2ab cos C. Apply it to find the third side of a triangle with sides 6 cm, 8 cm and included angle 60°.",
            "Describe surface area and volume of 3D solids. Calculate the total surface area and volume of a cone with radius 3 cm and height 4 cm.",
        ],
    },

    {
        "country": "Australia", "category": "Board Exam", "class_name": "Year 12", "subject": "Biology",
        "paper_id": "aus_board_y12_bio_01",
        "mcqs": [
            "Speciation occurs when: A) Populations become reproductively isolated  B) Organisms migrate  C) Gene mutation rate increases  D) Offspring survive",
            "The term 'ecosystem' refers to: A) All organisms and their physical environment  B) All animals in an area  C) Producers only  D) Food web only",
        ],
        "short_questions": [
            "Explain allopatric speciation. Give one real-world example.",
            "Describe the role of decomposers in an ecosystem.",
            "What is artificial selection? How does it differ from natural selection?",
        ],
        "long_questions": [
            "Describe genetic variation in populations. Explain the mechanisms that maintain and increase variation: mutation, recombination, and migration.",
            "Discuss human impacts on biodiversity. Describe conservation strategies including in situ and ex situ approaches.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Australia — Mid Term
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Australia", "category": "Mid Term", "class_name": "Year 12", "subject": "Physics",
        "paper_id": "aus_mid_y12_phy_01",
        "mcqs": [
            "The unit of electric potential is: A) Volt  B) Joule  C) Coulomb  D) Ampere",
            "Which law relates electric field and charge distribution? A) Gauss's Law  B) Ohm's Law  C) Faraday's Law  D) Lenz's Law",
        ],
        "short_questions": [
            "Calculate the electric field at a distance of 0.5 m from a 2 μC point charge.",
            "Explain the difference between electric potential and electric field.",
        ],
        "long_questions": [
            "Derive the expression for the force between two parallel current-carrying conductors. Explain how this defines the ampere.",
        ],
    },

    {
        "country": "Australia", "category": "Mid Term", "class_name": "Year 11", "subject": "Mathematics",
        "paper_id": "aus_mid_y11_math_01",
        "mcqs": [
            "The domain of f(x) = √(x-2) is: A) x ≥ 2  B) x > 2  C) x ≤ 2  D) All real numbers",
            "If y = 3x² then dy/dx = : A) 6x  B) 3x  C) 6x²  D) x²",
        ],
        "short_questions": [
            "Differentiate f(x) = x³ + 5x² - 3x + 7.",
            "Find the turning point of y = x² - 6x + 8 and determine if it is a minimum or maximum.",
        ],
        "long_questions": [
            "Explain logarithms and exponential functions. Solve 2^(x+1) = 16 and log₃(x) + log₃(x-8) = 2.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Australia — Final Term
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Australia", "category": "Final Term", "class_name": "Year 12", "subject": "Chemistry",
        "paper_id": "aus_final_y12_chem_01",
        "mcqs": [
            "An oxidation reaction involves: A) Loss of electrons  B) Gain of electrons  C) Gain of protons  D) Loss of protons",
            "Which reagent is used to test for the presence of starch? A) Iodine solution  B) Benedict's solution  C) Biuret reagent  D) Fehling's solution",
        ],
        "short_questions": [
            "Explain the differences between galvanic and electrolytic cells.",
            "What is Faraday's First Law of Electrolysis? Calculate the mass of copper deposited when 2 A flows for 30 min (Cu molar mass = 64 g/mol).",
        ],
        "long_questions": [
            "Describe the chemistry of proteins. Explain primary, secondary, tertiary and quaternary structure. How does denaturation occur?",
        ],
    },

    {
        "country": "Australia", "category": "Final Term", "class_name": "Year 10", "subject": "Biology",
        "paper_id": "aus_final_y10_bio_01",
        "mcqs": [
            "Which process is responsible for genetic variation in offspring? A) Meiosis  B) Mitosis  C) Binary fission  D) Budding",
            "The building blocks of proteins are: A) Amino acids  B) Fatty acids  C) Nucleotides  D) Monosaccharides",
        ],
        "short_questions": [
            "Explain the differences between DNA replication and transcription.",
            "What are stem cells? Describe their potential in medical applications.",
        ],
        "long_questions": [
            "Describe how vaccines work. Explain herd immunity and why it is important for public health.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Australia — Quiz
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Australia", "category": "Quiz", "class_name": "Year 12", "subject": "Physics",
        "paper_id": "aus_quiz_y12_phy_01",
        "mcqs": [
            "The Planck constant has units: A) J·s  B) J/s  C) kg·m/s  D) W·m²",
            "In an ideal gas, pressure is proportional to: A) Temperature (at constant V)  B) Volume  C) Density  D) Molar mass",
            "Which phenomenon proves light has wave properties? A) Diffraction  B) Photoelectric effect  C) Pair production  D) Compton scattering",
            "The speed of electromagnetic waves in a vacuum is: A) 3×10⁸ m/s  B) 1.5×10⁸ m/s  C) 6×10⁸ m/s  D) 3×10⁶ m/s",
        ],
        "short_questions": [
            "State the Heisenberg Uncertainty Principle and explain its physical significance.",
        ],
        "long_questions": [],
    },

    {
        "country": "Australia", "category": "Quiz", "class_name": "Year 11", "subject": "Chemistry",
        "paper_id": "aus_quiz_y11_chem_01",
        "mcqs": [
            "An atom of carbon has 6 protons and 6 neutrons. Its mass number is: A) 12  B) 6  C) 18  D) 0",
            "Which of the following is a physical change? A) Dissolving sugar  B) Burning wood  C) Rusting iron  D) Cooking an egg",
            "Electronegativity generally increases: A) Across a period  B) Down a group  C) With atomic mass  D) With atomic radius",
            "What type of bond is formed between Na and Cl? A) Ionic  B) Covalent  C) Metallic  D) Hydrogen",
        ],
        "short_questions": [
            "Define isotopes. Give two isotopes of hydrogen and their applications.",
        ],
        "long_questions": [],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Canada — Board Exam
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Canada", "category": "Board Exam", "class_name": "Grade 12", "subject": "Physics",
        "paper_id": "can_board_g12_phy_01",
        "mcqs": [
            "The conservation of momentum applies to: A) All closed systems  B) Only elastic collisions  C) Only inelastic collisions  D) Only massive objects",
            "An electric field lines always point: A) Away from positive charges  B) Toward positive charges  C) In circular loops  D) Perpendicular to charge",
            "Kirchhoff's Current Law states: A) Sum of currents at a node = 0  B) Sum of voltages in a loop = 0  C) Current is constant in all branches  D) Voltage drops across resistors equally",
        ],
        "short_questions": [
            "Explain the Doppler effect. How is it applied in radar speed guns?",
            "Calculate the wavelength of a photon with energy 3.2×10⁻¹⁹ J (h = 6.63×10⁻³⁴ J·s, c = 3×10⁸ m/s).",
            "Describe what happens to the image formed by a concave mirror when an object is placed at focus.",
        ],
        "long_questions": [
            "Derive the equation for the magnetic force on a moving charge. Describe circular motion of a charged particle in a uniform magnetic field.",
            "Explain the wave-particle duality of electrons. Describe the evidence from the double-slit experiment.",
        ],
    },

    {
        "country": "Canada", "category": "Board Exam", "class_name": "Grade 11", "subject": "Chemistry",
        "paper_id": "can_board_g11_chem_01",
        "mcqs": [
            "VSEPR theory predicts the: A) Molecular geometry  B) Atomic mass  C) Nuclear charge  D) Bond energy",
            "The oxidation number of oxygen in H₂O is: A) -2  B) +2  C) 0  D) -1",
            "Which type of reaction produces a precipitate? A) Precipitation  B) Combustion  C) Synthesis  D) Decomposition",
        ],
        "short_questions": [
            "Draw the Lewis structure of CO₂ and determine its molecular geometry.",
            "Explain the difference between molarity and molality.",
            "What is stoichiometry? Calculate the mass of CO₂ produced when 12 g of C burns completely.",
        ],
        "long_questions": [
            "Describe intermolecular forces: London dispersion, dipole-dipole, and hydrogen bonding. How do they affect boiling point?",
            "Explain chemical kinetics: rate law, rate constant, and reaction orders. How is the rate constant determined experimentally?",
        ],
    },

    {
        "country": "Canada", "category": "Board Exam", "class_name": "Grade 10", "subject": "Biology",
        "paper_id": "can_board_g10_bio_01",
        "mcqs": [
            "The process of converting glucose to pyruvate is called: A) Glycolysis  B) Krebs cycle  C) Calvin cycle  D) Photosynthesis",
            "Cells in a hypertonic solution will: A) Shrink  B) Swell  C) Stay the same  D) Burst",
            "Which molecule is the energy currency of the cell? A) ATP  B) ADP  C) NADH  D) RNA",
        ],
        "short_questions": [
            "Describe the structure of a eukaryotic cell. Name three organelles and their functions.",
            "Explain active transport. How does it differ from passive diffusion?",
            "What is the role of enzymes in biochemical reactions? How does temperature affect enzyme activity?",
        ],
        "long_questions": [
            "Compare aerobic and anaerobic respiration. Write chemical equations for each and state the ATP yield.",
            "Describe the structure of DNA. Explain the process of DNA replication including the role of DNA polymerase.",
        ],
    },

    {
        "country": "Canada", "category": "Board Exam", "class_name": "Grade 12", "subject": "Mathematics",
        "paper_id": "can_board_g12_math_01",
        "mcqs": [
            "The value of lim_{x→0} sin x / x is: A) 1  B) 0  C) ∞  D) -1",
            "A function is continuous at x = a if: A) lim_{x→a} f(x) = f(a)  B) f(a) exists only  C) f'(a) exists  D) f(a) = 0",
            "The area under a curve from a to b is given by: A) ∫ₐᵇ f(x) dx  B) f'(b) - f'(a)  C) f(b) - f(a)  D) ∑f(x)",
        ],
        "short_questions": [
            "Use L'Hôpital's Rule to evaluate lim_{x→0} (sin x)/x.",
            "Find the equation of the tangent to y = x³ - 2x at x = 1.",
            "Evaluate ∫₀¹ (3x² + 2x) dx.",
        ],
        "long_questions": [
            "Explain probability distributions. Describe the binomial and normal distributions. Find P(X = 3) for B(5, 0.4).",
            "Describe vectors in 3D space. Define dot product and cross product. Find the volume of the parallelepiped formed by a = (1,2,3), b = (4,5,6), c = (7,8,0).",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Canada — Mid Term
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Canada", "category": "Mid Term", "class_name": "Grade 12", "subject": "Computer Science",
        "paper_id": "can_mid_g12_cs_01",
        "mcqs": [
            "Which data structure follows FIFO? A) Queue  B) Stack  C) Tree  D) Heap",
            "The time complexity of binary search is: A) O(log n)  B) O(n)  C) O(n²)  D) O(1)",
        ],
        "short_questions": [
            "Explain the concept of object-oriented programming. Define encapsulation, inheritance, and polymorphism.",
            "Write pseudocode for insertion sort and state its time complexity.",
        ],
        "long_questions": [
            "Describe graph data structures. Explain DFS and BFS traversal with examples. What are their time complexities?",
        ],
    },

    {
        "country": "Canada", "category": "Mid Term", "class_name": "Grade 11", "subject": "Physics",
        "paper_id": "can_mid_g11_phy_01",
        "mcqs": [
            "The coefficient of kinetic friction is always: A) Less than coefficient of static friction  B) Greater  C) Equal  D) Unrelated",
            "Which law of thermodynamics states energy cannot be created or destroyed? A) First  B) Second  C) Third  D) Zeroth",
        ],
        "short_questions": [
            "Explain the work-energy theorem. Give a practical example.",
            "A 2 kg block slides down a frictionless incline at 30°. Find the acceleration.",
        ],
        "long_questions": [
            "Describe circular motion. Derive the centripetal acceleration formula. Apply it to a car turning on a banked road.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Canada — Final Term
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Canada", "category": "Final Term", "class_name": "Grade 11", "subject": "Biology",
        "paper_id": "can_final_g11_bio_01",
        "mcqs": [
            "Which gas is released during photosynthesis? A) Oxygen  B) Carbon dioxide  C) Nitrogen  D) Hydrogen",
            "Meiosis produces: A) 4 haploid cells  B) 2 diploid cells  C) 2 haploid cells  D) 4 diploid cells",
        ],
        "short_questions": [
            "Explain the greenhouse effect. How does CO₂ contribute to global warming?",
            "What is a keystone species? Give one example and explain its role.",
        ],
        "long_questions": [
            "Describe the nitrogen cycle. Explain the role of nitrogen-fixing bacteria, nitrification, denitrification, and decomposition.",
        ],
    },

    {
        "country": "Canada", "category": "Final Term", "class_name": "Grade 10", "subject": "Chemistry",
        "paper_id": "can_final_g10_chem_01",
        "mcqs": [
            "Which of the following is a sign of a chemical reaction? A) Colour change  B) No change in mass  C) Same properties  D) Reversible mixing",
            "The molar mass of CO₂ is: A) 44 g/mol  B) 28 g/mol  C) 12 g/mol  D) 32 g/mol",
        ],
        "short_questions": [
            "Balance the equation: Fe + HCl → FeCl₂ + H₂. Calculate the mass of H₂ produced from 5.6 g of Fe.",
            "Define alloys. Give two examples and their uses.",
        ],
        "long_questions": [
            "Describe the properties and uses of acids and bases. Explain neutralization. Describe the pH scale and its significance.",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Canada — Quiz
    # ══════════════════════════════════════════════════════════════════════════

    {
        "country": "Canada", "category": "Quiz", "class_name": "Grade 12", "subject": "Mathematics",
        "paper_id": "can_quiz_g12_math_01",
        "mcqs": [
            "The inverse of the function f(x) = 2x + 3 is: A) f⁻¹(x) = (x-3)/2  B) f⁻¹(x) = 2x - 3  C) f⁻¹(x) = (x+3)/2  D) f⁻¹(x) = x/2",
            "The sum of the infinite geometric series 1 + 1/3 + 1/9 + ... is: A) 3/2  B) 2  C) 1  D) 3",
            "If f(x) = x² and g(x) = 2x, then f(g(x)) = : A) 4x²  B) 2x²  C) x⁴  D) 4x",
            "The discriminant of 3x² - 6x + 3 = 0 is: A) 0  B) 36  C) -36  D) 12",
        ],
        "short_questions": [
            "Find all values of x such that 2ˣ = 64.",
        ],
        "long_questions": [],
    },

    {
        "country": "Canada", "category": "Quiz", "class_name": "Grade 11", "subject": "Biology",
        "paper_id": "can_quiz_g11_bio_01",
        "mcqs": [
            "Which organelle contains the genetic material of a cell? A) Nucleus  B) Mitochondria  C) Ribosome  D) Cell membrane",
            "The scientific name of humans is: A) Homo sapiens  B) Homo erectus  C) Australopithecus  D) Homo habilis",
            "Active transport requires: A) ATP  B) Oxygen  C) Sunlight  D) Water",
            "DNA replication is: A) Semi-conservative  B) Conservative  C) Dispersive  D) Random",
        ],
        "short_questions": [
            "Explain the difference between mitosis and meiosis. When does each occur in the human body?",
        ],
        "long_questions": [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# Seeder function
# ═══════════════════════════════════════════════════════════════════════════════

def _make_id(prefix: str, index: int, text: str) -> str:
    return hashlib.md5(f"{prefix}_{index}_{text[:40]}".encode()).hexdigest()


def seed_unverified_store() -> None:
    """
    Seed the unverified ChromaDB collection with international exam papers.
    Countries: UK, USA, India, Australia, Canada.
    Categories: Board Exam, Mid Term, Final Term, Quiz.
    Papers are stored DIRECTLY in the vector DB — no file system storage.
    Idempotent — skips if collection already populated.
    """
    from services.vector_store import unverified_col, add_to_unverified, save_unverified_paper_meta

    existing_count = unverified_col.count()
    if existing_count > 0:
        print(f"[Seed] Unverified store already has {existing_count} documents — skipping.")
        return

    print("[Seed] Building unverified store with international papers …")
    documents = []
    metadatas = []

    # Track which combinations we've catalogued (for JSON meta)
    catalogued = set()

    for paper in UNVERIFIED_SEED_PAPERS:
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
            "paper_type": "unverified",
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

        # Catalogue metadata (once per unique combination)
        combo_key = (country, category, class_name, subject)
        if combo_key not in catalogued:
            catalogued.add(combo_key)
            save_unverified_paper_meta(
                country=country,
                class_name=class_name,
                subject=subject,
                score=75.0,   # seed papers have a default uniqueness score
                category=category,
                filename=f"{paper_id}.pdf",
            )

    if not documents:
        print("[Seed] No documents to seed into unverified store.")
        return

    ids = [_make_id("unverified", i, d) for i, d in enumerate(documents)]
    print(f"[Seed] Upserting {len(documents)} questions into unverified store …")
    add_to_unverified(documents, metadatas, ids)
    print(f"[Seed] Done. Unverified store now has {unverified_col.count()} documents.")


if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    seed_unverified_store()
