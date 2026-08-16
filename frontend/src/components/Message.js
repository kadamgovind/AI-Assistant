function Message({ message }) {
  return (
    <div
      style={{
        textAlign: message.sender === "user" ? "right" : "left",
        margin: "5px 0",
      }}
    >
      <span
        style={{
          display: "inline-block",
          padding: "8px 12px",
          borderRadius: "10px",
          backgroundColor:
            message.sender === "user" ? "#007bff" : "#e5e5ea",
          color: message.sender === "user" ? "white" : "black",
        }}
      >
        {message.text}
      </span>
    </div>
  );
}

export default Message;