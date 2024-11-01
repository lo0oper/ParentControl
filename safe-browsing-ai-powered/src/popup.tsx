import { useState } from "react"

import Login from "~components/login/login";

function IndexPopup() {
  const [loggedIn, setLoggedId] = useState<boolean>(false);
  const [disableCustomTheme, setDisableCustomTheme] = useState<boolean>(false);
  return (
    <div style={{
      padding: 16
    }}>
      <h2>
        SAFE BROWSING POWERED BY AI Extension!
      </h2>
      <h1>
        <Login/>
      </h1>
    </div>

  )
}

export default IndexPopup
