import React, { useState } from "react";
import { TextField, Button, Box, Typography } from "@mui/material";

const Login = ({ onLogin }) => {
    const [username, setUsername] = useState("asirin");
    const [password, setPassword] = useState("asirin");
    const [error, setError] = useState("");

    const defaultPassword = "asirin";

    const users = [
        {
            "username": "asirin_kanat",
            "password": defaultPassword,
            "title": "Kanat"
        },
        {
            "username": "asirin_govde",
            "password": defaultPassword,
            "title": "Gövde"
        },
        {
            "username": "asirin_kuyruk",
            "password": defaultPassword,
            "title": "Kuyruk"
        },
        {
            "username": "asirin_aviyonik",
            "password": defaultPassword,
            "title": "Aviyonik"
        },
        {
            "username": "asirin_montaj",
            "password": defaultPassword,
            "title": "Montaj"
        },
    ]

    const loginFunc = async (data) => {
        try {
            const response = await fetch("http://localhost:8000/api/custom-token/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                localStorage.setItem('access_token', result.access);
                onLogin(result); 
            } else {
                setError(result.detail || "Giriş başarısız!");
            }
        } catch (error) {
            setError("Bir hata oluştu.");
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const data = { username, password };
        await loginFunc(data);
    };

    return (
        <Box sx={{ minWidth: 300, padding: 3, textAlign: "center", border: "1px solid #ccc", borderRadius: 2 }}>
            <Typography variant="h5" gutterBottom>Giriş Yap</Typography>
            <form onSubmit={handleSubmit}>
                <TextField
                    label="Kullanıcı Adı"
                    variant="standard"
                    fullWidth
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    margin="normal"
                />
                <TextField
                    label="Şifre"
                    variant="standard"
                    type="password"
                    fullWidth
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    margin="normal"
                />
                <Button type="submit" variant="contained" color="primary" fullWidth>
                    Giriş Yap
                </Button>
                {error && <Typography color="error" variant="body2" sx={{ mt: 1 }}>{error}</Typography>}
            </form>
            <Box sx={{ display: "flex", justifyContent: "space-between", m: 2 }}>
                {users.map((item, index) => (
                    <Button
                        key={index}
                        variant="contained"
                        size="small"
                        sx={{ m: 2 }}
                        onClick={() => loginFunc({ "username": item.username, "password": item.password })}
                        color="secondary"
                    >
                        {item.title} Personeli Olarak Giriş Yap
                    </Button>
                ))}
            </Box>
        </Box>
    );
};

export default Login;
