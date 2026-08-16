import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import ChatBox from "../components/ChatBox";

function Home() {
  const navigate = useNavigate();

  const [messages, setMessages] = useState([]);
  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const streamRef = useRef(null);

  // 🔐 Get Token
  const token = localStorage.getItem("token");

  // 🚪 Logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  // 🎤 Start Recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      streamRef.current = stream;

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = handleStop;

      mediaRecorder.start();
      setRecording(true);
    } catch (err) {
      console.error(err);
      alert("🎤 Microphone permission denied");
    }
  };

  // 🛑 Stop Recording
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecording(false);

      // 🔥 Stop mic stream (IMPORTANT)
      streamRef.current?.getTracks().forEach((track) => track.stop());
    }
  };

  // 🔥 After Recording
  const handleStop = async () => {
    const blob = new Blob(audioChunksRef.current, { type: "audio/webm" });

    try {
      setLoading(true);

      // 🎤 Speech to Text
      const formData = new FormData();
      formData.append("file", blob, "voice.webm");

      const res1 = await fetch("http://127.0.0.1:8000/speech-to-text", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!res1.ok) throw new Error("Speech API error");

      const data1 = await res1.json();
      const userText = data1.text;

      if (!userText) {
        setLoading(false);
        return;
      }

      // 💬 Add user message
      setMessages((prev) => [
        ...prev,
        { sender: "user", text: userText },
      ]);

      // 🤖 AI Response
      const res2 = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: userText,
        }),
      });

      if (!res2.ok) throw new Error("Chat API error");

      const data2 = await res2.json();
      const botReply = data2.response || "No response from AI";

      // 💬 Add bot message
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: botReply },
      ]);

      // 🔊 Text-to-Speech
      const speech = new SpeechSynthesisUtterance(botReply);
      speech.lang = "en-US";

      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(speech);

    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "⚠️ Error processing voice request",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      
      {/* 🔝 Header */}
      <div style={styles.header}>
        <h1>🤖 AIRA Assistant</h1>
        <button onClick={handleLogout} style={styles.logoutBtn}>
          Logout
        </button>
      </div>

      {/* 💬 Chat UI */}
      <div className="chat-box">
        <ChatBox
          messages={messages}
          setMessages={setMessages}
          loading={loading}
        />

        {/* 🎤 Mic Button */}
        <button
          onClick={recording ? stopRecording : startRecording}
          className="mic-btn"
          disabled={loading}
        >
          {recording ? "🛑 Stop Recording" : "🎤 Start Recording"}
        </button>
      </div>
    </div>
  );
}

const styles = {
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "20px",
  },
  logoutBtn: {
    padding: "8px 15px",
    border: "none",
    borderRadius: "5px",
    background: "red",
    color: "#fff",
    cursor: "pointer",
  },
};

export default Home;