document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("chatbot-toggle");
  const chatBox = document.getElementById("chatbot-box");
  const input = document.getElementById("chatbot-text");
  const sendBtn = document.getElementById("chatbot-send");
  const messages = document.getElementById("chatbot-messages");

  toggleBtn.addEventListener("click", () => {
    chatBox.style.display = chatBox.style.display === "flex" ? "none" : "flex";
    chatBox.style.flexDirection = "column";
  });

  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  function addMessage(content, sender = "bot") {
    const msg = document.createElement("div");
    msg.classList.add(sender === "user" ? "chat-user" : "chat-bot");
    msg.textContent = content;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
  }

  function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    fetch("/api/chatbot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    })
      .then((res) => res.json())
      .then((data) => {
        addMessage(data.response, "bot");
      })
      .catch(() => {
        addMessage("Hubo un error al contactar al asistente.", "bot");
      });
  }
});
