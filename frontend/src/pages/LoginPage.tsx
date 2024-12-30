// src/pages/LoginPage.tsx
import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import SignupModal from "../components/SignupModal";
import "../assets/LoginPage.css";

const LoginPage = () => {
    const [isSignupOpen, setSignupOpen] = useState(false);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const navigate = useNavigate();

    const openSignupModal = () => setSignupOpen(true);
    const closeSignupModal = () => setSignupOpen(false);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://localhost:5000/auth/login", { username, password });
            const { access_token } = response.data;

            // Save token and username to localStorage (or context)
            localStorage.setItem("token", access_token);
            localStorage.setItem("username", username);

            // Redirect to account page
            navigate("/account");
        } catch (error) {
            console.error("Login failed:", error);
            setErrorMessage("Invalid username or password. Please try again.");
        }
    };

    return (
        <div className="login">
            <h1>Login</h1>
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Login</button>
                {errorMessage && <p className="error-message">{errorMessage}</p>}
                <div>
                    <a href="#" onClick={openSignupModal}>
                        Don't have an account? Sign up now!
                    </a>
                </div>
            </form>
            <SignupModal isOpen={isSignupOpen} onClose={closeSignupModal} onSignup={() => {}} />
        </div>
    );
};

export default LoginPage;
