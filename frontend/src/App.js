import React, { useState } from "react";
import { Box, CssBaseline, Container, Typography } from "@mui/material";
import Login from "./components/login";
import Home from "./components/home";
import { ThemeProvider, createTheme } from "@mui/material/styles";

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userInfo, setUserInfo] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);

  const handleLogin = (result) => {
    setUserInfo({ ...result, isAdmin: result?.employee?.id === 1 });
    setIsAuthenticated(true); // Giriş yapıldığında ana sayfaya geçiş
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main">
        <CssBaseline />

        {!isAuthenticated ? (
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              marginTop: "15%",
            }}
          >
            <Typography variant="h2" color="primary" gutterBottom>
              UÇAK ÜRETİM UYGULAMASI
            </Typography>
            <Login onLogin={handleLogin} />
          </Box>
        ) : (
          <Home userInfo={userInfo} />
        )}
      </Container>
    </ThemeProvider>
  );
};

export default App;

const theme = createTheme({
  palette: {
    primary: {
      main: "#000000",
      light: "#4f4f4f",
      dark: "#121212",
      contrastText: "#ffffff",
    },
    secondary: {
      main: "#ffffff",
      light: "#f1f1f1",
      dark: "#b0b0b0",
      contrastText: "#000000",
    },
    background: {
      default: "#f4f6f8",
      paper: "#ffffff",
    },
    text: {
      primary: "#000000",
      secondary: "#6c757d",
    },
  },
});

// const fetchData = async () => {
//   try {
//     const response = await fetch("http://localhost:8000/api/protected/", {
//       method: "GET",
//       headers: {
//         Authorization: `Bearer ${accessToken}`,
//       },
//     });

//     const data = await response.json();
//     if (response.ok) {
//       console.log("Veri:", data);
//     } else {
//       console.error("API hatası:", data);
//     }
//   } catch (error) {
//     console.error("Veri çekme hatası:", error);
//   }
// };
