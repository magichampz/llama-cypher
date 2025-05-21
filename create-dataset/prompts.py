question_focuses = [
    "Subtle differences between similar concepts",
    "Edge cases and non-obvious implications",
    "Multi-step reasoning and cause-effect relationships",
    "Ability to apply knowledge to novel situations",
    "Recognition of subtle security implications",
    "Understanding of complex regulatory requirements"
]

# duplicate mcq generation prompt 1
# to do: make more specific prompts for different kinds of questions

MCQ_GENERATION_PROMPT_2 = """
    Topic: {topic}
    Subtopic: {subtopic}
    
    Generate a highly challenging multiple choice questions (MCQs) about this topic and subtopic in healthcare cybersecurity.
    The question should test understanding of {question_focus}.
    
    Guidelines for creating challenging questions:
    1. Focus on complex, nuanced scenarios that require deep domain knowledge in medical device cybersecurity
    2. Make wrong options plausible and require careful analysis to distinguish
    3. Avoid questions that can be answered through simple pattern matching or basic knowledge


    For each MCQ, output a JSON object with the following fields:
    - 'topic': the topic name
    - 'subtopic': the subtopic name
    - 'question': a question stem that presents a complex scenario or concept
    - 'options': an array of 4 carefully crafted answer options labeled A, B, C, D
    - 'correct_answer': a single letter representing the correct option (A, B, C, or D)

    JSON Formatting Rules:
    1. Do NOT include trailing commas in arrays or objects
    2. String Formatting Rules:
       - Use double quotes for all strings
       - Only escape double quotes within strings with a backslash: \\"
       - Do NOT escape single quotes (apostrophes) - they are valid in JSON strings
       - Do not use any other escape sequences
       - Do not include newlines within strings

    Return the question as a JSON object.
    DO NOT include any markdown code block markers in the response.
    """


MCQ_GENERATION_PROMPT_1 = """
    Topic: {topic}
    Subtopic: {subtopic}
    Generate 3 highly challenging multiple choice questions (MCQs) about this topic and subtopic in healthcare cybersecurity.
    
    Guidelines for creating challenging questions:
    1. Focus on complex, nuanced scenarios that require deep domain knowledge in medical device cybersecurity
    2. Include questions that test understanding of:
       - Subtle differences between similar concepts
       - Complex interactions between different security components
       - Edge cases and non-obvious implications
       - Multi-step reasoning and cause-effect relationships
    3. Make distractors (wrong options) plausible and require careful analysis to distinguish
    4. Include questions that test:
       - Understanding of underlying principles rather than just facts
       - Ability to apply knowledge to novel situations
       - Recognition of subtle security implications
       - Understanding of complex regulatory requirements
    5. Avoid questions that can be answered through simple pattern matching or basic knowledge

    Each question should have:
    - A clear, concise question stem that presents a complex scenario or concept
    - 4 carefully crafted answer options where the correct answer requires deep understanding
    - One correct answer that is not immediately obvious
    - Distractors that are plausible but demonstrate common misconceptions

    For each MCQ, output a JSON object with the following fields:
    - 'topic': the topic name
    - 'subtopic': the subtopic name
    - 'question': the question stem
    - 'options': an array of 4 options labeled A, B, C, D
    - 'correct_answer': the letter of the correct option (A, B, C, or D)

    JSON Formatting Rules:
    1. Do NOT include trailing commas in arrays or objects
    2. Each option in the 'options' array should be a complete string
    3. The 'options' array should have exactly 4 items
    4. The 'correct_answer' should be a single letter (A, B, C, or D)
    5. String Formatting Rules:
       - Use double quotes for all strings
       - Escape any double quotes within strings with a backslash: \\"
       - Do not use any other escape sequences
       - Do not include newlines within strings
       - Keep all text on a single line

    Example of correct options array format:
    "options": [
        "A. First option text",
        "B. Second option text",
        "C. Third option text",
        "D. Fourth option text"
    ]

    Return the entries as a JSON array of 3 objects.
    DO NOT include any markdown code block markers in the response.
    """

SYSTEM_MESSAGE = "You are a cybersecurity expert specialized in healthcare security and medical device security. Your expertise includes deep knowledge of medical device vulnerabilities, healthcare regulations, and complex security scenarios. Focus on generating challenging questions that test deep understanding rather than surface-level knowledge. Ensure all JSON output is strictly valid with proper string escaping and no trailing commas." 