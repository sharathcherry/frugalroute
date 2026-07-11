window.DATA = {
  "engine": "langgraph",
  "records": [
    {
      "id": "0",
      "task": "Classify sentiment: 'I love this, works great!'",
      "answer": "positive",
      "category": "classification",
      "source": "local",
      "route_p": 0.26,
      "confidence": 0.95,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "1",
      "task": "Classify sentiment: 'This is the worst purchase ever.'",
      "answer": "negative",
      "category": "classification",
      "source": "local",
      "route_p": 0.27,
      "confidence": 0.95,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "2",
      "task": "Classify sentiment: 'The package arrived on Tuesday.'",
      "answer": "neutral",
      "category": "classification",
      "source": "local",
      "route_p": 0.27,
      "confidence": 0.95,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "3",
      "task": "Is this spam? 'You won a free prize, click now!'",
      "answer": "spam",
      "category": "qa",
      "source": "local",
      "route_p": 0.27,
      "confidence": 0.95,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "4",
      "task": "Label the topic: 'The GDP grew 3% last quarter.'",
      "answer": "economics",
      "category": "classification",
      "source": "local",
      "route_p": 0.27,
      "confidence": 0.95,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "5",
      "task": "Classify sentiment given sarcasm: 'Oh great, another delay. Wonderful.'",
      "answer": "negative",
      "category": "classification",
      "source": "local",
      "route_p": 0.28,
      "confidence": 0.95,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "6",
      "task": "Extract all email addresses from: contact a@x.com or b@y.org",
      "answer": "a@x.com,b@y.org",
      "category": "extraction",
      "source": "local",
      "route_p": 0.27,
      "confidence": 1.0,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "7",
      "task": "Extract the phone number from: call me at 555-1234 tomorrow",
      "answer": "555-1234",
      "category": "extraction",
      "source": "local",
      "route_p": 0.27,
      "confidence": 0.95,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "8",
      "task": "Extract the date from: the meeting is on 2026-07-06 at noon",
      "answer": "2026-07-06",
      "category": "extraction",
      "source": "local",
      "route_p": 0.27,
      "confidence": 1.0,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "9",
      "task": "Extract the total price from: 2 items at $5 each plus $3 shipping",
      "answer": "13",
      "category": "extraction",
      "source": "local",
      "route_p": 0.28,
      "confidence": 0.95,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "10",
      "task": "Extract all company names from: Apple and Microsoft partnered with AMD",
      "answer": "Apple,Microsoft,AMD",
      "category": "extraction",
      "source": "local",
      "route_p": 0.28,
      "confidence": 1.0,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "11",
      "task": "Extract the implied deadline from: submit before the second Friday of July 2026",
      "answer": "July 14, 2026",
      "category": "extraction",
      "source": "local",
      "route_p": 0.29,
      "confidence": 0.75,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "12",
      "task": "Summarize in 5 words: The quarterly report showed revenue growth of 12% driven by cloud.",
      "answer": "Revenue grew 12%, driven by cloud.",
      "category": "summarization",
      "source": "local",
      "route_p": 0.3,
      "confidence": 0.95,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "13",
      "task": "Summarize: The cat sat on the mat and then went to sleep.",
      "answer": "The cat sat on the mat and fell asleep.",
      "category": "summarization",
      "source": "local",
      "route_p": 0.27,
      "confidence": 0.95,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "14",
      "task": "Summarize the key risk: Latency rose 40% after the deploy, errors doubled, users churned.",
      "answer": "Increased latency, more errors, user churn post-deploy.",
      "category": "summarization",
      "source": "local",
      "route_p": 0.3,
      "confidence": 0.65,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "15",
      "task": "Summarize a dense legal clause about indemnification and liability caps.",
      "answer": "The clause limits the party's liability to specific damages and requires one party to compensate the other for certain losses, setting a maximum cap on liability.",
      "category": "summarization",
      "source": "local",
      "route_p": 0.28,
      "confidence": 0.75,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "16",
      "task": "What is the capital of France?",
      "answer": "Paris",
      "category": "qa",
      "source": "local",
      "route_p": 0.25,
      "confidence": 1.0,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "17",
      "task": "What is the chemical symbol for gold?",
      "answer": "Au",
      "category": "qa",
      "source": "local",
      "route_p": 0.26,
      "confidence": 1.0,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "18",
      "task": "How many continents are there?",
      "answer": "There are **seven** continents on Earth:\n\n1. **Asia**  \n2. **Africa**  \n3. **North America**  \n4. **South America**  \n5. **Antarctica**  \n6. **Europe**  \n7. **Australia** (sometimes referred to as **Oceania** when including the Pacific islands)\n\n*Note:* Some educational systems teach a five\u2011continent model (combining Europe & Asia into \u201cEurasia,\u201d and North & South America into \u201cAmerica\u201d), but the most widely used classification today lists seven distinct continents.",
      "category": "math",
      "source": "remote",
      "route_p": 0.87,
      "confidence": null,
      "remote_tokens": 279,
      "tokens_saved": 1
    },
    {
      "id": "19",
      "task": "Who wrote Romeo and Juliet?",
      "answer": "William Shakespeare",
      "category": "qa",
      "source": "local",
      "route_p": 0.25,
      "confidence": 1.0,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "20",
      "task": "What year did the Berlin Wall fall?",
      "answer": "1989",
      "category": "qa",
      "source": "local",
      "route_p": 0.26,
      "confidence": 1.0,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "21",
      "task": "What is the boiling point of water at sea level in Celsius?",
      "answer": "100",
      "category": "qa",
      "source": "local",
      "route_p": 0.27,
      "confidence": 1.0,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "22",
      "task": "Why does increasing temperature speed up a chemical reaction? Explain step by step.",
      "answer": "**How a Higher Temperature Makes a Reaction Faster \u2013 A Step\u2011by\u2011Step Explanation**\n\nBelow is a logical chain that connects the macroscopic observation \u201cthe reaction goes faster when it\u2019s hotter\u201d to the microscopic events that actually happen in a reacting mixture.\n\n---\n\n## 1. Reactants Must Collide to React  \n\n1. **Molecules are in constant motion** \u2013 they translate, rotate, and vibrate.  \n2. **A chemical reaction can only occur when two (or more) reactant molecules come into contact** (a *collision*).  \n3. Not every collision leads to product formation; the molecules must have the right **orientation** and **enough energy** to overcome the barrier that separates reactants from products.\n\n---\n\n## 2. The Energy Barrier \u2013 Activation Energy (E\u2090)  \n\n1. **Potential\u2011energy surface** \u2013 Imagine a landscape where the reactants sit in a valley, the products in another valley, and a hill (the *transition state*) separates them.  \n2. **Activation energy (E\u2090)** is the height of that hill.  \n3. **Only collisions that supply at least E\u2090 can push the system over the hill** and allow the reaction to proceed.\n\n---\n\n## 3. Temperature Controls the Distribution of Molecular Energies  \n\n1. **Maxwell\u2011Boltzmann distribution** describes how kinetic energies are spread among molecules at a given temperature (T).  \n2. As T rises, the distribution **shifts to higher energies** and **flattens**, meaning:  \n\n   - **More molecules have high kinetic energy** (the \u201ctail\u201d of the distribution gets larger).  \n   - **The average kinetic energy** (\u00bd\u202fmv\u00b2) increases linearly with T (\u27e8E\u27e9 = 3/2\u202fk_B\u202fT for an ideal gas).\n\n3. **Result:** a larger fraction of the molecules now possess energy \u2265\u202fE\u2090.\n\n---\n\n## 4. Quantifying the Fraction of \u201cEnergetic\u201d Collisions  \n\nThe fraction (f) of molecules with kinetic energy \u2265\u202fE\u2090 is given (approximately) by the Boltzmann factor:\n\n\\[\nf \\approx e^{-E_a/(RT)}\n\\]\n\n- **R** = gas constant, **T** = absolute temperature (K).  \n- When T increases, the exponent becomes less negative, so **f grows exponentially**.\n\n*Example*: If E\u2090 = 50\u202fkJ\u202fmol\u207b\u00b9, at 298\u202fK, f \u2248 e\u207b\u207d\u2075\u2070\u202f000\u202f/\u202f(8.314\u00b7298)\u207e \u2248 1.2\u202f\u00d7\u202f10\u207b\u2079.  \nAt 350\u202fK, f \u2248 5.5\u202f\u00d7\u202f10\u207b\u2079 \u2013 more than a four\u2011fold increase in the fraction of \u201creactive\u201d molecules.\n\n---\n\n## 5. Collision Frequency Also Increases  \n\n1. **Molecular speed (v) \u221d \u221aT** (from kinetic theory).  \n2. **Collision frequency (Z)** for a gas mixture is roughly:\n\n\\[\nZ \\propto N_A \\, \\sigma \\, \\sqrt{\\frac{8k_B T}{\\pi \\mu}}\n\\]\n\n   - **N_A** = number density, **\u03c3** = collision cross\u2011section, **\u03bc** = reduced mass.  \n3. Raising T makes molecules move faster, so **they encounter each other more often**.\n\n---\n\n## 6. Putting It Together \u2013 The Arrhenius Equation  \n\nThe overall rate constant (k) for a simple elementary reaction is:\n\n\\[\nk = A \\, e^{-E_a/(RT)}\n\\]\n\n- **A** (the pre\u2011exponential factor) contains the **collision frequency** and the **orientation factor** (probability that a collision has the right geometry).  \n- **e\u207b\u1d31\u1d43/(RT)** is the **fraction of collisions with enough energy**.\n\nWhen T goes up:\n\n1. **A** grows modestly because collisions become more frequent (\u221d \u221aT).  \n2. The exponential term **increases dramatically** because the denominator RT gets larger, making the exponent less negative.\n\nThe combined effect is that **k can increase by orders of magnitude for a modest temperature rise**.\n\n---\n\n## 7. Consequence for Reaction Rate  \n\nFor a reaction of overall order *n* (e.g., a bimolecular reaction, rate = k\u202f[A][B]):\n\n\\[\n\\text{Rate} = k(T) \\times \\text{[reactant concentrations]}\n\\]\n\nSince **k(T)** skyrockets with temperature, the **observed rate** does as well, even if concentrations stay the same.\n\n---\n\n## 8. Visual Analogy (Optional)  \n\n- **Think of a hill (E\u2090) and a crowd of people (molecules) trying to get over it.**  \n- At a cool temperature, most people are walking slowly; only a few have enough \u201cenergy\u201d (speed) to climb the hill.  \n- Warm the crowd (raise temperature) and everyone walks faster; many more people can reach the top each minute, and they also bump into each other more often. The flow over the hill (reaction) speeds up dramatically.\n\n---\n\n## 9. Summary \u2013 Step\u2011by\u2011Step Recap  \n\n| Step | What Happens | Why It Speeds Up the Reaction |\n|------|--------------|------------------------------|\n| 1 | Molecules move and collide. | Collisions are the prerequisite for reaction. |\n| 2 | A reaction needs \u2265\u202fE\u2090 energy to cross the transition state. | Only \u201cenergetic\u201d collisions can lead to product formation. |\n| 3 | Raising T shifts the Maxwell\u2011Boltzmann distribution to higher energies. | More molecules have kinetic energy \u2265\u202fE\u2090. |\n| 4 | The Boltzmann factor \\(e^{-E_a/(RT)}\\) grows exponentially with T. | Fraction of reactive collisions rises sharply. |\n| 5 | Molecular speeds increase (\u221d\u202f\u221aT), so collisions happen more often. | Collision frequency (A) increases. |\n| 6 | Both effects appear in the Arrhenius equation \\(k = A e^{-E_a/(RT)}\\). | The rate constant k (and thus the reaction rate) rises dramatically. |\n| 7 | Faster k \u2192 faster observed rate (Rate = k\u202f[reactants]\u207f). | The reaction proceeds more quickly overall. |\n\n---\n\n### Bottom Line  \n\n**Increasing temperature speeds up a chemical reaction because it (1) makes molecules move faster, giving them more frequent collisions, and (2) gives a larger proportion of those collisions enough kinetic energy to overcome the activation energy barrier.** The combined effect is captured mathematically by the Arrhenius equation, which predicts an exponential increase in the reaction rate constant with temperature.",
      "category": "reasoning",
      "source": "remote",
      "route_p": 0.89,
      "confidence": null,
      "remote_tokens": 1620,
      "tokens_saved": 1
    },
    {
      "id": "23",
      "task": "Explain step by step why the sky appears blue.",
      "answer": "**Why the sky looks blue \u2013 a step\u2011by\u2011step explanation**\n\n---\n\n### 1. Sunlight is a mixture of many colors  \n- The Sun emits light that contains all visible wavelengths (\u2248\u202f380\u202fnm\u202f\u2013\u202f750\u202fnm).  \n- When you separate this light with a prism, you see the familiar rainbow of colors.\n\n### 2. Light must travel through Earth\u2019s atmosphere to reach us  \n- The atmosphere is a thin layer of gases (mostly nitrogen and oxygen) plus tiny particles (dust, water droplets, etc.).  \n- As sunlight passes through this layer, it interacts with the molecules and particles it encounters.\n\n### 3. Scattering of light  \n- **Scattering** is the redirection of light when it hits something smaller than its wavelength.  \n- In the atmosphere, the dominant scattering mechanism for visible light is **Rayleigh scattering**, which occurs when the scattering particles are much smaller than the wavelength of the light (the gas molecules satisfy this condition).\n\n### 4. Rayleigh scattering depends on wavelength  \n- The intensity of Rayleigh scattering varies inversely with the fourth power of wavelength (\u221d\u202f1/\u03bb\u2074).  \n- This means:  \n\n  \\[\n  \\frac{I_{\\text{blue}}}{I_{\\text{red}}} \\approx \\left(\\frac{\\lambda_{\\text{red}}}{\\lambda_{\\text{blue}}}\\right)^4\n  \\]\n\n  Since blue light (\u2248\u202f450\u202fnm) has a much shorter wavelength than red light (\u2248\u202f650\u202fnm), blue light is scattered **about 10\u202ftimes more strongly** than red.\n\n### 5. Scattered light reaches our eyes from all directions  \n- When sunlight enters the atmosphere, the blue component is scattered in every direction by the gas molecules.  \n- Even if you look away from the Sun, you still receive that scattered blue light coming from the whole sky overhead.\n\n### 6. Direct sunlight still contains all colors  \n- The light that travels straight from the Sun to your eye (the \u201cdirect beam\u201d) is only weakly affected, so it retains the full white spectrum.  \n- That\u2019s why the Sun itself looks white (or slightly yellow) while the surrounding sky is blue.\n\n### 7. Why the sky isn\u2019t violet, even though violet scatters even more  \n- Human eyes are less sensitive to violet light, and a lot of violet is absorbed by the upper atmosphere (ozone).  \n- The combination of our eye\u2019s sensitivity curve and the presence of some yellowish sunlight makes the perceived color shift toward blue rather than violet.\n\n### 8. What happens at sunrise and sunset?  \n- When the Sun is low on the horizon, its light must travel through **much more** atmosphere (a longer path).  \n- The blue light gets scattered out of the line of sight early, leaving the longer\u2011wavelength reds and oranges to dominate the direct beam, which is why the sky near the Sun appears reddish at those times.\n\n---\n\n### Quick recap in plain language  \n\n1. Sunlight contains all colors.  \n2. The atmosphere is full of tiny gas molecules.  \n3. These molecules scatter short\u2011wavelength (blue) light far more than long\u2011wavelength (red) light.  \n4. Scattered blue light comes to us from every part of the sky, making the whole dome look blue.  \n5. Our eyes see blue rather than violet because we\u2019re less sensitive to violet and because some violet is filtered out.\n\nThat\u2019s the physical reason the daytime sky appears blue!",
      "category": "reasoning",
      "source": "remote",
      "route_p": 0.88,
      "confidence": null,
      "remote_tokens": 874,
      "tokens_saved": 1
    },
    {
      "id": "24",
      "task": "Deduce who is oldest: Ann is older than Bob, Bob older than Cy.",
      "answer": "Since Ann is older than Bob, and Bob is older than Cy, the order from oldest to youngest is:\n\n**Ann \u2192 Bob \u2192 Cy**\n\nSo **Ann is the oldest**.",
      "category": "reasoning",
      "source": "remote",
      "route_p": 0.88,
      "confidence": null,
      "remote_tokens": 189,
      "tokens_saved": 2
    },
    {
      "id": "25",
      "task": "Explain the reasoning: if all A are B and all B are C, are all A C?",
      "answer": "### The statement in plain English  \n\n> **If all\u202fB are\u202fC, then all\u202fC are\u202fB?**  \n\nor, more formally,  \n\n\\[\n\\text{Premise: } \\forall x\\,(B(x) \\rightarrow C(x))\\qquad\\text{Question: Does this imply } \\forall x\\,(C(x) \\rightarrow B(x))\\;?\n\\]\n\nThe short answer is **no** \u2013 the premise does **not** guarantee the conclusion.  \nBelow is a step\u2011by\u2011step explanation of why, together with a few useful logical tools (Venn diagrams, set notation, and counter\u2011examples).\n\n---\n\n## 1. What \u201cAll\u202fB are\u202fC\u201d really means  \n\n| Symbolic form | English translation | Set\u2011theoretic picture |\n|---------------|----------------------|----------------------|\n| \\(\\forall x\\,(B(x) \\rightarrow C(x))\\) | Every object that is a B is also a C. | The set **B** is a **subset** of the set **C**:  \\(B \\subseteq C\\). |\n\nVisually:\n\n```\n   +-------------------+      C\n   |   +-------+       |      (big circle)\n   |   |  B    |       |      (small circle inside)\n   |   +-------+       |\n   +-------------------+\n```\n\nAll members of **B** sit inside **C**, but **C** may contain many other elements that are *not* in **B**.\n\n---\n\n## 2. The converse \u201cAll\u202fC are\u202fB\u201d  \n\nThe converse would be\n\n\\[\n\\forall x\\,(C(x) \\rightarrow B(x))\\qquad\\text{or}\\qquad C \\subseteq B .\n\\]\n\nFor the converse to be true, the two sets would have to be **exactly the same** (i.e., \\(B = C\\)).  \nThe original premise alone does **not** give us that information.\n\n---\n\n## 3. Why the inference is invalid \u2013 a concrete counter\u2011example  \n\n| Category | B (example) | C (example) |\n|----------|-------------|-------------|\n| Animals  | **Dogs**    | **Mammals** |\n\n- **All dogs are mammals** \u2013 true (every dog belongs to the class of mammals).  \n- **All mammals are dogs** \u2013 false (there are many mammals that are not dogs: cats, whales, humans, etc.).\n\nBecause the premise holds while the conclusion fails, the inference is **logically invalid**.\n\n---\n\n## 4. Formal proof of invalidity  \n\nA single counter\u2011example is enough to show that a universal statement does **not** entail its converse.  \nIn symbolic logic:\n\n1. Premise: \\(\\forall x\\,(B(x) \\rightarrow C(x))\\) is true in the model where  \n   - Domain = {dog, cat, whale}  \n   - \\(B(\\text{dog}) = \\text{true},\\; B(\\text{cat}) = B(\\text{whale}) = \\text{false}\\)  \n   - \\(C(\\text{dog}) = C(\\text{cat}) = C(\\text{whale}) = \\text{true}\\).\n\n2. In that same model, \\(\\forall x\\,(C(x) \\rightarrow B(x))\\) is **false** because \\(C(\\text{cat})\\) is true while \\(B(\\text{cat})\\) is false.\n\nThus the premise does **not** logically force the conclusion.\n\n---\n\n## 5. When does the inference *do* work?  \n\nThe only situation where \u201cAll\u202fB are\u202fC\u201d **does** imply \u201cAll\u202fC are\u202fB\u201d is when we already know that the two sets have the same size (or are known to be identical). Formally:\n\n\\[\n\\bigl(\\forall x\\,(B(x) \\rightarrow C(x))\\bigr) \\land \\bigl(\\forall x\\,(C(x) \\rightarrow B(x))\\bigr) \\;\\Longleftrightarrow\\; B = C .\n\\]\n\nIf we add an extra premise such as \u201cThere is no C that is not B\u201d (i.e., \\(\\neg\\exists x\\,(C(x) \\land \\neg B(x))\\)), then the conclusion follows, but that extra premise is *exactly* the converse we are trying to prove, so it adds nothing new.\n\n---\n\n## 6. A related valid inference (transitivity)  \n\nWhat *is* valid is the **transitive** chain:\n\n\\[\n\\text{All B are C} \\quad\\land\\quad \\text{All C are D} \\;\\Longrightarrow\\; \\text{All B are D}.\n\\]\n\nIn symbols:\n\n\\[\n\\bigl(\\forall x\\,(B(x) \\rightarrow C(x))\\bigr) \\land \\bigl(\\forall x\\,(C(x) \\rightarrow D(x))\\bigr) \\;\\Longrightarrow\\; \\forall x\\,(B(x) \\rightarrow D(x)).\n\\]\n\nThe proof is straightforward:\n\n1. Take an arbitrary object \\(a\\) with \\(B(a)\\).  \n2. From the first premise, \\(C(a)\\) follows.  \n3. From the second premise, \\(D(a)\\) follows.  \n4. Hence \\(B(a) \\rightarrow D(a)\\) holds for any \\(a\\), giving the universal statement.\n\n---\n\n## 7. Quick checklist for \u201cAll\u202fX are\u202fY\u201d statements  \n\n| Question | Answer \u2192 Implication |\n|----------|----------------------|\n| **Is the converse true?** | *Only if* you already know \\(X = Y\\). |\n| **Can you infer \u201cSome\u202fY are\u202fX\u201d?** | Yes, because \u201cAll\u202fX are\u202fY\u201d guarantees at least one Y (if any X exists). |\n| **Can you infer \u201cNo\u202fY are\u202fX\u201d?** | No \u2013 that would contradict the premise unless there are no X at all. |\n| **Is the statement vacuously true when there are no X?** | Yes. If the set of X\u2019s is empty, \u201cAll\u202fX are\u202fY\u201d is automatically true, but it tells you nothing about Y. |\n\n---\n\n## 8. TL;DR (Bottom line)\n\n- **\u201cAll\u202fB are\u202fC\u201d** means **B \u2286 C**.  \n- The converse **\u201cAll\u202fC are\u202fB\u201d** would require **C \u2286 B**, i.e., **B = C**.  \n- The premise alone does **not** guarantee that; a simple real\u2011world counter\u2011example (dogs vs. mammals) shows the inference is invalid.  \n- Only with an additional premise that *every* C is a B (or that the two sets are known to be identical) can you conclude the converse.\n\nFeel free to ask for more examples, a Venn\u2011diagram illustration, or a deeper dive into categorical syllogisms!",
      "category": "reasoning",
      "source": "remote",
      "route_p": 0.89,
      "confidence": null,
      "remote_tokens": 1885,
      "tokens_saved": 7
    },
    {
      "id": "26",
      "task": "Why would a semantic cache reduce token cost? Reason it out.",
      "answer": "## TL;DR  \nA **semantic cache** stores the *meaning* of past prompts and their completions, not just the raw text. When a new request is \u201cclose enough\u201d to something already in the cache, the system can reuse the cached answer (or a part of it) instead of sending the whole request to the LLM. This cuts down the number of **input tokens** (the prompt you send) and/or **output tokens** (the text the model has to generate), which directly translates into lower API\u2011billing costs and less compute time.\n\nBelow is a step\u2011by\u2011step reasoning of why and how this works, followed by practical examples, quantitative illustrations, and a quick guide to implementing a semantic cache responsibly.\n\n---\n\n## 1. What \u201ctoken cost\u201d actually means\n\n| Token type | Where it comes from | How it\u2019s billed (typical OpenAI pricing) |\n|------------|--------------------|------------------------------------------|\n| **Input tokens** | The prompt you send (including system messages, user messages, few\u2011shot examples, etc.) | Charged per\u2011token at the *input* rate |\n| **Output tokens** | The model\u2019s generated completion | Charged per\u2011token at the *output* rate (often higher than input) |\n\nIf you can **reduce either side**, you reduce the total cost:\n\n- **Fewer input tokens** \u2192 smaller payload \u2192 cheaper to send.\n- **Fewer output tokens** \u2192 less generation work \u2192 cheaper to receive.\n\nA semantic cache can affect both.\n\n---\n\n## 2. The naive \u201ctextual\u201d cache vs. a \u201csemantic\u201d cache\n\n| Cache type | Matching criterion | Typical hit\u2011rate | Token\u2011saving mechanism |\n|------------|--------------------|------------------|------------------------|\n| **Exact\u2011text cache** | Exact string equality of the whole prompt | Low (unless you have many repeated queries) | Skip the request entirely; reuse the stored answer. |\n| **Semantic cache** | *Similarity* of the *meaning* of the prompt (e.g., vector similarity) | Higher (captures paraphrases, minor wording changes) | Reuse cached answer *or* reuse parts of it, possibly with minor edits. |\n\nBecause natural language is highly variable, two users can ask the *same* question in many different ways. A semantic cache can recognize that \u201cWhat\u2019s the weather in Paris tomorrow?\u201d and \u201cWill it rain in Paris on the next day?\u201d are essentially the same request, whereas an exact\u2011text cache would miss both.\n\n---\n\n## 3. How a semantic cache reduces **input tokens**\n\n### 3.1. Short\u2011circuiting the request\n\n1. **User sends a new prompt** `P_new`.\n2. **Embedding step**: Convert `P_new` to a dense vector `v_new` (e.g., using a lightweight embedding model like OpenAI\u2019s `text-embedding-ada-002`).\n3. **Similarity search**: Look up the nearest neighbor(s) in the cache (vectors of past prompts).\n4. **Similarity threshold**: If the cosine similarity > `\u03c4` (e.g., 0.92), treat it as a *semantic hit*.\n5. **Return cached answer** `A_cached` **without calling the LLM**.\n\nResult: **Zero input tokens** and **zero output tokens** for that request. The only cost incurred is the cheap embedding call (often a few cents per 1\u202f000 tokens) and the vector\u2011search operation (negligible in most deployments).\n\n### 3.2. Prompt\u2011compression via \u201creference\u201d IDs\n\nIf you *must* call the LLM (e.g., you need a fresh answer but want to reuse context), you can:\n\n- **Replace the full prompt** with a short identifier (e.g., `<<CACHE_REF:12345>>`) that the model has been fine\u2011tuned or instructed to expand internally.\n- The model then internally \u201cremembers\u201d the cached semantics, generating a response based on the stored knowledge rather than re\u2011processing the full text.\n\nThis reduces the **input token count** from, say, 150 tokens to just a handful.\n\n---\n\n## 4. How a semantic cache reduces **output tokens**\n\n### 4.1. Re\u2011using cached completions\n\nEven when you still need to call the LLM (e.g., you want a *slightly* updated answer), you can:\n\n1. **Fetch the cached completion** `A_cached`.\n2. **Prompt the model** with a *diff* instruction:  \n   ```\n   Use the following answer as a base, but update any outdated facts:\n   <BASE_ANSWER>\n   ```\n3. The model now only needs to **edit** the base answer, often producing a **shorter output** (e.g., 20 tokens instead of 80).\n\n### 4.2. Few\u2011shot example reduction\n\nWhen you build a prompt that includes several *example* Q&A pairs (few\u2011shot learning), you can:\n\n- **Replace repeated examples** with a reference to a cached \u201ctemplate\u201d that the model has already seen.\n- This shrinks the prompt dramatically, cutting input tokens, and because the model already knows the pattern, it may need **fewer output tokens** to complete the task.\n\n---\n\n## 5. Quantitative Illustration\n\nAssume a typical usage pattern:\n\n| Metric | Without cache | With semantic cache (hit\u2011rate 70%) |\n|--------|----------------|-----------------------------------|\n| Avg. input tokens per request | 200 | 60 (30% of requests are short\u2011circuited \u2192 0 tokens; remaining 30% trimmed to 100) |\n| Avg. output tokens per request | 150 | 45 (short\u2011circuited \u2192 0; trimmed \u2192 30) |\n| Embedding cost per request | 0 | 0.0005\u202f$ (\u2248 0.5\u202f\u00a2) |\n| LLM cost per 1\u202f000 tokens (example: GPT\u20114o) | $0.03 (input) + $0.06 (output) = $0.09 | Same rates, but fewer tokens |\n| **Effective cost per request** | (200\u202f\u00d7\u202f0.03/1000) + (150\u202f\u00d7\u202f0.06/1000) = $0.012 | (60\u202f\u00d7\u202f0.03/1000) + (45\u202f\u00d7\u202f0.06/1000) + $0.0005 \u2248 $0.0045 |\n\n**Result:** ~62\u202f% cost reduction per request, even after accounting for the cheap embedding call.\n\nIf the hit\u2011rate climbs to 90\u202f% (common in highly repetitive domains like FAQ bots), the savings can exceed 80\u202f%.\n\n---\n\n## 6. Why the Savings are Real, Not Just \u201cTheoretical\u201d\n\n1. **Billing is token\u2011based** \u2013 every token that crosses the API boundary is counted. Skipping a request entirely eliminates both sides of that count.\n2. **Compute time correlates with token count** \u2013 fewer tokens mean less GPU/CPU work, which translates to lower latency and lower operational cost for self\u2011hosted models.\n3. **Embedding models are cheap** \u2013 the cost of generating a 1536\u2011dimensional vector is a fraction of a cent, far cheaper than a single LLM completion.\n4. **Cache hits are *deterministic*** \u2013 once a semantic match is found, you can guarantee the same answer (or a controlled variation), which is valuable for compliance and reproducibility.\n\n---\n\n## 7. Practical Implementation Steps\n\n### 7.1. Choose an embedding model\n- **OpenAI `text-embedding-ada-002`** (1536\u2011dim, cheap, good general\u2011purpose semantics)\n- **Open\u2011source alternatives**: `sentence\u2011transformers/all\u2011mpnet-base-v2`, `nomic\u2011embed\u2011text\u2011v1.5`, etc.\n\n### 7.2. Build the vector store\n- **Managed services**: Pinecone, Weaviate, Qdrant Cloud, Milvus.\n- **Self\u2011hosted**: FAISS (in\u2011memory), Annoy, HNSWlib.\n\n### 7.3. Define a similarity threshold\n- Empirically test on a validation set.\n- Typical values: 0.85\u20130.95 for high\u2011precision reuse; lower if you\u2019re okay with more \u201capproximate\u201d answers.\n\n### 7.4. Cache schema\n| Field | Type | Description |\n|-------|------|-------------|\n| `prompt_id` | UUID | Unique identifier |\n| `prompt_text` | TEXT | Original user prompt (optional, for debugging) |\n| `prompt_vector` | VECTOR | Embedding |\n| `completion_text` | TEXT | LLM answer |\n| `timestamp` | DATETIME | When cached |\n| `metadata` | JSON | Domain tags, source, version, etc. |\n\n### 7.5. Retrieval workflow\n```python\ndef get_answer(user_prompt):\n    v = embed(user_prompt)                     # cheap embedding call\n    hit = vector_store.search(v, k=1, threshold=\u03c4)\n    if hit:\n        return hit.completion_text             # cache hit \u2192 no LLM call\n    else:\n        # Build full prompt (maybe with few\u2011shot examples)\n        full_prompt = build_prompt(user_prompt)\n        answer = call_llm(full_prompt)         # normal API call\n        # Store for future reuse\n        vector_store.upsert(\n            id=uuid4(),\n            vector=v,\n            metadata={\"prompt\": user_prompt, \"completion\": answer}\n        )\n        return answer\n```\n\n### 7.6. Handling \u201cstale\u201d entries\n- **TTL (time\u2011to\u2011live)**: expire entries after a configurable period (e.g., 30\u202fdays) if the underlying knowledge changes.\n- **Versioning**: tag entries with a knowledge\u2011base version; on a version bump, invalidate old cache entries.\n\n### 7.7. Edge Cases & Fallbacks\n| Situation | Strategy |\n|-----------|----------|\n| **Similarity but different intent** (e.g., \u201cHow to bake a cake?\u201d vs. \u201cHow to bake a cake for a vegan diet?\u201d) | Use a higher threshold or add a secondary classifier to verify intent before reusing. |\n| **User explicitly wants a fresh answer** | Provide a UI toggle (\u201cRefresh answer\u201d) that bypasses the cache. |\n| **Regulatory compliance** (e.g., medical advice) | Enforce a *no\u2011cache* policy for high\u2011risk domains, or require human review before reuse. |\n\n---\n\n## 8. Limitations & Mitigations\n\n| Limitation | Why it matters | Mitigation |\n|------------|----------------|------------|\n| **Semantic drift** \u2013 embeddings may deem two prompts similar when they actually need different answers. | Wrong answer \u2192 user frustration, potential liability. | Use a **dual\u2011check**: similarity + a lightweight intent classifier; set a conservative threshold. |\n| **Cache size** \u2013 storing every prompt/completion can become large. | Storage cost, slower search. | Implement **eviction policies** (LRU, TTL) and **compression** (store only deltas). |\n| **Embedding cost** \u2013 still a cost, albeit tiny. | High\u2011throughput systems could see noticeable spend. | Batch embeddings, use cheaper open\u2011source models, or share embeddings across similar requests. |\n| **Stale knowledge** \u2013 cached answers may become outdated (e.g., price changes). | Misinformation. | Periodic **revalidation**: re\u2011run cached prompts after a set interval and replace if the answer differs beyond a threshold. |\n| **Privacy** \u2013 caching user data may raise GDPR/CCPA concerns. | Legal risk. | Anonymize or hash prompts before storage; provide opt\u2011out mechanisms. |\n\n---\n\n## 9. Real\u2011World Use Cases\n\n| Domain | Typical query pattern | Expected cache hit\u2011rate | Token\u2011saving impact |\n|--------|----------------------|------------------------|---------------------|\n| **Customer support FAQ bot** | Repeated \u201cHow do I reset my password?\u201d variations | 80\u201195\u202f% | 70\u201190\u202f% cost reduction |\n| **Legal document summarizer** | Similar contract clauses across clients | 60\u201180\u202f% | 50\u201170\u202f% reduction (especially on output tokens) |\n| **E\u2011commerce product search** | \u201cWhat are the specs of the iPhone 15?\u201d vs. \u201cTell me about iPhone 15 features.\u201d | 70\u202f% | 55\u202f% reduction (input + output) |\n| **Code generation assistant** | Common patterns like \u201cCreate a Python function to read a CSV.\u201d | 50\u201170\u202f% | 40\u201160\u202f% reduction (output tokens saved) |\n\n---\n\n## 10. Bottom\u2011Line Takeaway\n\nA **semantic cache** works because it **avoids sending redundant work to the LLM**. By recognizing when a new request is *meaningfully* the same as something you\u2019ve already answered, you can:\n\n1. **Skip the LLM call entirely** \u2192 zero input & output tokens.\n2. **Trim the prompt** (replace full text with a short reference) \u2192 fewer input tokens.\n3. **Reuse or edit a cached answer** \u2192 fewer output tokens.\n\nAll of this translates into **lower per\u2011request token consumption**, which directly reduces the monetary cost of using token\u2011priced APIs and also improves latency and scalability. When implemented with a sensible similarity threshold, periodic invalidation, and privacy safeguards, a semantic cache is a high\u2011ROI optimization for any production system that sees repeated or paraphrased queries.",
      "category": "reasoning",
      "source": "remote",
      "route_p": 0.88,
      "confidence": null,
      "remote_tokens": 3070,
      "tokens_saved": 1
    },
    {
      "id": "27",
      "task": "Explain step by step how backpropagation updates weights.",
      "answer": "## Back\u2011propagation in a nutshell  \n\nBack\u2011propagation (often shortened to \u201cback\u2011prop\u201d) is the algorithm that lets a neural network **learn** by adjusting its weights so that the error (loss) on the training data gets smaller.  \nAt a high level it does three things:\n\n1. **Forward pass** \u2013 compute the network\u2019s output for a given input.  \n2. **Backward pass** \u2013 compute the gradient (partial derivative) of the loss with respect to every weight, using the chain rule.  \n3. **Weight update** \u2013 move each weight a little bit in the direction that reduces the loss (gradient descent or a variant).\n\nBelow is a step\u2011by\u2011step walk\u2011through, first for a tiny network (one hidden layer) and then the general vector\u2011matrix form that scales to any architecture.\n\n---\n\n## 1\ufe0f\u20e3 A concrete example: 2\u2011input \u2192 2\u2011hidden \u2192 1\u2011output network  \n\n```\nx1 \u2500\u2500\u25ba (w1) \u2500\u2500\u25ba\n                +\u2500\u2500\u25ba h1 = \u03c3(z1) \u2500\u2500\u25ba (v1) \u2500\u2500\u25ba\nx2 \u2500\u2500\u25ba (w2) \u2500\u2500\u25ba                +\u2500\u2500\u25ba y\u0302 = \u03c3(z3)\n                +\u2500\u2500\u25ba h2 = \u03c3(z2) \u2500\u2500\u25ba (v2) \u2500\u2500\u25ba\n```\n\n* `x = [x1, x2]` \u2013 input vector  \n* `w1, w2, \u2026` \u2013 weights from input \u2192 hidden  \n* `v1, v2` \u2013 weights from hidden \u2192 output  \n* `\u03c3` \u2013 activation function (e.g., sigmoid, ReLU)  \n* `y\u0302` \u2013 network prediction  \n* `y` \u2013 true target  \n\n### Notation for this walk\u2011through  \n\n| Symbol | Meaning |\n|--------|---------|\n| `z\u2081 = w\u2081\u00b7x\u2081 + w\u2082\u00b7x\u2082 + b\u2081` | pre\u2011activation of hidden unit\u202f1 |\n| `h\u2081 = \u03c3(z\u2081)` | activation of hidden unit\u202f1 |\n| `z\u2082 = w\u2083\u00b7x\u2081 + w\u2084\u00b7x\u2082 + b\u2082` | pre\u2011activation of hidden unit\u202f2 |\n| `h\u2082 = \u03c3(z\u2082)` | activation of hidden unit\u202f2 |\n| `z\u2083 = v\u2081\u00b7h\u2081 + v\u2082\u00b7h\u2082 + b\u2083` | pre\u2011activation of output unit |\n| `y\u0302 = \u03c3(z\u2083)` | final output (prediction) |\n| `L(y, y\u0302)` | loss function (e.g., MSE = \u00bd(y\u2011y\u0302)\u00b2 or cross\u2011entropy) |\n\n---\n\n## 2\ufe0f\u20e3 Step\u2011by\u2011step procedure  \n\n### **Step 0 \u2013 Initialise**  \n* Randomly initialise all weights (`w`s, `v`s) and biases (`b`s) (e.g., with a Gaussian of small variance).  \n* Choose a learning rate `\u03b7` (step size) and a loss function `L`.\n\n---\n\n### **Step 1 \u2013 Forward pass (compute activations & loss)**  \n\n1. **Hidden layer**  \n   ```\n   z1 = w1*x1 + w2*x2 + b1\n   h1 = \u03c3(z1)\n\n   z2 = w3*x1 + w4*x2 + b2\n   h2 = \u03c3(z2)\n   ```\n\n2. **Output layer**  \n   ```\n   z3 = v1*h1 + v2*h2 + b3\n   y\u0302 = \u03c3(z3)          # network prediction\n   ```\n\n3. **Loss**  \n   ```\n   L = loss(y, y\u0302)    # e.g. \u00bd (y - y\u0302)\u00b2\n   ```\n\nAll these quantities are now known for the current training example.\n\n---\n\n### **Step 2 \u2013 Backward pass (compute gradients)**  \n\nThe goal: obtain \u2202L/\u2202\u03b8 for every weight/bias \u03b8.  \nWe start from the output and move **backwards**, applying the chain rule.\n\n#### 2.1 Gradient at the output node  \n\n```\n\u03b43 = \u2202L/\u2202z3 = \u2202L/\u2202y\u0302 * \u2202y\u0302/\u2202z3\n```\n\n* For MSE: \u2202L/\u2202y\u0302 = -(y - y\u0302)  \n* For sigmoid output: \u2202y\u0302/\u2202z3 = \u03c3'(z3) = y\u0302\u00b7(1 - y\u0302)  \n\nThus  \n\n```\n\u03b43 = (y\u0302 - y) * \u03c3'(z3)          # note the sign flip for MSE\n```\n\n`\u03b43` is often called the **error signal** for the output unit.\n\n#### 2.2 Gradients for output\u2011layer weights & bias  \n\n```\n\u2202L/\u2202v1 = \u03b43 * h1\n\u2202L/\u2202v2 = \u03b43 * h2\n\u2202L/\u2202b3 = \u03b43\n```\n\nBecause `z3 = v1*h1 + v2*h2 + b3`, the derivative w.r.t. each weight is simply the upstream error `\u03b43` times the activation feeding into that weight.\n\n#### 2.3 Propagate the error to the hidden layer  \n\nFor each hidden unit `i` we compute its own error signal `\u03b4i`:\n\n```\n\u03b41 = (\u03b43 * v1) * \u03c3'(z1)\n\u03b42 = (\u03b43 * v2) * \u03c3'(z2)\n```\n\nExplanation:  \n* `\u03b43 * v1` is the contribution of hidden unit\u202f1 to the output error (chain rule).  \n* Multiply by the derivative of the hidden activation `\u03c3'(z1)` to get the gradient w.r.t. the hidden pre\u2011activation.\n\n#### 2.4 Gradients for input\u2011to\u2011hidden weights & biases  \n\n```\n\u2202L/\u2202w1 = \u03b41 * x1\n\u2202L/\u2202w2 = \u03b41 * x2\n\u2202L/\u2202b1 = \u03b41\n\n\u2202L/\u2202w3 = \u03b42 * x1\n\u2202L/\u2202w4 = \u03b42 * x2\n\u2202L/\u2202b2 = \u03b42\n```\n\nAgain, each weight\u2019s gradient is the upstream error signal for that neuron times the activation that fed into it.\n\n---\n\n### **Step 3 \u2013 Weight update (gradient descent)**  \n\nWith all partial derivatives in hand, we move each parameter a little opposite to the gradient:\n\n```\nv1 \u2190 v1 - \u03b7 * \u2202L/\u2202v1\nv2 \u2190 v2 - \u03b7 * \u2202L/\u2202v2\nb3 \u2190 b3 - \u03b7 * \u2202L/\u2202b3\n\nw1 \u2190 w1 - \u03b7 * \u2202L/\u2202w1\nw2 \u2190 w2 - \u03b7 * \u2202L/\u2202w2\nb1 \u2190 b1 - \u03b7 * \u2202L/\u2202b1\n\nw3 \u2190 w3 - \u03b7 * \u2202L/\u2202w3\nw4 \u2190 w4 - \u03b7 * \u2202L/\u2202w4\nb2 \u2190 b2 - \u03b7 * \u2202L/\u2202b2\n```\n\n*If you use a variant such as **Stochastic Gradient Descent (SGD)** you repeat the whole process for each training example (or a mini\u2011batch).  \n*If you use **Adam**, RMSProp, etc., the update rule includes momentum\u2011like terms and adaptive learning\u2011rates, but the core gradient computation stays exactly the same.*\n\n---\n\n## 4\ufe0f\u20e3 Vector\u2011matrix formulation (the way libraries implement it)\n\nFor larger networks we write everything in matrix form, which lets us compute all gradients with a few matrix multiplications.\n\n### Notation  \n\n* `X` \u2013 input column vector (size `n_in`)  \n* `W\u00b9` \u2013 weight matrix from input \u2192 hidden (size `n_hidden \u00d7 n_in`)  \n* `b\u00b9` \u2013 bias vector for hidden (size `n_hidden`)  \n* `a\u00b9 = \u03c3( W\u00b9 X + b\u00b9 )` \u2013 hidden activations (size `n_hidden`)  \n* `W\u00b2` \u2013 weight matrix from hidden \u2192 output (size `n_out \u00d7 n_hidden`)  \n* `b\u00b2` \u2013 bias vector for output (size `n_out`)  \n* `z\u00b2 = W\u00b2 a\u00b9 + b\u00b2` \u2013 pre\u2011activation of output  \n* `\u0177 = \u03c3_out(z\u00b2)` \u2013 network output (size `n_out`)  \n* `L(\u0177, Y)` \u2013 loss (Y is the true target vector)\n\n### Forward pass (vectorized)\n\n```\nz\u00b9 = W\u00b9 X + b\u00b9\na\u00b9 = \u03c3(z\u00b9)\n\nz\u00b2 = W\u00b2 a\u00b9 + b\u00b2\n\u0177 = \u03c3_out(z\u00b2)\n```\n\n### Backward pass (vectorized)\n\n1. **Output error signal**  \n\n   ```\n   \u03b4\u00b2 = \u2202L/\u2202z\u00b2 = (\u2202L/\u2202\u0177) \u2299 \u03c3_out'(z\u00b2)\n   ```\n\n   (`\u2299` denotes element\u2011wise product.)\n\n2. **Gradients for output layer**  \n\n   ```\n   \u2202L/\u2202W\u00b2 = \u03b4\u00b2 a\u00b9\u1d40          # outer product\n   \u2202L/\u2202b\u00b2 = \u03b4\u00b2               # sum over batch dimension if using mini\u2011batches\n   ```\n\n3. **Propagate to hidden layer**  \n\n   ```\n   \u03b4\u00b9 = (W\u00b2\u1d40 \u03b4\u00b2) \u2299 \u03c3'(z\u00b9)\n   ```\n\n4. **Gradients for hidden layer**  \n\n   ```\n   \u2202L/\u2202W\u00b9 = \u03b4\u00b9 X\u1d40\n   \u2202L/\u2202b\u00b9 = \u03b4\u00b9\n   ```\n\n### Weight update (generic)\n\n```\nW\u00b9 \u2190 W\u00b9 - \u03b7 * \u2202L/\u2202W\u00b9\nb\u00b9 \u2190 b\u00b9 - \u03b7 * \u2202L/\u2202b\u00b9\nW\u00b2 \u2190 W\u00b2 - \u03b7 * \u2202L/\u2202W\u00b2\nb\u00b2 \u2190 b\u00b2 - \u03b7 * \u2202L/\u2202b\u00b2\n```\n\nIf you are training on a **mini\u2011batch** of size `m`, the formulas above are applied to the whole batch at once, and the bias gradients become the mean (or sum) of the `\u03b4` vectors across the batch.\n\n---\n\n## 5\ufe0f\u20e3 Key points to remember  \n\n| Concept | Why it matters |\n|---------|----------------|\n| **Chain rule** | Allows us to decompose the derivative of a deep composition of functions into a product of local derivatives (`\u03b4` terms). |\n| **Error signal (`\u03b4`)** | The quantity that \u201ccarries\u201d the loss information backward through the network. Each layer\u2019s `\u03b4` is the upstream `\u03b4` multiplied by the weight that connects them and by the activation derivative. |\n| **Local gradients** | For a weight `w_ij` connecting neuron `j` (in the previous layer) to neuron `i` (in the current layer), the gradient is `\u03b4_i * a_j`. This is why the update rule looks like \u201cerror \u00d7 input\u201d. |\n| **Learning rate (`\u03b7`)** | Controls step size. Too large \u2192 divergence; too small \u2192 painfully slow learning. |\n| **Mini\u2011batch vs. full\u2011batch** | Mini\u2011batch (e.g., 32\u2011256 examples) gives a noisy but faster estimate of the gradient, which is why SGD works well in practice. |\n| **Activation derivatives** | Must be easy to compute. Sigmoid \u2192 `\u03c3(z)(1-\u03c3(z))`; ReLU \u2192 `1` if `z>0` else `0`; tanh \u2192 `1 - tanh\u00b2(z)`. |\n| **Weight initialization** | Proper scaling (e.g., Xavier/Glorot, He) keeps the initial `\u03b4` values from exploding or vanishing. |\n| **Vanishing / exploding gradients** | In very deep nets, repeated multiplication by small/large derivatives can shrink or blow up `\u03b4`. Modern tricks (ReLU, batch norm, residual connections, careful init) mitigate this. |\n\n---\n\n## 6\ufe0f\u20e3 Quick pseudo\u2011code (Python\u2011like) for a single training step  \n\n```python\ndef forward(x, params):\n    z1 = params.W1 @ x + params.b1          # (h, )\n    a1 = sigmoid(z1)                        # hidden activation\n    z2 = params.W2 @ a1 + params.b2         # (out, )\n    y_hat = sigmoid(z2)                     # network output\n    cache = (x, z1, a1, z2, y_hat)\n    return y_hat, cache\n\ndef backward(y, cache, params):\n    x, z1, a1, z2, y_hat = cache\n\n    # ---- output layer ----\n    dL_dyhat = y_hat - y                     # dL/dy\u0302 for MSE\n    delta2 = dL_dyhat * sigmoid_derivative(z2)   # \u03b4\u00b3\n    dW2 = np.outer(delta2, a1)               # \u2202L/\u2202W\u00b2\n    db2 = delta2\n\n    # ---- hidden layer ----\n    delta1 = (params.W2.T @ delta2) * sigmoid_derivative(z1)  # \u03b4\u00b9\n    dW1 = np.outer(delta1, x)                # \u2202L/\u2202W\u00b9\n    db1 = delta1\n\n    grads = {'W1': dW1, 'b1': db1, 'W2': dW2, 'b2': db2}\n    return grads\n\ndef update(params, grads, lr):\n    params.W1 -= lr * grads['W1']\n    params.b1 -= lr * grads['b1']\n    params.W2 -= lr * grads['W2']\n    params.b2 -= lr * grads['b2']\n```\n\nRunning `forward \u2192 loss \u2192 backward \u2192 update` for each training example (or mini\u2011batch) is exactly what modern deep\u2011learning libraries (TensorFlow, PyTorch, JAX) do under the hood\u2014only they vectorise the operations and add extra tricks (momentum, weight decay, etc.).\n\n---\n\n## 7\ufe0f\u20e3 TL;DR (the \u201ccheat sheet\u201d)  \n\n1. **Forward pass** \u2013 compute activations layer by layer, then the loss.  \n2. **Output error** \u2013 `\u03b4_out = \u2202L/\u2202output * activation\u2032(pre\u2011output)`.  \n3. **Back\u2011propagate** \u2013 for each layer `l` (from last to first):  \n   * `\u03b4_l = (W_{l+1}\u1d40 \u03b4_{l+1}) \u2299 activation\u2032(z_l)`  \n   * Gradient for weights: `\u2202L/\u2202W_l = \u03b4_l a_{l\u20111}\u1d40`  \n   * Gradient for biases: `\u2202L/\u2202b_l = \u03b4_l`  \n4. **Update** \u2013 `W_l \u2190 W_l - \u03b7 * \u2202L/\u2202W_l`, `b_l \u2190 b_l - \u03b7 * \u2202L/\u2202b_l`.  \n\nThat\u2019s back\u2011propagation in a nutshell: a systematic way to compute *how* each weight contributed to the error, and then nudge it a little so the error gets smaller next time. Happy training!",
      "category": "reasoning",
      "source": "remote",
      "route_p": 0.88,
      "confidence": null,
      "remote_tokens": 3485,
      "tokens_saved": 0
    },
    {
      "id": "28",
      "task": "Calculate the sum of 145 and 278.",
      "answer": "The sum of 145 and 278 is **423**.",
      "category": "math",
      "source": "remote",
      "route_p": 0.87,
      "confidence": null,
      "remote_tokens": 134,
      "tokens_saved": 3
    },
    {
      "id": "29",
      "task": "How many is 12 multiplied by 12?",
      "answer": "12\u202f\u00d7\u202f12\u202f=\u202f144.",
      "category": "math",
      "source": "remote",
      "route_p": 0.87,
      "confidence": null,
      "remote_tokens": 137,
      "tokens_saved": 1
    },
    {
      "id": "30",
      "task": "Solve for x: 2x + 6 = 20.",
      "answer": "To solve the linear equation  \n\n\\[\n2x + 6 = 20,\n\\]\n\nfollow these steps:\n\n1. **Isolate the term with \\(x\\)**  \n   Subtract 6 from both sides:\n\n   \\[\n   2x + 6 - 6 = 20 - 6 \\quad\\Longrightarrow\\quad 2x = 14.\n   \\]\n\n2. **Solve for \\(x\\)**  \n   Divide both sides by 2:\n\n   \\[\n   \\frac{2x}{2} = \\frac{14}{2} \\quad\\Longrightarrow\\quad x = 7.\n   \\]\n\n\\[\n\\boxed{x = 7}\n\\]",
      "category": "math",
      "source": "remote",
      "route_p": 0.87,
      "confidence": null,
      "remote_tokens": 277,
      "tokens_saved": 1
    },
    {
      "id": "31",
      "task": "What is 15% of 240?",
      "answer": "36",
      "category": "qa",
      "source": "local",
      "route_p": 0.24,
      "confidence": 0.95,
      "remote_tokens": 0,
      "tokens_saved": 0
    },
    {
      "id": "32",
      "task": "Calculate the product of 23 and 47.",
      "answer": "The product of \\(23\\) and \\(47\\) is  \n\n\\[\n23 \\times 47 = 1081.\n\\]",
      "category": "math",
      "source": "remote",
      "route_p": 0.87,
      "confidence": null,
      "remote_tokens": 170,
      "tokens_saved": 3
    },
    {
      "id": "33",
      "task": "A train travels 60 km in 45 minutes; how many km/h?",
      "answer": "To find the speed in\u202fkm/h, use the formula  \n\n\\[\n\\text{speed} = \\frac{\\text{distance}}{\\text{time}}\n\\]\n\n1. **Convert the time to hours**  \n   \\[\n   45\\text{ minutes} = \\frac{45}{60}\\text{ hour} = 0.75\\text{ h}\n   \\]\n\n2. **Divide the distance by the time**  \n   \\[\n   \\text{speed} = \\frac{60\\text{ km}}{0.75\\text{ h}} = 80\\text{ km/h}\n   \\]\n\n**Answer:** The train travels at **80\u202fkm/h**.",
      "category": "math",
      "source": "remote",
      "route_p": 0.88,
      "confidence": null,
      "remote_tokens": 318,
      "tokens_saved": 1
    },
    {
      "id": "34",
      "task": "Compute the compound interest on 1000 at 5% for 2 years.",
      "answer": "**Compound\u2011interest calculation**\n\n- **Principal (P):**\u202f\\$1,000  \n- **Annual interest rate (r):**\u202f5\u202f%\u202f=\u202f0.05  \n- **Time (t):**\u202f2\u202fyears  \n- **Compounding frequency:**\u202fAssumed once per year (annual compounding)\n\nThe future value after \\(t\\) years is  \n\n\\[\nA = P\\,(1+r)^{t}\n\\]\n\n\\[\nA = 1000\\,(1+0.05)^{2}\n   = 1000\\,(1.05)^{2}\n   = 1000 \\times 1.1025\n   = \\$1,102.50\n\\]\n\n**Compound interest earned**\n\n\\[\n\\text{Interest} = A - P = 1,102.50 - 1,000 = \\$102.50\n\\]\n\n---\n\n**Result:** After 2 years, the investment grows to **\\$1,102.50**, meaning you earn **\\$102.50** in compound interest.",
      "category": "qa",
      "source": "remote",
      "route_p": 0.27,
      "confidence": 0.0,
      "remote_tokens": 440,
      "tokens_saved": 4
    },
    {
      "id": "35",
      "task": "How many multiply steps to compute 2^10 by squaring?",
      "answer": "To compute \\(2^{10}\\) with **exponentiation by squaring**, you count two kinds of multiplications:\n\n1. **Squaring steps** \u2013 each time you replace the current base by its square.  \n2. **\u201cMultiply\u2011into\u2011result\u201d steps** \u2013 each time the current exponent bit is\u202f1 and you multiply the accumulated result by the current base.\n\n---\n\n### Binary view of the exponent  \n\n\\(10_{10}=1010_2\\)\n\n- There are \\(\\lfloor\\log_2 10\\rfloor = 3\\) squaring operations (one for each shift of the exponent).  \n- The binary representation has two 1\u2011bits, so you need two \u201cmultiply\u2011into\u2011result\u201d operations (one for each 1\u2011bit).\n\n---\n\n### Step\u2011by\u2011step walk\u2011through  \n\n| Step | Exponent (binary) | Action | Multiplication performed? |\n|------|-------------------|--------|---------------------------|\n| 0    | 1010              | start: base\u202f=\u202f2, result\u202f=\u202f1 | \u2013 |\n| 1    | 1010 \u2192 0101 (even) | **Square**: \\(2 \\times 2 = 4\\) | 1 |\n| 2    | 0101 (odd)        | **Result\u202f\u00d7=\u202fbase**: \\(1 \\times 4 = 4\\) | 2 |\n|      |                   | **Square**: \\(4 \\times 4 = 16\\) | 3 |\n| 3    | 0010 (even)       | **Square**: \\(16 \\times 16 = 256\\) | 4 |\n| 4    | 0001 (odd)        | **Result\u202f\u00d7=\u202fbase**: \\(4 \\times 256 = 1024\\) | 5 |\n|      | (exponent becomes 0) | stop | \u2013 |\n\nTotal multiplications = **3 squarings + 2 result\u2011multiplications = 5**.\n\n---\n\n## Answer\n**It takes 5 multiplication steps to compute \\(2^{10}\\) by exponentiation\u2011by\u2011squaring.**",
      "category": "math",
      "source": "remote",
      "route_p": 0.88,
      "confidence": null,
      "remote_tokens": 1176,
      "tokens_saved": 0
    }
  ],
  "agg": {
    "n": 36,
    "remote_tokens": 14054,
    "tokens_saved": 26,
    "free_pct": 61.1,
    "escalate_pct": 38.9,
    "cache_hits": 0,
    "mix": {
      "local": 22,
      "remote": 14
    },
    "by_category": {
      "classification": {
        "local": 5,
        "remote": 0,
        "cache": 0,
        "other": 0
      },
      "qa": {
        "local": 7,
        "remote": 1,
        "cache": 0,
        "other": 0
      },
      "extraction": {
        "local": 6,
        "remote": 0,
        "cache": 0,
        "other": 0
      },
      "summarization": {
        "local": 4,
        "remote": 0,
        "cache": 0,
        "other": 0
      },
      "math": {
        "local": 0,
        "remote": 7,
        "cache": 0,
        "other": 0
      },
      "reasoning": {
        "local": 0,
        "remote": 6,
        "cache": 0,
        "other": 0
      }
    }
  }
};
