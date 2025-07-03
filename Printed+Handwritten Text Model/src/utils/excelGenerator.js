// File: src/utils/excelGenerator.js
import * as XLSX from 'xlsx';

export const generateExcel = (data) => {
  const worksheet = XLSX.utils.json_to_sheet(data.map(item => ({
    'File Name': item.file_name,
    'Extracted Diagnosis': item.extracted_diagnosis,
    'Corrected Diagnosis': item.corrected_diagnosis,
    'Processing Status': item.processing_status
  })));

  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Extraction Results");

  XLSX.writeFile(workbook, "extraction_results.xlsx");
};