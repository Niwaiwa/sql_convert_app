import React, { useState } from 'react';
import { Button, TextField, Table, TableBody, TableCell, TableHead, TableRow, Pagination } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import RefreshIcon from '@mui/icons-material/Refresh';
import axios from 'axios';


type Data = {
  id: number;
  sql: string;
  converted_sql: string;
  hash_map: string;
};

export default function Home() {
  const [query, setQuery] = useState<string>('');
  const [result, setResult] = useState<string>('');
  const [dataList, setDataList] = useState<Data[]>([]);
  const [page, setPage] = useState<number>(1);
  const [totalCnt, setTotalCnt] = useState<number>(0);
  // const serverUrl = 'http://localhost:8000';
  const serverUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  const handleQuerySubmit = async () => {
    const requestData = JSON.stringify({ "sql": query })
    const response = await axios.post(`${serverUrl}/sql`, requestData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = response.data;
    setResult(data.result);
    refreshData();
  };

  const handlePageChange = (value: number) => {
    refreshData(value);
  };

  const handleRefresh = () => {
    refreshData();
  };

  const refreshData = async (page: number = 1) => {
    try {
      const requestUrl = `${serverUrl}/sql?page=${page}`
      const response = await axios.get(requestUrl);
      const data = response.data;
      setDataList(data.data);
      setTotalCnt(data.total);
      setPage(data.page);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div style={{ margin: '20px' }}>
      <div>
        <h2>Query Result:</h2>
        <p>{result}</p>
      </div>

      <div>
        <TextField
          label="SQL Query"
          variant="outlined"
          fullWidth
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button onClick={handleQuerySubmit} variant="contained" color="primary" style={{ marginTop: '10px' }}>
          Submit
        </Button>
      </div>

      <div style={{ marginTop: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <h2>Previous Data:</h2>
          <IconButton
            aria-label="close"
            color="inherit"
            sx={{ p: 0.5 }}
            onClick={handleRefresh}
          >
            <RefreshIcon />
          </IconButton>
        </div>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>SQL</TableCell>
              <TableCell>Converted SQL</TableCell>
              <TableCell>Hash Map</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {dataList.map((data) => (
              <TableRow key={data.id}>
                <TableCell>{data.id}</TableCell>
                <TableCell>{data.sql}</TableCell>
                <TableCell>{data.converted_sql}</TableCell>
                <TableCell>{data.hash_map}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <Pagination 
          count={Math.ceil(totalCnt / 10)}
          page={page} 
          defaultPage={1}
          onChange={(event, value) => handlePageChange(value)}
          style={{ marginTop: '10px', justifyContent: 'center' }}
        />
      </div>
    </div>
  );
}
