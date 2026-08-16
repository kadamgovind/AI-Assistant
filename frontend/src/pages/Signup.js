import React, { useState } from "react";
import InputField from "../components/InputField";
import { signupUser } from "../services/api";
import { useNavigate, Link } from "react-router-dom";

function Signup() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);

  const handleSignup = async (e) => {
    if (e) e.preventDefault();

    // ✅ Validation
    if (!form.name || !form.email || !form.password) {
      alert("Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      const res = await signupUser(form);

      console.log("SIGNUP RESPONSE:", res);

      // ✅ SUCCESS CASE
      if (res?.message) {
        alert("Signup Successful ✅");

        // 🔥 IMPORTANT: auto login feel dene ke liye token set
        if (res?.access_token) {
          localStorage.setItem("token", res.access_token);
        } else {
          // fallback (temporary dev mode)
          localStorage.setItem("token", "logged_in");
        }

        // 🔥 FIX: must match App.js route
        navigate("/home");   // ✅ HOME PAGE OPEN
      } else {
        alert(res?.error || res?.detail || "Signup failed ❌");
      }

    } catch (error) {
      console.error("Signup Error:", error);
      alert("Server error ❌");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2>Signup</h2>

      <InputField
        type="text"
        placeholder="Enter Name"
        value={form.name}
        onChange={(e) =>
          setForm({ ...form, name: e.target.value })
        }
      />

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
        onClick={handleSignup}
        disabled={loading}
        style={styles.button}
      >
        {loading ? "Creating Account..." : "Signup"}
      </button>

      <p style={{ marginTop: "10px" }}>
        Already have an account?{" "}
        <Link to="/login">Login</Link>   {/* ✅ FIXED LINK */}
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

export default Signup;