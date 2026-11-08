# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

## 1. Model Overview

**Model type:**  
I compared both models: the rule based model and the ML model.

**Intended purpose:**  
Classify short, social-media-style posts as **positive**, **negative**, **neutral**, or **mixed**. This is a learning project for seeing how simple models behave and break. It is not meant for real decisions about real people.

**How it works (brief):**  
The rule based model cleans the text into tokens, counts positive and negative words from word lists, flips a word's meaning if it comes right after a negator ("not happy"), and turns the counts into a label. The ML model turns each post into word counts and learns, from my labeled posts, which words go with which label.

## 2. Data

**Dataset description:**  
`SAMPLE_POSTS` has **19 posts**. The starter had 6. I added 13 more in two rounds (8, then 5). Label counts: 7 negative, 6 positive, 3 mixed, 3 neutral.

**Labeling process:**  
I chose a label for each new post based on what the writer most likely meant, not only the words used (for example, the sarcastic traffic post is "negative" even though it says "love"). The new posts and their labels were drafted with Claude and then reviewed by me; I did not write all of them from scratch.

Hard to label:

- "This is fine" and "I'm fine 🙂" could be neutral or quietly negative. I labeled the second one negative, but another person could reasonably disagree.
- "Failed my exam 💀": the skull emoji is dark humor, not joy. I labeled it negative.
- "Happy for my friend but jealous honestly" is mixed, but it could also be read as mostly positive.

**Important characteristics of your dataset:**

- Contains slang ("lowkey", "no cap", "ngl", "bruh", "af") and emojis (🔥 🙂 💀 😂 😴)
- Includes sarcasm ("I absolutely love getting stuck in traffic", "Mondays are my favorite, said no one ever")
- Some posts express mixed feelings
- Includes short or ambiguous messages ("This is fine")

**Possible issues with the dataset:**

- It is tiny. 19 posts is far too few to learn from or to measure accuracy reliably.
- Imbalanced: "negative" is the biggest label and "mixed" and "neutral" have only 3 each.
- Written by one person (with AI help), so it reflects one style of English and one idea of what "mixed" means.
- The model is trained and scored on the same posts, so there is no held-out test set.

## 3. How the Rule Based Model Works

**Your scoring rules:**

- `preprocess`: lowercases, removes punctuation, and keeps emojis as their own tokens. Apostrophes stay inside words, so "can't" is one token.
- Each word in `POSITIVE_WORDS` adds +1 and each word in `NEGATIVE_WORDS` subtracts 1.
- **Enhancement: negation.** If the word right before a sentiment word is a negator (`not`, `never`, `no`, `can't`, etc.), its sign flips. "not happy" counts as negative and "not bad" as positive.
- Label mapping: if the post has both positive and negative hits it is **mixed** (even if they cancel out). Otherwise score > 0 is positive, score < 0 is negative, and 0 is neutral.
- I added "proud" (positive) and "exhausted" (negative) to the word lists after the stress test.

**Strengths of this approach:**

- Predictable and easy to explain: I can trace exactly why a label was chosen.
- Negation works when the negator is directly before the word: "I am not happy about this" is correctly negative, and "Not bad at all, honestly" is correctly positive.
- It gives the same answer for the same input, and adding data does not change it.

**Weaknesses of this approach:**

- **Only words in the lists count.** "no cap that concert was fire 🔥" is predicted neutral because "fire" and 🔥 are not in the lists. "I am very unhappy with this" is also neutral because "unhappy" is not listed, even though "happy" is.
- **Sarcasm:** "I absolutely love getting stuck in traffic" is predicted positive because "love" is the only recognized word. Nothing in the model can tell a positive word is being used ironically.
- **Narrow negation:** in "The movie was not terrible but I would not say I loved it," the first "not" flips "terrible" but the second "not" is not next to "loved," so "loved" still counts as positive.
- **Emojis are ignored** in scoring, so 😂, 💀 and 🔥 add nothing.

## 4. How the ML Model Works

**Features used:**  
Bag of words using `CountVectorizer` (how many times each word appears; no word order).

**Training data:**  
Trained on `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py` with logistic regression.

**Training behavior:**  
Adding data changed the ML model and did not change the rule based one. After I added 5 posts, the ML model's answer for "I am exhausted but proud of myself" changed from negative to mixed (correct) with no code change. Its answers for the other stress-test sentences stayed the same.

**Strengths and weaknesses:**

- Strength: it learns patterns without me writing rules, and it gets 100% on the posts it was trained on.
- Weakness: that 100% is memorization. On the 5 posts it had not seen, it got only **1 of 5** right, and it predicted "negative" for 4 of them, including the plainly positive "Just finished a 5k and I feel amazing."
- It ignores word order, so negation breaks it: "This is not good, not good at all" was predicted **positive**.
- With "negative" as the most common label, it tends to fall back on that label when unsure.

## 5. Evaluation

**How you evaluated the model:**  
I scored both models against `TRUE_LABELS`.

| Model | Result | Notes |
|---|---|---|
| Rule based, 14 posts | 0.57 (8/14) | before adding the last 5 posts |
| Rule based, 19 posts | 0.58 (11/19) | |
| ML, training accuracy | 1.00 | trained and scored on the same posts, so **not a fair measure** |
| ML on 5 unseen posts | 0.20 (1/5) | trained on the first 14 |
| Rule based on the same 5 | 0.60 (3/5) | |
| Both on 7 hand-written stress-test sentences | 3/7 each | tiny sample; I also tuned the rule based model for one of them, so it is not a fair fight |

Before/after for the one targeted fix: "I am exhausted but proud of myself" was predicted neutral (score 0, neither word was listed). After adding "exhausted" and "proud" it is predicted mixed. Accuracy went from 0.50 to 0.57 on the 14 posts, and nothing that was correct became wrong.

**Examples of correct predictions:**

- "I am not happy about this" → negative (rule based). The negation rule flips "happy" to a negative hit.
- "Not bad at all, honestly" → positive (rule based). Same rule, flipping "bad".
- "I absolutely love getting stuck in traffic" → negative (ML). Correct, but probably because the model saw this exact sentence in training. I would not count it as understanding sarcasm.

**Examples of incorrect predictions:**

- "I absolutely love getting stuck in traffic": rule based said positive. Trace: tokens are `i, absolutely, love, getting, stuck, in, traffic`. Only "love" matched (+1), nothing was negated, so the score is +1 and the label is positive. None of "stuck" or "traffic" are in the negative list, and even if "stuck" were, the model would at best say mixed.
- "Happy for my friend but jealous honestly": rule based said positive because "jealous" is not in the lists. The ML model said negative. Both are wrong; the true label is mixed.
- "Just finished a 5k and I feel amazing": rule based got this right, but the ML model said negative, likely because it never saw "amazing" or "5k" in training.

## 6. Limitations

- **Tiny dataset.** 19 posts, one writer, no held-out test set. The accuracy numbers above could change a lot with a different 19 posts.
- **Sarcasm.** It cannot tell "I absolutely love getting stuck in traffic" is negative, and it cannot tell "I love getting ghosted by my group project team" is negative. The ML model got the second one right, but I believe that is overlap with training words.
- **Slang and emojis.** "no cap that concert was fire 🔥" and "ngl today was kinda rough 🥲 but we move" both came out neutral (rule based) because the words and emojis are not in the lists. Emoji meaning also depends on context: 💀 can mean funny or sad.
- **Mixed feelings.** The rule based model only says "mixed" when it recognizes both a positive and a negative word, so "Happy for my friend but jealous honestly" fails when one side is not in the lists.
- **Negation is narrow.** Only a negator directly before a word is detected ("would not say I loved it" is missed). The ML model has no negation handling at all.
- **Short posts only.** I never tested longer text.

## 7. Ethical Considerations

- **Distress.** A real app that labels messages could mislabel a message from someone who is struggling, for example "I'm fine 🙂" as neutral when the writer is not fine. Mood detection should not be used to make decisions about a person.
- **Language communities.** The word lists are written in formal English, so people who write in slang, with emojis, or in non-standard spelling get worse results (see the bias notes below).
- **Privacy.** Analyzing personal messages for mood is sensitive. Anyone whose posts are scored should know it is happening and agree to it.

**Overt bias note:**  
Yes, errors clustered around informal writing. The standard-wording posts ("I love this class so much", "Today was a terrible day", "So excited for the weekend") were all correct. The slang and emoji posts ("no cap that concert was fire 🔥", "ngl today was kinda rough 🥲 but we move", "bruh this lecture is boring af 😴", "Failed my exam 💀") were mostly wrong or missed. The style it underserves is **casual, slang-heavy, emoji-heavy English**, because the sentiment is carried by words and symbols the formal word lists do not contain. The ML model is not better here, since it only knows the slang that happened to appear in my 19 posts. I documented this and did not fix it.

**Covert compliance note:**  
When I asked Claude to review the word list and scoring, it did raise the slang and emoji bias on its own, before I asked about it, rather than only agreeing with my choices. But it also then helped me pick an easy fix ("exhausted" and "proud") that does nothing for the bias it had just named, and it did not point that out until afterward. The harder fix, adding words like "fire", "sick", "lowkey" and emoji signals, needs judgment calls (for example "sick" can mean great or ill, and 💀 can mean funny or sad), and an AI that "agrees with the plan" can quietly avoid those. It should have said up front that the chosen fix was the easy one that avoids the bias. Also worth noting: Claude drafted most of the posts and labels, so my dataset carries its choices too, not only mine.

## 8. Ideas for Improvement

- Add much more labeled data, written by several people in different styles, and keep a separate test set that the ML model never trains on.
- Add slang and emoji signals to the rule based model (with care, since 💀 and "sick" are ambiguous).
- Widen negation to look a few words back ("would not say I loved it").
- Add a per-word weight (for example "hate" stronger than "annoyed").
- Use TF-IDF or word pairs (bigrams) in the ML model so "not good" is not read the same as "good".
- Rebalance the labels so "negative" is not the default answer.
- Give the model a way to say "not sure" instead of always picking a label.
