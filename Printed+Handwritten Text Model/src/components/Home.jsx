import React from 'react';
import { Box } from '@mui/material';
import ImageUpload from '../components/ImageUpload';
import ResultsDisplay from '../components/ResultsDisplay';

const Home = () => {
  return (
    <div className="text-center">
      <h2 className="text-3xl font-bold mb-4">Home Page</h2>
      <p className="text-lg">Welcome to the Image Processor App. Use the navigation to explore more.</p>
    </div>
  );
};

export default Home;

