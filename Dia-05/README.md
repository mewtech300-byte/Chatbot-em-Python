# Dia 05: Contexto e pensamento

Hoje , implementei a lógica de persistência de dados. Agora o chatbot consegue manter o contexto de uma conversa, permitindo interações mais naturais.

# O que mudou:
- **Adição de `cl.user_session`**: Utilizado para guardar o histórico de mensagens da sessão atual.
- **Implementação de `system_instruction`**: Aplicação de Prompt Engineering para definir a personalidade do assistente.
- **Tratamento da resposta**: Lógica para filtrar a saída do modelo e evitar repetições desnecessárias.
- ### 📸 Registro de Execução [Print que o bot lembrou meu nome...]
