from __future__ import annotations

from flask import request, jsonify
from . import api_bp
from ...services.openai_client import client
from ...services.agent_registry import get_or_create_agent, RecreateRequired
from ...services.persona_selector import select_persona, PERSONAS

STATUS_COMPLETED = "completed"


def _talk_to_assistant(user_msg: str, agent_name: str) -> str:
    agente = get_or_create_agent(agent_name)
    thread_id, assistant_id = agente["thread_id"], agente["assistant_id"]

    persona_text = PERSONAS[select_persona(user_msg)]
    client.beta.threads.messages.create(thread_id=thread_id, role="user", content=persona_text)
    client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_msg)

    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
    while run.status != STATUS_COMPLETED:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread_id).data
    return messages[0].content[0].text.value if messages else "Falha ao obter resposta."


@api_bp.route("/chat", methods=["POST"])
def chat_route():
    data = request.get_json(silent=True) or {}
    text = data.get("msg", "").strip()
    if not text:
        return jsonify(error="Mensagem vazia"), 400

    try:
        answer = _talk_to_assistant(text, data.get("agent", "general"))
        return jsonify(answer=answer)
    except RecreateRequired:
        return jsonify(error="Apague agents.json para recriar o assistente com o novo PDF.")
