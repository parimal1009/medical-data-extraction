import React from 'react';
import { Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Box, Chip } from '@mui/material';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import { generateExcel } from '../utils/excelGenerator';
import { styled } from '@mui/material/styles';

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  '&.MuiTableCell-head': {
    backgroundColor: theme.palette.primary.dark,
    color: theme.palette.common.white,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));

const StyledButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(2),
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[4],
  },
  transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
}));

function ResultsDisplay({ results }) {
  const handleDownload = () => {
    generateExcel(results);
  };

  if (results.length === 0) return null;

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
        Extraction Results
      </Typography>
      <TableContainer component={Paper} sx={{ mb: 2, borderRadius: 2, overflow: 'hidden' }}>
        <Table>
          <TableHead>
            <TableRow>
              <StyledTableCell>File Name</StyledTableCell>
              <StyledTableCell>Extracted Diagnosis (Vision)</StyledTableCell>
              <StyledTableCell>Corrected Diagnosis (Gemini)</StyledTableCell>
              <StyledTableCell align="center">Processing Status</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {results.map((result, index) => (
              <StyledTableRow key={index}>
                <TableCell>{result.file_name}</TableCell>
                <TableCell>{result.extracted_diagnosis}</TableCell>
                <TableCell>{result.corrected_diagnosis}</TableCell>
                <TableCell align="center">
                  <Chip
                    icon={result.processing_status === 'Success' ? <CheckCircleIcon /> : <ErrorIcon />}
                    label={result.processing_status}
                    color={result.processing_status === 'Success' ? 'success' : 'error'}
                    variant="outlined"
                  />
                </TableCell>
              </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <StyledButton
        variant="contained"
        color="secondary"
        startIcon={<FileDownloadIcon />}
        onClick={handleDownload}
        size="large"
      >
        Download Excel
      </StyledButton>
    </Box>
  );
}

export default ResultsDisplay;