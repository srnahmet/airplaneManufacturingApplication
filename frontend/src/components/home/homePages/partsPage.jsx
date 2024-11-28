import React, { Fragment, useEffect, useState } from 'react'
import { Box, Button, Paper, Snackbar, Tab, Tabs, Typography, } from '@mui/material'
import { BarChart } from '@mui/x-charts/BarChart';
import CreatePartComponent from './partsPageCreatePart';
import { fetchWithAuth } from '../../../utils/fetchHelper';

function PartsPage({ userInfo }) {

  const [snackBarMessage, setSnackBarMessage] = useState("İşlem tamamlandı!");
  const [snackBarOpen, setSnackBarOpen] = useState(false);
  // tab
  const [tabValue, setTabValue] = useState(0);
  const [tabs, setTabs] = useState([]);

  const [partCounts, setPartCounts] = useState([]);
  const [partTypes, setPartTypes] = useState([]);

  const [loading, setLoading] = useState(false);
  const [missings, setMissings] = useState([]);


  const fetchParthData = (newValue = 0, draftPartyTypes = []) => {
    setLoading(true)
    fetch(`http://127.0.0.1:8000/api/parts-list-by-airplane-type-id-count/${newValue}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        const draft = partTypes.length > 0
          ? partTypes.map(item => data.filter(item2 => item2.part_type == item.id)?.[0]?.part_count)
          : draftPartyTypes.map(item => data.filter(item2 => item2.part_type == item.id)?.[0]?.part_count);
        setPartCounts(draft);

        const partTypeIds = data.map(item => item.part_type);
        const draftMissing = partTypes.filter(item => !partTypeIds.includes(item.id)).map(item => item.name);
        setMissings(draftMissing);
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      }).finally(() => setLoading(false));
  }

  const fetchAirplaneInfo = () => {
    setLoading(true)
    fetch('http://127.0.0.1:8000/api/airplane-types/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Hata');
        }
        return response.json();
      })
      .then(data => {
        setTabs(data)
      })
      .catch(error => {
        console.error('Error:', error);
      }).finally(() => setLoading(false));
  }

  const fetchPartTypeInfo = () => {
    setLoading(true)
    fetch('http://127.0.0.1:8000/api/part-types/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Hata');
        }
        return response.json();
      })
      .then(data => {
        setPartTypes(data);
        fetchParthData(0, data);
      })
      .catch(error => {
        console.error('Error:', error);
      }).finally(() => {
        setLoading(false);
      });
  }

  const handleTabValueChange = (event, newValue) => {
    setTabValue(newValue);
    fetchParthData(newValue);
  };

  const handleAssembly = async () => {
    setLoading(true);

    const queryParams = new URLSearchParams({
      airplane_type_id: tabValue,
    }).toString();

    try {
      const response = await fetchWithAuth(`http://127.0.0.1:8000/api/create-airplane/?${queryParams}`, {
        method: 'POST',
      });
      fetchParthData(tabValue);
    } catch (error) {
      setSnackBarMessage("Montaj Tamamlanamadı!")
      setSnackBarOpen(true);
      console.error('Error:', error);
    } finally {
      setSnackBarMessage("Montaj Tamamlandı!")
      setSnackBarOpen(true);
      setLoading(false);
    }
  };



  useEffect(() => {
    fetchAirplaneInfo();
    fetchPartTypeInfo();
  }, []);

  return (
    <Box>
      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        open={snackBarOpen}
        onClose={() => setSnackBarOpen(false)}
        message={snackBarMessage}
        key={0}
      />
      <Box>
        <Box sx={{ width: '100%', borderBottom: 1, borderColor: 'divider', p: 2 }} >
          <Tabs
            variant="fullWidth"
            onChange={handleTabValueChange}
            value={tabValue}
            textColor="warning"
            indicatorColor="primary"
          >
            <Tab label={"Tüm Envanter"} value={0} />
            {
              tabs.map((tab) => {
                return (<Tab label={tab?.name} value={tab?.id} />)
              })
            }
          </Tabs>
        </Box>

        <BarChart
          fullWidth
          xAxis={[{ scaleType: 'band', data: partTypes.map(item => item?.name) }]}
          series={[{ data: partCounts }]}
          height={300}
          borderRadius={25}
        />

        {tabValue > 0 && !userInfo?.team?.part_type_id &&
          <Button variant="contained" color="error" disabled={missings?.length > 0} fullWidth onClick={handleAssembly}>
            {
              missings?.length > 0 ? `Montajlanamaz (${missings.join(',')} Eksik!)` : "Montajla"}
          </Button>
        }
      </Box>
      {(userInfo?.team?.part_type_id || userInfo?.isAdmin) &&
        <Paper sx={{ p: 5, textAlign: "center" }}>
          <Typography variant="h5" gutterBottom>Parça Üret</Typography>
          <CreatePartComponent userInfo={userInfo} fetchParthData={fetchParthData} tabValue={tabValue} partTypes={partTypes} airplaneTypes={tabs} />
        </Paper>
      }
    </Box>
  )
}

export default PartsPage
