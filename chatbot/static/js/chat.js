document.addEventListener('DOMContentLoaded', () => {
  const chat = document.getElementById('chat');
  const input = document.getElementById('input');
  const send = document.getElementById('send-btn');
  const AGENT = 'meu_agente';

  const add = (txt, bot = false) => {
    const p = document.createElement('p');
    p.className = `chat__bubble ${bot ? 'chat__bubble--bot' : 'chat__bubble--user'}`;
    p.textContent = txt;
    chat.appendChild(p);
    chat.scrollTop = chat.scrollHeight;
    return p;
  };

  const phaseSteps = [
    { label: 'Interpretando a pergunta', ms: 1600 },
    { label: 'Buscando informações', ms: 3600 },
    { label: 'Avaliando resposta', ms: 3600 }
  ];

  async function sendMsg() {
    const text = input.value.trim();
    if (!text) return;
    add(text, false);
    input.value = '';

    let phase = 0, dots = 0;
    const loader = add(`${phaseSteps[0].label} .`, true);

    const dotLoop = setInterval(() => {
      dots = (dots + 1) % 4;
      const ellipsis = '.'.repeat(dots);
      const label = phase < phaseSteps.length ? phaseSteps[phase].label : 'Estruturando saída';
      loader.textContent = `${label} ${ellipsis}`;
    }, 350);

    const phaseLoop = setInterval(() => {
      phase += 1;
      if (phase >= phaseSteps.length) clearInterval(phaseLoop);
    }, phaseSteps[phase].ms);

    try {
      const resp = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ msg: text, agent: AGENT })
      });
      const data = await resp.json();
      clearInterval(dotLoop);
      clearInterval(phaseLoop);

      const finalMsg = data.answer || data.error || 'Resposta vazia.';
      loader.textContent = finalMsg;

      const erroPDF = 'Apague agents.json para recriar o assistente com o novo PDF.';
      const newBotClass = finalMsg.trim() === erroPDF
        ? 'chat__bubble--bot--error'
        : 'chat__bubble--bot';

      loader.className = `chat__bubble ${newBotClass}`;

    } catch {
      clearInterval(dotLoop);
      clearInterval(phaseLoop);
      loader.textContent = 'Falha de conexão.';
    }
  }

  send.addEventListener('click', sendMsg);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') sendMsg(); });
});
