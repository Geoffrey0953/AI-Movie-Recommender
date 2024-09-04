import React from "react";
import Form from "../components/Form";
import { useNavigate } from "react-router-dom";

function Login() {
    const navigate = useNavigate();

    const handleRegisterRedirect = () => {
        navigate("/register");
    };

    return (
        <div>
            <Form route="/api/token/" method="login" />
            <button 
                onClick={handleRegisterRedirect} 
                style={{ marginTop: '20px', padding: '10px 20px', cursor: 'pointer' }}>
                Don't have an account? Register
            </button>
        </div>
    );
}

export default Login;
