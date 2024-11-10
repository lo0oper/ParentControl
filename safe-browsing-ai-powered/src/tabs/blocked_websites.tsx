import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { Storage } from "@plasmohq/storage"
import { ACTIONS } from '../constants/constant';
import { SecureStorage } from '@plasmohq/storage/secure';
 
const secureStorage = new SecureStorage({ area: "local" })
const storage = new Storage({
  copiedKeyList: ["shield-modulation"]
})

const BlockedWebsites: React.FC = () => {
  const [blockedWebsites, setBlockedWebsites] = useState<string[]>([]);
  const [newWebsite, setNewWebsite] = useState<string>('');
  const [openErrorModal, setOpenErrorModal] = useState(false); // State for modal visibility
  const [errorMessage, setErrorMessage] = useState(''); // State for error message


  const addBlockedWebsite = (website_host: string) => {
    const userEmail = storage.get("email");
    console.log({"userEmail":userEmail});
    const data = {
      user_email: userEmail,
      banned_website: website_host
    };
    const action = ACTIONS.ADD_WEBSITE;
    chrome.runtime.sendMessage({ action, data }, (response) => {
      if (response.error) {
        setErrorMessage(response.error); // Set the error message
        setOpenErrorModal(true); // Open the error modal
      } else {
        console.log(`website :${data.banned_website} added successfully`)
      }
    });
  };



  // Load blocked websites from Chrome storage on component mount
  useEffect(() => {
    // chrome.runtime.sendMessage({ action, data }, (response) => {
    //   console.log({ 'response from background': response });
    //   console.log(response.sta)
    //   if (response.error) {
    //     setErrorMessage(response.error); // Set the error message
    //     setOpenErrorModal(true); // Open the error modal
    //   } else {
    //     setMessage('"Login" successful!');
    //     chrome.tabs.create({ url: chrome.runtime.getURL('tabs/blocked_websites.html') });
    //   }
    // });
    chrome.storage.sync.get('blockedWebsites', (result) => {
      setBlockedWebsites(result.blockedWebsites || []);
    });
  }, []);

  // Add a new website to the blocked list
  const handleAddWebsite = () => {
    if (newWebsite.trim() === '') return;

    const updatedWebsites = [...blockedWebsites, newWebsite];
    addBlockedWebsite(newWebsite);
    chrome.storage.sync.set({ blockedWebsites: updatedWebsites }, () => {
      setBlockedWebsites(updatedWebsites);
      setNewWebsite('');
    });
  };

  // Remove a website from the blocked list
  const handleRemoveWebsite = (website: string) => {
    const updatedWebsites = blockedWebsites.filter((w) => w !== website);
    chrome.storage.sync.set({ blockedWebsites: updatedWebsites }, () => {
      setBlockedWebsites(updatedWebsites);
    });
  };

  return (
    <Container maxWidth="md" style={{ marginTop: '2rem' }}>
      <Typography variant="h4" gutterBottom>
        Blocked Websites
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Website</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {blockedWebsites.map((website) => (
              <TableRow key={website}>
                <TableCell>{website}</TableCell>
                <TableCell align="right">
                  <IconButton
                    color="secondary"
                    onClick={() => handleRemoveWebsite(website)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleAddWebsite();
        }}
        style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}
      >
        <TextField
          label="Enter website URL"
          variant="outlined"
          fullWidth
          value={newWebsite}
          onChange={(e) => setNewWebsite(e.target.value)}
        />
        <Button type="submit" variant="contained" color="primary">
          Add Website
        </Button>
      </form>
    </Container>
  );
};

export default BlockedWebsites;
