from __future__ import annotations

import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PERSONAS: dict[str, str] = {
    "positivo": "Você é um assistente entusiasmado 😄 que celebra cada conquista do aluno.",
    "neutro": "Você é um assistente acadêmico formal e direto.",
    "negativo": "Você é um assistente empático, focado em acalmar o usuário em situação de stress.",
}

SYSTEM_PROMPT = (
    "Classifique o sentimento da mensagem do usuário em positivo, neutro ou negativo. "
    "Retorne apenas uma destas palavras, sem pontuação extra."
)


def select_persona(user_msg: str) -> str:
    resp = cliente.chat.completions.create(
        model="gpt-3.5-turbo-0125",  
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0,
    )
    sentiment = resp.choices[0].message.content.strip().lower()
    return sentiment if sentiment in PERSONAS else "neutro"