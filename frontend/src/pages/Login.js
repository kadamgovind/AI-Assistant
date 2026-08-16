import React, { useState } from "react";
import InputField from "../components/InputField";
import { loginUser } from "../services/api";
import { useNavigate, Link } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    if (e) e.preventDefault();

    // 🔐 Validation
    if (!form.email || !form.password) {
      alert("Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      const res = await loginUser(form);

      console.log("LOGIN RESPONSE:", res);

      // ✅ SUCCESS CASE
      if (res?.access_token) {
        // store token
        localStorage.setItem("token", res.access_token);

        alert("Login Success ✅");

        // 🔥 IMPORTANT FIX: route must match App.js
        navigate("/home");   // ✅ FIXED HERE
      } else {
        alert(res?.detail || "Invalid credentials ❌");
      }

    } catch (error) {
      console.error("Login Error:", error);
      alert("Server error ❌");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2>Login</h2>

      <InputField
        type="email"
        placeholder="Enter Email"
        value={form.email}
        onChange={(e) =>
          setForm({ ...form, email: e.target.value })
        }
      />

      <InputField
        type="password"
        placeholder="Enter Password"
        value={form.password}
        onChange={(e) =>
          setForm({ ...form, password: e.target.value })
        }
      />

      <button
        onClick={handleLogin}
        disabled={loading}
        style={styles.button}
      >
        {loading ? "Logging in..." : "Login"}
      </button>

      <p style={{ marginTop: "10px" }}>
        Don't have an account?{" "}
        <Link to="/signup">Signup</Link>
      </p>
    </div>
  );
}

const styles = {
  container: {
    width: "320px",
    margin: "100px auto",
    textAlign: "center",
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "10px",
    boxShadow: "0 0 10px rgba(0,0,0,0.1)",
  },
  button: {
    marginTop: "10px",
    padding: "10px",
    width: "100%",
    cursor: "pointer",
  },
};

export default Login;