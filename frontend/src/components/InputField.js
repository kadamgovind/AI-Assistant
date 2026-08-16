import React from "react";

function InputField({ type, placeholder, value, onChange }) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      style={{
        width: "100%",
        padding: "10px",
        margin: "10px 0",
        borderRadius: "8px",
        border: "1px solid #ccc",
      }}
    />
  );
}

export default InputField;