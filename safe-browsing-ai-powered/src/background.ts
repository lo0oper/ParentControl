import { ACTIONS, API_URLS } from "~constants/constant";

// background.ts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log({"In background for Auth with request  and sender":request.action,sender})
    if (request.action === ACTIONS.SIGNUP) {
      signUp(request.data).then(response => sendResponse(response));
      return true; // Keep the message channel open for async response
    } else if (request.action === ACTIONS.LOGIN) {
        console.debug("BG in login")
      login(request.data).then(response => sendResponse(response));
      return true;
    }else{
        console.log("No action type found")
        console.log({"action":request.action})
    }
  });
  
  async function signUp(data: { email: string; password: string }) {
    try {
        console.log(`trying to signUp :${JSON.stringify(data)}`)
      const response = await fetch(API_URLS.SIGNUP, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      const result = await response.json();
      // Save token or user data if needed
      await chrome.storage.local.set({ token: result.token });
      return result;
    } catch (error) {
      return { error: error.message };
    }
  }
  
  async function login(data: { email: string; password: string }) {
    try {
      console.log(`trying to login :${JSON.stringify(data)}`)
      const response = await fetch(API_URLS.LOGIN, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      const result = await response.json();
      await chrome.storage.local.set({ token: result.token });
      return result;
    } catch (error) {
      return { error: error.message };
    }
  }
  