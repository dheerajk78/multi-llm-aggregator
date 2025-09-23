import React, { useState,useEffect } from "react";
import Chat from "./Chat";
import Login from "./Login";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [token, setToken] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);

  // ✅ Check localStorage on initial load
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedUser = localStorage.getItem("currentUser");
    if (savedToken && savedUser) {
      setToken(savedToken);
      setCurrentUser(savedUser);
      setLoggedIn(true);
    }
  }, []);
	
// Called after successful login
  const handleLogin = ({ jwt, username }) => {
    localStorage.setItem("token", jwt);
    localStorage.setItem("currentUser", username);
    setToken(jwt);
    setCurrentUser(username);
    setLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("currentUser");
    setToken(null);
    setCurrentUser(null);
    setLoggedIn(false);
  };
  return (
    <>
      {!loggedIn ? (
        <Login onLogin={handleLogin} />
      ) : (
        <Chat token={token} currentUser={currentUser} onLogout={handleLogout}  />
      )}
    </>
  );
}

export default App;

