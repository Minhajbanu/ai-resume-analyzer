

import ollama

def analyze_with_llm(relevant_chunks, job_description, similarity_score):

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an expert HR recruiter and resume evaluator.

Your task is to compare the resume with the job description
and provide a structured professional evaluation.


Resume Relevant Sections:
{context}

Job Description:
{job_description}

Semantic Match Score: {round(similarity_score * 100, 2)}%

Provide:
1. Give an Overall Match Score (0-100).
2. List Missing Technical Skills.
3. List Missing Soft Skills.
4. Suggest 5 specific improvements to make the resume stronger.
5. Rewrite 2 resume bullet points in a more impactful way using quantified results.
6. Give a final hiring recommendation (Shortlist / Consider / Reject).

Be specific. Do not repeat the resume text.
"""

    response = ollama.chat(
        model="gemma3:4b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']