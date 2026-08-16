import React, { useState, useRef, useEffect } from "react";

function ChatBox() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  // ✅ Auto scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat, loading]);

  // ✅ Send message
  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMsg = { sender: "user", text: message };

    // Update UI immediately
    setChat((prev) => [...prev, userMsg]);
    setMessage("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: 1,
          message: message,
        }),
      });

      // ✅ Handle bad response
      if (!res.ok) {
        throw new Error("Server error");
      }

      const data = await res.json();

      const botMsg = {
        sender: "bot",
        text: data.response || "No response from AI",
      };

      setChat((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error("Error:", error);

      setChat((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "⚠️ Error connecting to backend",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // ✅ Enter key support
  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !loading) {
      sendMessage();
    }
  };

  return (
    <div style={{ width: "350px", marginTop: "20px" }}>
      <h2>🤖 Aira Chat</h2>

      {/* Chat Box */}
      <div
        style={{
          border: "1px solid #ccc",
          padding: "10px",
          height: "400px",
          overflowY: "auto",
          borderRadius: "10px",
          background: "#f9f9f9",
        }}
      >
        {chat.map((msg, index) => (
          <div
            key={index}
            style={{
              display: "flex",
              justifyContent:
                msg.sender === "user" ? "flex-end" : "flex-start",
              marginBottom: "8px",
            }}
          >
            <div
              style={{
                padding: "10px",
                borderRadius: "15px",
                maxWidth: "70%",
                background:
                  msg.sender === "user" ? "#4CAF50" : "#e0e0e0",
                color: msg.sender === "user" ? "white" : "black",
                wordWrap: "break-word",
              }}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {/* Typing Indicator */}
        {loading && (
          <p style={{ fontSize: "12px", color: "gray" }}>
            Aira is typing...
          </p>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Input Area */}
      <div style={{ marginTop: "10px", display: "flex" }}>
        <input
          type="text"
          placeholder="Type your message..."
          value={message}
          disabled={loading}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyPress}
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            outline: "none",
          }}
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          style={{
            marginLeft: "10px",
            padding: "10px 15px",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#4CAF50",
            color: "white",
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatBox;