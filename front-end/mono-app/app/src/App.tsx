import React from 'react';
import { CustomButton } from '@monorepo/reusable-components';
import { ThemeProvider, createTheme } from '@mui/material';

const theme = createTheme();

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <h1>Hello World</h1>
        <CustomButton 
          label="Click me!" 
          onClick={() => alert('Button clicked!')}
        />
      </div>
    </ThemeProvider>
  );
}

export default App; 