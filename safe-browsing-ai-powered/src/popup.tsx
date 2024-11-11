import { useState } from "react"

import Login from "~components/login/login";
import SignUp from "~components/signUp/signUp";

function IndexPopup() {
  const [showSignUp, setShowSignUp] = useState<boolean>(false); // Toggle state for SignUp

  const toggleSignUp = () => {
    setShowSignUp(!showSignUp); // Toggle between SignUp and Login
  };

  return (
    <div style={{
      padding: 16,
      maxWidth: '400px',
      width:'398px',
      textAlign: 'center',
      height:'0px',
      backgroundColor: 'transparent'
    }}>
      <h3>SAFE BROWSING POWERED BY AI Extension!</h3>
      <div style={{ margin: '16px 0' }}>
        {showSignUp ? (
          <>
            <h4>Create a New Account</h4>
            <SignUp />
            <button onClick={toggleSignUp} style={{ marginTop: 8 }}>
              Already have an account? Login
            </button>
          </>
        ) : (
          <>
            <h4>Login to Your Account</h4>
            <Login />
          </>
        )}
      </div>
    </div>
  );
}

export default IndexPopup
