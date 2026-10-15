async function invokeAzureModel(payload) {
  const response = await fetch('/api/azure', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok)
    throw new Error(data.error || `Error del servicio (${response.status}).`);
  return data;
}

const defaultSystemPrompt = 'Eres un asistente de inteligencia artificial. Responde en el idioma del usuario de forma clara, concisa y estructurada.';

export function createAzureChatClient(systemPrompt = defaultSystemPrompt) {
  return {
    send : async function(userText, options = {}) {
      return handleUserPrompt(userText, options, systemPrompt);
    }
  };
}

async function handleUserPrompt(userText, options = {}, systemPrompt) {
  const messages = [
    { 
      role: 'system', 
      content: systemPrompt 
    },
    ...(options.messages || []).filter(message => ['user', 'assistant'].includes(message.role)),
    { role: 'user', content: userText }
  ];
  const payload = { messages, temperature: 0.1 };

  if (options.model) payload.model = options.model;

  try {
    const response = await invokeAzureModel(payload);
    if (typeof response?.content === 'string' && response.content.trim()) return response.content;
    return { error: 'Azure AI devolvió una respuesta vacía o inesperada.' };
  } catch (error) {
    console.error('rcg.ai.azure.handleUserPrompt Error:', error);
    return { error: `Error procesando la petición: ${error.message}` };
  }
}
