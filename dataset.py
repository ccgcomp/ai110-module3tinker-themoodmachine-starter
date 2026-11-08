"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "proud",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "exhausted",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
]

SAMPLE_POSTS.extend([
    "Lowkey stressed but kind of proud of myself",
    "I absolutely love getting stuck in traffic",
    "no cap that concert was fire 🔥",
    "I'm fine 🙂",
    "Failed my exam 💀",
    "Got the internship!!! 😂 can't stop smiling",
    "Not bad at all, honestly",
    "Woke up, ate breakfast, went to class",
])

TRUE_LABELS.extend([
    "mixed",     # "Lowkey stressed but kind of proud of myself"
    "negative",  # "I absolutely love getting stuck in traffic" (sarcasm)
    "positive",  # "no cap that concert was fire 🔥" (slang)
    "negative",  # "I'm fine 🙂" (ambiguous: passive-aggressive "fine")
    "negative",  # "Failed my exam 💀" (💀 here is just dark humor, not joy)
    "positive",  # "Got the internship!!! 😂 can't stop smiling"
    "positive",  # "Not bad at all, honestly" (negation of a negative word)
    "neutral",   # "Woke up, ate breakfast, went to class"
])

SAMPLE_POSTS.extend([
    "Mondays are my favorite, said no one ever",
    "Just finished a 5k and I feel amazing",
    "Nothing special happening today",
    "Happy for my friend but jealous honestly",
    "bruh this lecture is boring af 😴",
])

TRUE_LABELS.extend([
    "negative",  # "Mondays are my favorite, said no one ever" (sarcasm)
    "positive",  # "Just finished a 5k and I feel amazing"
    "neutral",   # "Nothing special happening today"
    "mixed",     # "Happy for my friend but jealous honestly"
    "negative",  # "bruh this lecture is boring af 😴" (slang)
])

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
