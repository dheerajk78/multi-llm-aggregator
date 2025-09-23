import React, { useState } from "react";
import Chat from "./Chat";
import Login from "./Login";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [token, setToken] = useState(null);

  const handleLogin = (jwt) => {
    localStorage.setItem("token", jwt);
    setToken(jwt);
    setLoggedIn(true); // explicitly mark user as logged in
  };

  return (
    <>
      {!loggedIn ? (
        <Login onLoginSuccess={handleLogin} />
      ) : (
        <Chat token={token} />
      )}
    </>
  );
}

export default App;

