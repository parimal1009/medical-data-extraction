import React, { useState, useCallback, useRef } from 'react';
import { Button, LinearProgress, Box, Typography, Paper, Snackbar } from '@mui/material';
import { styled } from '@mui/material/styles';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import ContentPasteIcon from '@mui/icons-material/ContentPaste';

const UploadArea = styled(Paper)(({ theme, isDragActive }) => ({
  padding: theme.spacing(3),
  textAlign: 'center',
  cursor: 'pointer',
  backgroundColor: isDragActive ? theme.palette.action.hover : theme.palette.background.paper,
  border: `2px dashed ${isDragActive ? theme.palette.primary.main : theme.palette.divider}`,
  borderRadius: theme.shape.borderRadius,
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    backgroundColor: theme.palette.action.hover,
  },
}));

const Input = styled('input')({
  display: 'none',
});

const StyledButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(1),
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[4],
  },
  transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
}));

function ImageUpload({ onUpload, isProcessing, progress }) {
  const [isDragActive, setIsDragActive] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const uploadAreaRef = useRef(null);

  const handleDragEnter = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
    const files = Array.from(e.dataTransfer.files);
    onUpload(files);
  }, [onUpload]);

  const handleFileChange = useCallback((event) => {
    const files = Array.from(event.target.files);
    onUpload(files);
  }, [onUpload]);

  const handlePaste = useCallback(async () => {
    try {
      const clipboardItems = await navigator.clipboard.read();
      const imageFiles = [];

      for (const item of clipboardItems) {
        for (const type of item.types) {
          if (type.startsWith('image/')) {
            const blob = await item.getType(type);
            imageFiles.push(new File([blob], `pasted-image-${Date.now()}.png`, { type }));
          }
        }
      }

      if (imageFiles.length > 0) {
        onUpload(imageFiles);
      } else {
        setSnackbarMessage('No image found in clipboard');
        setSnackbarOpen(true);
      }
    } catch (error) {
      console.error('Failed to read clipboard contents: ', error);
      setSnackbarMessage('Failed to paste image. Please try copying the image again.');
      setSnackbarOpen(true);
    }
  }, [onUpload]);

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  return (
    <Box sx={{ textAlign: 'center' }}>
      <Input
        accept="image/*"
        id="raised-button-file"
        multiple
        type="file"
        onChange={handleFileChange}
        disabled={isProcessing}
      />
      <UploadArea
        ref={uploadAreaRef}
        isDragActive={isDragActive}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onPaste={handlePaste}
        tabIndex={0}
      >
        <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
        <Typography variant="h6" gutterBottom>
          Drag & Drop Images Here
        </Typography>
        <Typography variant="body2" color="textSecondary" paragraph>
          Or use the options below
        </Typography>
        <Box>
          <label htmlFor="raised-button-file">
            <StyledButton
              variant="contained"
              component="span"
              startIcon={<FileUploadIcon />}
              disabled={isProcessing}
            >
              Browse
            </StyledButton>
          </label>
          <StyledButton
            variant="contained"
            startIcon={<ContentPasteIcon />}
            onClick={handlePaste}
            disabled={isProcessing}
          >
            Paste
          </StyledButton>
        </Box>
      </UploadArea>
      {isProcessing && (
        <Box sx={{ mt: 2, width: '100%', maxWidth: 400, mx: 'auto' }}>
          <LinearProgress 
            variant="determinate" 
            value={progress * 100} 
            sx={{ height: 8, borderRadius: 4 }}
          />
          <Typography variant="body2" sx={{ mt: 1, color: 'text.secondary' }}>
            {`${Math.round(progress * 100)}% Processed`}
          </Typography>
        </Box>
      )}
      <Snackbar
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        message={snackbarMessage}
      />
    </Box>
  );
}

export default ImageUpload;