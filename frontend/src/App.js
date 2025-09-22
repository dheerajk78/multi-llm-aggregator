import React, { useState } from "react";
import Chat from "./Chat";
import Login from "./Login";

function App() {
  const [user, setUser] = useState(null);

  return (
    <div>
      {!user ? (
        <Login onLogin={setUser} />
      ) : (
        <Chat user={user} />
      )}
    </div>
  );
}

export default App;

