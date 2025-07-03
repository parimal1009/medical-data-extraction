import React from 'react';
import { Typography } from '@mui/material';

const About = () => {
  return (
    <div>
      <Typography variant="h4" component="h2">
        About This App
      </Typography>
      <Typography variant="body1">
        This is a simple image processing app built with React and Material UI.
      </Typography>
    </div>
  );
};

export default About;
