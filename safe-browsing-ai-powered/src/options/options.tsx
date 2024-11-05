import React, { useState, useEffect } from 'react';

interface UserDetails {
  username: string;
  email: string;
  restrictedWebSites: string[];
}

function Options() {
  const [userDetails, setUserDetails] = useState<UserDetails>({
    username: '',
    email: '',
    restrictedWebSites: []
  });

  const [newRestrictedWebSites, setNewRestrictedWebSites] = useState<string>(''); 

  useEffect(() => {
    // Load saved details from Chrome storage on component load
    chrome.storage.sync.get(['userDetails'], (result) => {
      if (result.userDetails) {
        setUserDetails(result.userDetails);
      }
    });
  }, []);

  const handleAddRestrictedWebsite = () => {
    if (newRestrictedWebSites.trim()) {
      setUserDetails((prevDetails) => ({
        ...prevDetails,
        preferences: [...prevDetails.restrictedWebSites, newRestrictedWebSites.trim()],
      }));
      setNewRestrictedWebSites(''); // Clear input after adding
    }
  };

  const handleRemovePreference = (index: number) => {
    setUserDetails((prevDetails) => ({
      ...prevDetails,
      preferences: prevDetails.restrictedWebSites.filter((_, i) => i !== index),
    }));
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setUserDetails((prevDetails) => ({
      ...prevDetails,
      [name]: value,
    }));
  };

  const handleSave = () => {
    chrome.storage.sync.set({ userDetails }, () => {
      alert('Details saved successfully!');
    });
  };

  return (
    <div style={{ padding: '20px', maxWidth: '500px' }}>
      <h2>Your restricted WebSites</h2>
      <label>
        Username:
        <input
          type="text"
          name="username"
          value={userDetails.username}
          onChange={handleChange}
          style={{ display: 'block', marginBottom: '10px', width: '100%' }}
        />
      </label>
      <label>
        Email:
        <input
          type="email"
          name="email"
          value={userDetails.email}
          onChange={handleChange}
          style={{ display: 'block', marginBottom: '10px', width: '100%' }}
        />
      </label>
      <label>
        restrictedWebSites:
        <div>
          {userDetails.restrictedWebSites.map((preference, index) => (
            <div key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
              <span>{preference}</span>
              <button onClick={() => handleRemovePreference(index)} style={{ marginLeft: '10px' }}>
                Remove
              </button>
            </div>
          ))}
          <input
            type="text"
            value={newRestrictedWebSites}
            onChange={(e) => setNewRestrictedWebSites(e.target.value)}
            placeholder="Add the Website host that you want to restrict"
            style={{ width: '80%', marginRight: '5px' }}
          />
          <button onClick={handleAddRestrictedWebsite}>Add</button>
        </div>
      </label>
      <button onClick={handleSave}>Save</button>
    </div>
  );
}

export default Options;
