import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Typography, Box, Container, Paper } from '@mui/material';
import ImageUpload from '../components/ImageUpload';
import ResultsDisplay from '../components/ResultsDisplay';
import { processImages } from '../utils/imageProcessing';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#3f51b5',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
});

const Extract = () => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState([]);
  const [progress, setProgress] = useState(0);

  const handleImageUpload = async (files) => {
    setIsProcessing(true);
    setProgress(0);
    setResults([]);

    try {
      const processedResults = await processImages(files, 15, (progress) => {
        setProgress(progress);
      });
      setResults(processedResults);
    } catch (error) {
      console.error('Error processing images:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
            Extract Text from Images
          </Typography>
          
          <Paper elevation={3} sx={{ p: 3, mb: 4, bgcolor: 'background.paper', borderRadius: 2 }}>
            <ImageUpload onUpload={handleImageUpload} isProcessing={isProcessing} progress={progress} />
          </Paper>
          
          {results.length > 0 && (
            <Paper elevation={3} sx={{ p: 3, bgcolor: 'background.paper', borderRadius: 2 }}>
              <ResultsDisplay results={results} />
            </Paper>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
};

export default Extract;