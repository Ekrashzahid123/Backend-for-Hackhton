"""
Seed the Unverified ChromaDB collection with seed exam papers.

Coverage: same classes as verified — 9, 10, 11, 12, O Level, A Level
Boards   : Punjab Boards, Federal Board, Cambridge
Subjects : Mathematics, Physics, Chemistry, Biology, Computer Science, English

Papers are stored DIRECTLY in the Unverified Vector DB
(no file system storage required).

Run automatically on startup or manually:
    python -m services.seed_unverified_store
"""

import os
import hashlib
import datetime
from typing import List, Dict

_TIMESTAMP = datetime.datetime.utcnow().isoformat()


# ═══════════════════════════════════════════════════════════════════════════════
# Seed papers — separate from verified content to maintain uniqueness
# ═══════════════════════════════════════════════════════════════════════════════

UNVERIFIED_SEED_PAPERS: List[Dict] = [

    # ── Pakistan > Punjab Boards > Class 9 ───────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Physics", "paper_id": "upk_punjab_c9_phy_01",
        "mcqs": [
            "Torque is defined as the product of force and: A) Distance  B) Perpendicular distance  C) Velocity  D) Acceleration",
            "A body thrown horizontally from a height follows a: A) Parabolic path  B) Circular path  C) Straight path  D) Elliptical path",
            "The weight of an object on the Moon is approximately: A) 1/6 of its weight on Earth  B) Same as on Earth  C) Double of its weight on Earth  D) Zero",
        ],
        "short_questions": [
            "Define torque and its unit. How does it differ from work?",
            "A stone is thrown horizontally at 20 m/s from a cliff 45 m high. Calculate the time to reach the ground.",
            "Explain how the weight of a body changes with altitude.",
        ],
        "long_questions": [
            "Derive the formula for maximum height and time of flight for a projectile launched at angle θ. Calculate the range for θ = 45°.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Chemistry", "paper_id": "upk_punjab_c9_chem_01",
        "mcqs": [
            "The number of moles in 22 g of CO₂ is: A) 0.5  B) 1.0  C) 1.5  D) 2.0",
            "Which of the following is a physical change? A) Melting of ice  B) Rusting of iron  C) Burning wood  D) Souring of milk",
            "A solution with pH = 3 is: A) Strongly acidic  B) Weakly acidic  C) Neutral  D) Basic",
        ],
        "short_questions": [
            "Calculate the number of molecules in 18 g of water.",
            "Differentiate between a solution and a suspension with examples.",
            "What is the effect of catalyst on activation energy?",
        ],
        "long_questions": [
            "Explain the factors affecting rate of reaction: concentration, temperature, particle size, and catalysts. Use collision theory to explain each.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Biology", "paper_id": "upk_punjab_c9_bio_01",
        "mcqs": [
            "Which organelle is responsible for the synthesis of lipids? A) Smooth ER  B) Rough ER  C) Golgi apparatus  D) Nucleus",
            "The process by which white blood cells engulf bacteria is called: A) Phagocytosis  B) Pinocytosis  C) Exocytosis  D) Endocytosis",
            "Root pressure is caused by: A) Active transport of ions into roots  B) Transpiration  C) Photosynthesis  D) Respiration",
        ],
        "short_questions": [
            "Differentiate between endocytosis and exocytosis.",
            "What is turgor pressure? Explain its importance in plant support.",
            "Describe the role of the Golgi apparatus.",
        ],
        "long_questions": [
            "Explain the transport of water and minerals in plants. Describe the role of xylem and phloem. Explain the transpiration pull mechanism.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Mathematics", "paper_id": "upk_punjab_c9_math_01",
        "mcqs": [
            "If A ∩ B = ∅, the sets A and B are called: A) Disjoint  B) Equal  C) Equivalent  D) Subsets",
            "The midpoint formula between (x₁,y₁) and (x₂,y₂) is: A) ((x₁+x₂)/2, (y₁+y₂)/2)  B) (x₁-x₂, y₁-y₂)  C) (x₁x₂, y₁y₂)  D) (x₁/x₂, y₁/y₂)",
            "If an angle in a semicircle is inscribed, it measures: A) 90°  B) 45°  C) 180°  D) 60°",
        ],
        "short_questions": [
            "Find the midpoint and length of the segment joining A(-2, 3) and B(4, -1).",
            "Solve: √(2x-1) = 3.",
            "Factorize: a⁴ - b⁴.",
        ],
        "long_questions": [
            "Prove that the angle subtended by an arc at the centre is double the angle at the circumference.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 9", "subject": "Computer Science", "paper_id": "upk_punjab_c9_cs_01",
        "mcqs": [
            "Which of the following converts high-level language to machine code line by line? A) Interpreter  B) Compiler  C) Assembler  D) Linker",
            "The hexadecimal equivalent of decimal 255 is: A) FF  B) EE  C) AB  D) F0",
        ],
        "short_questions": [
            "Write an algorithm to find whether a number is prime.",
            "Explain the difference between SRAM and DRAM.",
        ],
        "long_questions": [
            "Describe input and output devices in detail. Explain the working of a laser printer and a scanner.",
        ],
    },

    # ── Pakistan > Punjab Boards > Class 10 ──────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 10", "subject": "Physics", "paper_id": "upk_punjab_c10_phy_01",
        "mcqs": [
            "The force between two parallel conductors carrying current in the same direction is: A) Attractive  B) Repulsive  C) Zero  D) Perpendicular",
            "The frequency of AC mains supply in Pakistan is: A) 50 Hz  B) 60 Hz  C) 100 Hz  D) 25 Hz",
            "A positive lens has: A) Converging power  B) Diverging power  C) Zero power  D) Infinite power",
        ],
        "short_questions": [
            "What is magnetic flux? Write its unit and formula.",
            "Explain Lenz's Law with an example.",
            "Define refractive index. How does it relate to the speed of light?",
        ],
        "long_questions": [
            "Describe the construction and working of an AC generator. Explain how EMF varies with time and draw the output waveform.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 10", "subject": "Chemistry", "paper_id": "upk_punjab_c10_chem_01",
        "mcqs": [
            "What is the IUPAC name of CH₃CH₂OH? A) Ethanol  B) Methanol  C) Propanol  D) Butanol",
            "The reaction between an acid and a base is called: A) Neutralization  B) Precipitation  C) Combustion  D) Decomposition",
        ],
        "short_questions": [
            "What is the difference between a strong acid and a weak acid? Give examples.",
            "Explain saponification and write its equation.",
        ],
        "long_questions": [
            "Describe the chemistry of soaps and detergents. How do they remove grease? Compare their effectiveness in hard water.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 10", "subject": "Biology", "paper_id": "upk_punjab_c10_bio_01",
        "mcqs": [
            "The largest gland in the human body is: A) Liver  B) Pancreas  C) Thyroid  D) Adrenal",
            "Growth hormone is secreted by the: A) Pituitary gland  B) Thyroid gland  C) Adrenal cortex  D) Pancreas",
        ],
        "short_questions": [
            "Explain the role of insulin and glucagon in regulating blood glucose.",
            "What is a reflex action? Describe the reflex arc.",
        ],
        "long_questions": [
            "Describe the endocrine system. Explain the hormones secreted by the pituitary, thyroid, adrenal, and reproductive glands.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 10", "subject": "Mathematics", "paper_id": "upk_punjab_c10_math_01",
        "mcqs": [
            "The roots of x² - 4x + 4 = 0 are: A) Equal and real  B) Unequal and real  C) Imaginary  D) Negative",
            "In a right triangle, if one angle is 30°, the other acute angle is: A) 60°  B) 45°  C) 90°  D) 30°",
        ],
        "short_questions": [
            "Find the sum of first 20 terms of the AP: 1, 3, 5, 7, ...",
            "Prove: tan²θ + 1 = sec²θ.",
        ],
        "long_questions": [
            "Prove that the tangent at any point of a circle is perpendicular to the radius through that point.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 10", "subject": "Computer Science", "paper_id": "upk_punjab_c10_cs_01",
        "mcqs": [
            "Which of the following is an example of cloud storage? A) Google Drive  B) USB drive  C) RAM  D) Hard disk",
            "Which tag creates a hyperlink in HTML? A) <a>  B) <link>  C) <href>  D) <url>",
        ],
        "short_questions": [
            "Write a Python program to check if a given year is a leap year.",
            "What is cybersecurity? List three common cyber threats.",
        ],
        "long_questions": [
            "Explain the concept of the Internet of Things (IoT). Describe its applications in healthcare, smart homes, and agriculture.",
        ],
    },

    # ── Pakistan > Punjab Boards > Class 11 ──────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 11", "subject": "Physics", "paper_id": "upk_punjab_c11_phy_01",
        "mcqs": [
            "The drag force on a body moving through a fluid is proportional to: A) v²  B) v  C) √v  D) 1/v",
            "The moment of inertia of a solid sphere about its diameter is: A) 2/5 mr²  B) 2/3 mr²  C) mr²  D) 1/2 mr²",
        ],
        "short_questions": [
            "Distinguish between elastic and inelastic collisions. In which is kinetic energy conserved?",
            "Explain the concept of escape velocity. Calculate it for the Earth (g = 9.8 m/s², R = 6400 km).",
        ],
        "long_questions": [
            "Explain Bernoulli's equation and its derivation. Describe its applications: flight lift, carburetor, and Venturi meter.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 11", "subject": "Chemistry", "paper_id": "upk_punjab_c11_chem_01",
        "mcqs": [
            "According to VSEPR, the shape of water (H₂O) is: A) Bent/V-shaped  B) Linear  C) Tetrahedral  D) Trigonal planar",
            "The standard state of temperature and pressure (STP) is: A) 0°C and 1 atm  B) 25°C and 1 atm  C) 0°C and 100 kPa  D) 100°C and 1 atm",
        ],
        "short_questions": [
            "Explain Hess's Law. How is it used to calculate enthalpy of formation?",
            "Define equilibrium constant K. How does it relate to Gibbs free energy?",
        ],
        "long_questions": [
            "Explain chemical thermodynamics. Define enthalpy, entropy, and Gibbs free energy. Derive the relationship ΔG = ΔH - TΔS.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 11", "subject": "Biology", "paper_id": "upk_punjab_c11_bio_01",
        "mcqs": [
            "Which of the following is a totipotent cell? A) Zygote  B) Neuron  C) Muscle cell  D) Red blood cell",
            "In C4 plants, CO₂ is first fixed into: A) Oxaloacetate  B) 3-PGA  C) G3P  D) RuBP",
        ],
        "short_questions": [
            "Differentiate between C3 and C4 photosynthesis. Give examples of each type.",
            "What is the significance of Krebs cycle in cellular respiration?",
        ],
        "long_questions": [
            "Describe the light reactions of photosynthesis. Explain the Z-scheme and the role of photosystems I and II.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 11", "subject": "Mathematics", "paper_id": "upk_punjab_c11_math_01",
        "mcqs": [
            "The general term of a GP is: A) arⁿ⁻¹  B) a + (n-1)d  C) n(a+l)/2  D) a/(1-r)",
            "The value of cos(π/3) is: A) 1/2  B) √3/2  C) 1/√2  D) 0",
        ],
        "short_questions": [
            "Find the nth term and sum of the GP: 2, 6, 18, 54, ...",
            "Using De Moivre's theorem, find (1 + i)⁸.",
        ],
        "long_questions": [
            "Explain arithmetic and geometric progressions. Derive the sum formulas. Find the sum of 12 terms of AP: 5, 9, 13, ... and GP: 3, 6, 12, ...",
        ],
    },

    # ── Pakistan > Punjab Boards > Class 12 ──────────────────────────────────
    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 12", "subject": "Physics", "paper_id": "upk_punjab_c12_phy_01",
        "mcqs": [
            "In a full-wave rectifier, the ripple frequency is: A) Twice the supply frequency  B) Same as supply frequency  C) Half the supply frequency  D) Four times the supply frequency",
            "Which of these is an intrinsic semiconductor? A) Pure silicon  B) N-type silicon  C) P-type silicon  D) Doped germanium",
        ],
        "short_questions": [
            "What is forward bias in a p-n junction? How does it affect the depletion region?",
            "Explain the working of a CRO (Cathode Ray Oscilloscope).",
        ],
        "long_questions": [
            "Describe fission chain reaction. Explain how it is controlled in a nuclear reactor. Discuss safety measures and radioactive waste management.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 12", "subject": "Chemistry", "paper_id": "upk_punjab_c12_chem_01",
        "mcqs": [
            "In a Wittig reaction, a carbonyl compound reacts with: A) Phosphorus ylide  B) Grignard reagent  C) Organolithium  D) Sodium borohydride",
            "Nylon-6 is formed from: A) Caprolactam  B) Ethylene  C) Propylene  D) Styrene",
        ],
        "short_questions": [
            "What is addition polymerization? Give an example with reaction.",
            "Describe the Cannizzaro reaction. Under what conditions does it occur?",
        ],
        "long_questions": [
            "Describe the biological importance of carbohydrates, lipids, and proteins. Explain how each is digested and used by the body.",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 12", "subject": "Biology", "paper_id": "upk_punjab_c12_bio_01",
        "mcqs": [
            "Which hormone triggers ovulation? A) LH  B) FSH  C) Estrogen  D) Progesterone",
            "Cloning uses the technique of: A) Somatic cell nuclear transfer  B) Meiosis  C) Mitosis  D) Conjugation",
        ],
        "short_questions": [
            "Describe in vitro fertilization (IVF). What are its ethical considerations?",
            "What is gene therapy? Describe its applications in treating genetic disorders.",
        ],
        "long_questions": [
            "Describe the human immune response to an infection. Explain the roles of T-lymphocytes and B-lymphocytes. How does vaccination work?",
        ],
    },

    {
        "country": "Pakistan", "category": "Punjab Boards", "class_name": "Class 12", "subject": "Mathematics", "paper_id": "upk_punjab_c12_math_01",
        "mcqs": [
            "The order of the differential equation d²y/dx² + dy/dx + y = 0 is: A) 2  B) 1  C) 3  D) 0",
            "If y = x sin x, then dy/dx = : A) sin x + x cos x  B) x cos x  C) sin x - x cos x  D) cos x",
        ],
        "short_questions": [
            "Solve the ODE: dy/dx = 2x + 1, given y = 3 when x = 0.",
            "Evaluate: ∫sin²x dx using the double angle formula.",
        ],
        "long_questions": [
            "Explain the concept of differential equations. Solve y'' - 4y' + 4y = 0 using the characteristic equation method.",
        ],
    },

    # ── Pakistan > Cambridge > O Level ───────────────────────────────────────
    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "O Level", "subject": "Physics", "paper_id": "upk_cam_olevel_phy_01",
        "mcqs": [
            "The efficiency of a machine is always: A) Less than 100%  B) Equal to 100%  C) Greater than 100%  D) Zero",
            "Sound cannot travel through: A) Vacuum  B) Air  C) Water  D) Solid",
        ],
        "short_questions": [
            "Define efficiency of a machine. Why is it always less than 100%?",
            "Explain the difference between transverse and longitudinal waves with diagrams.",
        ],
        "long_questions": [
            "Explain how a thermocouple works as a thermometer. Compare it with a clinical thermometer and an infrared thermometer in terms of range and sensitivity.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "O Level", "subject": "Chemistry", "paper_id": "upk_cam_olevel_chem_01",
        "mcqs": [
            "The rate of reaction increases with temperature because: A) Particles collide more frequently with more energy  B) Activation energy decreases  C) Products decompose  D) Volume decreases",
            "Calcium carbonate decomposes on heating to give: A) CaO + CO₂  B) Ca + CO₂  C) CaCO + O₂  D) Ca(OH)₂",
        ],
        "short_questions": [
            "Draw and label the energy profile diagram for an exothermic reaction. Indicate activation energy and ΔH.",
            "What are the uses of limestone and calcium oxide in industry?",
        ],
        "long_questions": [
            "Explain the nitrogen cycle. Describe how nitrogen is fixed, nitrified, and denitrified. What is the role of bacteria at each stage?",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "O Level", "subject": "Biology", "paper_id": "upk_cam_olevel_bio_01",
        "mcqs": [
            "The process by which plants lose water vapor from leaves is: A) Transpiration  B) Perspiration  C) Respiration  D) Evaporation",
            "Double fertilization occurs in: A) Angiosperms  B) Gymnosperms  C) Ferns  D) Mosses",
        ],
        "short_questions": [
            "Explain the factors affecting the rate of transpiration.",
            "Describe the mechanism of inspiration and expiration in humans.",
        ],
        "long_questions": [
            "Explain the carbon cycle. Describe how carbon dioxide is added to and removed from the atmosphere. What impact does human activity have on this cycle?",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "O Level", "subject": "Mathematics", "paper_id": "upk_cam_olevel_math_01",
        "mcqs": [
            "Vectors are equal when they have the same: A) Magnitude and direction  B) Only magnitude  C) Only direction  D) Starting point",
            "The bearing of due west is: A) 270°  B) 180°  C) 090°  D) 000°",
        ],
        "short_questions": [
            "Vector a = (3, -4). Find |a| and the unit vector in the direction of a.",
            "A ship sails on bearing 040° for 20 km. Find how far north and east it has travelled.",
        ],
        "long_questions": [
            "Construct a cumulative frequency diagram for the following data and use it to find the median, lower quartile, and upper quartile: [marks data for 50 students].",
        ],
    },

    # ── Pakistan > Cambridge > A Level ───────────────────────────────────────
    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "A Level", "subject": "Physics", "paper_id": "upk_cam_alevel_phy_01",
        "mcqs": [
            "The energy stored in an inductor is: A) ½LI²  B) LI²  C) ½LI  D) L²I",
            "Which quantum number determines the spin of an electron? A) Spin quantum number  B) Principal  C) Azimuthal  D) Magnetic",
        ],
        "short_questions": [
            "Explain the quantum tunneling phenomenon. Where is it applied?",
            "Define magnetic flux density. Derive the force on a current-carrying conductor in a magnetic field.",
        ],
        "long_questions": [
            "Explain special relativity: time dilation and length contraction. Derive the Lorentz transformation equations.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "A Level", "subject": "Chemistry", "paper_id": "upk_cam_alevel_chem_01",
        "mcqs": [
            "Grignard reagent is: A) RMgX  B) RLi  C) R₂Zn  D) RAlX₂",
            "The Fischer esterification requires: A) Acid catalyst  B) Base catalyst  C) No catalyst  D) Enzyme",
        ],
        "short_questions": [
            "Explain the SN1 and SN2 mechanisms. What factors favour each?",
            "Describe the Aldol condensation reaction. Give an example.",
        ],
        "long_questions": [
            "Discuss retrosynthetic analysis. Plan a synthesis of ibuprofen from benzene using organic reactions.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "A Level", "subject": "Biology", "paper_id": "upk_cam_alevel_bio_01",
        "mcqs": [
            "CRISPR-Cas9 is used for: A) Gene editing  B) PCR  C) Gel electrophoresis  D) Cloning",
            "Which hormone is responsible for the 'fight or flight' response? A) Adrenaline  B) Insulin  C) Thyroxine  D) Cortisol",
        ],
        "short_questions": [
            "Explain the CRISPR-Cas9 system. How is it used to edit genes?",
            "Describe the mechanism of action of hormones using a second messenger model.",
        ],
        "long_questions": [
            "Explain the structure and function of the nephron in detail. Include the roles of ultrafiltration, selective reabsorption, and secretion in producing urine.",
        ],
    },

    {
        "country": "Pakistan", "category": "Cambridge", "class_name": "A Level", "subject": "Mathematics", "paper_id": "upk_cam_alevel_math_01",
        "mcqs": [
            "The modulus of (1 + i) is: A) √2  B) 2  C) 1  D) i",
            "A stationary point where f''(x) = 0 is called: A) Point of inflection  B) Maximum  C) Minimum  D) Saddle point",
        ],
        "short_questions": [
            "Differentiate: f(x) = x³ ln(2x) using the product rule.",
            "Solve the differential equation: dy/dx = y/x, given y = 2 when x = 1.",
        ],
        "long_questions": [
            "Explain hypothesis testing using the normal distribution. Describe Type I and Type II errors. Test whether the mean IQ of 50 students (mean=105, σ=15) differs from 100 at 5% significance.",
        ],
    },

    # ── Pakistan > Federal Board > Class 9 ───────────────────────────────────
    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 9", "subject": "Physics", "paper_id": "upk_fbise_c9_phy_01",
        "mcqs": [
            "The property of matter to resist change in its state of motion is: A) Inertia  B) Momentum  C) Force  D) Energy",
            "The slope of a displacement-time graph gives: A) Velocity  B) Acceleration  C) Distance  D) Force",
        ],
        "short_questions": [
            "Define momentum. How is it related to Newton's Second Law?",
            "A car accelerates from 10 m/s to 30 m/s in 5 s. Find acceleration and distance covered.",
        ],
        "long_questions": [
            "Explain the concept of circular motion. Derive the expression for centripetal acceleration and force.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 10", "subject": "Biology", "paper_id": "upk_fbise_c10_bio_01",
        "mcqs": [
            "The vaccine for smallpox was developed by: A) Edward Jenner  B) Louis Pasteur  C) Alexander Fleming  D) Robert Koch",
            "The number of chambers in the human heart is: A) 4  B) 2  C) 3  D) 6",
        ],
        "short_questions": [
            "What is blood pressure? What are normal systolic and diastolic values?",
            "Explain the role of platelets in blood clotting.",
        ],
        "long_questions": [
            "Describe the structure of the human heart. Explain the cardiac cycle (systole and diastole) and the role of the SA and AV nodes.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 11", "subject": "Chemistry", "paper_id": "upk_fbise_c11_chem_01",
        "mcqs": [
            "The van der Waals forces are strongest in: A) Iodine  B) Methane  C) Helium  D) Neon",
            "Boiling point of water is higher than H₂S because of: A) Hydrogen bonding  B) Ionic bonding  C) Van der Waals forces  D) Covalent bonds",
        ],
        "short_questions": [
            "Compare the physical properties of ionic and covalent compounds.",
            "Explain the Born-Haber cycle for NaCl. Identify each energy term.",
        ],
        "long_questions": [
            "Describe different types of solids: ionic, molecular, covalent, and metallic. Compare their properties and give two examples of each.",
        ],
    },

    {
        "country": "Pakistan", "category": "Federal Board", "class_name": "Class 12", "subject": "Mathematics", "paper_id": "upk_fbise_c12_math_01",
        "mcqs": [
            "The equation of a circle with centre (h,k) and radius r is: A) (x-h)² + (y-k)² = r²  B) x² + y² = r²  C) (x+h)² + (y+k)² = r²  D) x² + y² = 2r",
            "The angle between two lines with slopes m₁ and m₂ is: A) tan⁻¹|(m₁-m₂)/(1+m₁m₂)|  B) tan⁻¹(m₁m₂)  C) sin⁻¹(m₁-m₂)  D) cos⁻¹(m₁+m₂)",
        ],
        "short_questions": [
            "Find the equation of the circle passing through (1,0), (0,1), and (0,0).",
            "Find the angle between the lines 2x - 3y + 1 = 0 and x + y - 2 = 0.",
        ],
        "long_questions": [
            "Explain conic sections analytically. Derive the standard equations of parabola, ellipse, and hyperbola. Identify the type of conic for: x²/9 + y²/4 = 1.",
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# Seeder function
# ═══════════════════════════════════════════════════════════════════════════════

def _make_id(prefix: str, index: int, text: str) -> str:
    return hashlib.md5(f"{prefix}_{index}_{text[:40]}".encode()).hexdigest()


def seed_unverified_store() -> None:
    """
    Seed the unverified ChromaDB collection with community-style exam papers.
    Papers are stored DIRECTLY in the vector DB — no file system storage.
    Idempotent — skips if collection already populated.
    """
    from services.vector_store import unverified_col, add_to_unverified, save_unverified_paper_meta

    existing_count = unverified_col.count()
    if existing_count > 0:
        print(f"[Seed] Unverified store already has {existing_count} documents — skipping.")
        return

    print("[Seed] Building unverified store …")
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
