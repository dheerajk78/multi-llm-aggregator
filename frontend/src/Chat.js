import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
const API_BASE = process.env.REACT_APP_API_BASE || "";

function Chat({ token, currentUser, onLogout }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [providers, setProviders] = useState([]);
  const [selectedProvider, setSelectedProvider] = useState("");
  const [selectedModel, setSelectedModel] = useState("");
  const [usage, setUsage] = useState(null);

  // Fetch providers + models from backend
  useEffect(() => {
    const fetchProviders = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/models`);
        const data = await res.json();
        setProviders(data.providers || []);

        if (data.providers.length > 0) {
          setSelectedProvider(data.providers[0].id);
          setSelectedModel(data.providers[0].default_model);
        }
      } catch (err) {
        console.error("Error fetching providers:", err);
      }
    };
    fetchProviders();
  }, []);

  useEffect(() => {
    if (selectedProvider) {
      loadUsageStats(selectedProvider);
    }
  }, [selectedProvider]);

  const loadUsageStats = async (providerId) => {
    try {
      const res = await fetch(`${API_BASE}/api/usage?provider=${providerId}`);
      const data = await res.json();

      if (data.error) {
        setUsage(`❌ Error: ${data.error}`);
      } else {
        setUsage(
          `Provider: ${data.provider} | Total Tokens: ${data.total_tokens} | Estimated Cost: $${data.estimated_cost_usd}`
        );
      }
    } catch (err) {
      setUsage(`❌ Error: ${err.message}`);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || !selectedProvider || !selectedModel) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const token = localStorage.getItem("token")
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json","Authorization": `Bearer ${token}` },
        body: JSON.stringify({
          provider: selectedProvider,
          model: selectedModel,
          message: input,
          user_id: currentUser || "test-user",
        }),
      });

      const data = await response.json();
      const assistantMessage = { role: "assistant", content: data.reply };
      setMessages((prev) => [...prev, assistantMessage]);
      loadUsageStats(selectedProvider);
    } catch (err) {
      console.error("Error sending message:", err);
      const errorMessage = {
        role: "assistant",
        content: `❌ Network error: ${err.message}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    }

    setInput("");
  };

  return (
    <div className="container mt-4" style={{ maxWidth: "700px" }}>
      <h3 className="text-center mb-4">Chat Assistant</h3>
<button className="btn btn-outline-danger btn-sm" onClick={onLogout}>
          Logout
        </button>
      {/* Provider + Model selection */}
      <div className="row mb-3">
        <div className="col">
          <label className="form-label">Provider</label>
          <select
            className="form-select"
            value={selectedProvider}
            onChange={(e) => {
              setSelectedProvider(e.target.value);
              const prov = providers.find((p) => p.id === e.target.value);
              if (prov) setSelectedModel(prov.default_model);
            }}
          >
            {providers.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name || p.id}
              </option>
            ))}
          </select>
        </div>
        <div className="col">
          <label className="form-label">Model</label>
          <select
            className="form-select"
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
          >
            {providers
              .find((p) => p.id === selectedProvider)
              ?.models.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.id}
                </option>
              ))}
          </select>
        </div>
      </div>

      {/* Chat messages */}
      <div
        className="border rounded p-3 mb-3"
        style={{ height: "60vh", overflowY: "auto", background: "#f8f9fa" }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-2 mb-2 rounded ${
              msg.role === "user"
                ? "bg-primary text-white text-end"
                : "bg-light text-dark text-start"
            }`}
          >
            {msg.content}
          </div>
        ))}
      </div>

      {/* Input box */}
      <div className="input-group mb-2">
        <input
          type="text"
          className="form-control"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button className="btn btn-primary" onClick={sendMessage}>
          Send
        </button>
      </div>

      {/* Usage stats */}
      <div className="mt-2 p-2 bg-light border rounded" id="usage-box">
        {usage || "Loading usage stats..."}
      </div>
    </div>
  );
}

export default Chat;

