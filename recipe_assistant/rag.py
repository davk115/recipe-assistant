import ingest
from openai import OpenAI

client = OpenAI()

index = ingest.load_index()

def search(query):
    boost = {
        'recipe_name': 4.53,
        'cuisine_type': 0.08,
        'ingredients': 1.77,
        'cooking_instructions': 2.12,
        'dietary_preferences': 2.45,
        'difficulty': 4.78
    }

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results

prompt_template = """
You're a chef. Answer the QUESTION based on the CONTEXT from our exercises database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

entry_template = """
recipe_name: {recipe_name}
cuisine_type: {cuisine_type}
ingredients: {ingredients}
cooking_instructions: {cooking_instructions}
dietary_preferences: {dietary_preferences}
difficulty: {difficulty}
""".strip()

def build_prompt(query, search_results):
    context = ""
    
    for doc in search_results:
        context = context + entry_template.format(**doc) + "\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(prompt, model='gpt-4o-mini'):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


def rag(query, model='gpt-4o-mini'):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt, model=model)
    return answer