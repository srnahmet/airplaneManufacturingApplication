import { Box, Button, Tab, Tabs, } from '@mui/material'
import React, { useEffect, useState } from 'react'
import MUIDataTable from "mui-datatables";
import { language } from '../../../utils/dataTableOptions';
import DeleteIcon from '@mui/icons-material/Delete';
import { fetchWithAuth } from '../../../utils/fetchHelper';

function TeamPage({ userInfo }) {

  // tab
  const [tabValue, setTabValue] = useState(userInfo?.employee?.team_id?.toString() || "1");
  const [tabs, setTabs] = useState([]);

  const [data, setData] = useState([]);
  const [totalRecords, setTotalRecords] = useState(0);
  const [loading, setLoading] = useState(false);

  const [airplanes, setUavs] = useState([]);

  const [parts, setParts] = useState([]);

  const fetchPartData = async (newTabValue = null) => {
    setLoading(true);
    const team = newTabValue ? newTabValue : tabValue;
    try {
      const response = await fetchWithAuth(`http://127.0.0.1:8000/api/parts-by-team-id/?team_id=${team}`);
      const data = await response;
      setParts(data.map(item => [item?.id, item?.airplane_type_name?.name, item?.create_date?.split('T')?.[0]]));
    } catch (error) {
      console.log(error.message);
    } finally {
      setLoading(false);
    }

  };

  const fetchData = async (newTabValue = null) => {
    setLoading(true);
    const team = newTabValue ? newTabValue : tabValue;
    fetch(`http://127.0.0.1:8000/api/employees/${team}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setData(data.map((item) => [
          item.name,
          item.team_name.name,
        ]));
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      }).finally(() => setLoading(false));
  };

  const fetchTeamInfo = () => {
    setLoading(true)
    fetch('http://127.0.0.1:8000/api/teams-list/')
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

  const handleDeletePart = async (partId) => {
    setLoading(true);
    try {
      const response = await fetchWithAuth(`http://127.0.0.1:8000/api/parts-by-id/${partId}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          // Authorization gibi ek başlıklar gerekiyorsa burada tanımlanabilir
          // 'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Silme işlemi başarısız oldu');
      }
    } catch (error) {
      console.log(error.message);
    } finally {
      setLoading(false);
      handleTabValueChange(null,tabValue);
    }
  };

  // Tablo ayarları
  const options = {
    count: totalRecords,
    rowsPerPage: 10,
    rowsPerPageOptions: [10, 20, 50],
    selectableRows: "none",
    textLabels: language,
  };


  const handleTabValueChange = (event, newValue) => {
    setTabValue(newValue);
    fetchData(newValue);
    fetchPartData(newValue);
  };


  useEffect(() => {
    console.log(userInfo)
    fetchTeamInfo();
    fetchData();
    fetchPartData();
  }, []);

  const partColumns = [
    {
      name: "#",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "Uçak",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "Oluşturulma Tarihi",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "",
      options: {
        filter: true,
        sort: true,
        customBodyRender: (value, tableMeta) => {
          return (
            <Button color='error' onClick={()=>handleDeletePart(tableMeta?.rowData?.[0])} endIcon={<DeleteIcon />}>Geri Dönüşüm Talebi</Button>
          );
        },
      },
    },
  ];
  


  return (
    <Box>
      <Box sx={{ width: '100%', borderBottom: 1, borderColor: 'divider', p: 2 }} >
        <Tabs
          variant="fullWidth"
          onChange={handleTabValueChange}
          value={tabValue}
            textColor="warning"
            indicatorColor="primary"
        >
          {
            tabs.map((tab) => {
              if (userInfo.isAdmin || userInfo?.team?.part_type_id?.toString() === tab?.id?.toString() ) return (<Tab label={<div>{tab?.name}  <div>{" (" + tab?.employee_count + " Çalışan)"}</div></div>} value={tab?.id} />)
            })
          }
        </Tabs>
      </Box>

      <MUIDataTable
        title={tabs.filter(tab => tab.id?.toString() === tabValue?.toString())?.[0]?.name + " Personelleri"}
        data={data}
        columns={columns}
        options={options}
      />
      {userInfo?.employee?.team_id !== 5 && <MUIDataTable
        title={"Takıma Bağlı Parçalar"}
        data={parts}
        columns={partColumns}
        options={options}
      />}
    </Box>
  )
}

export default TeamPage


const columns = [
  {
    name: "Ad",
    options: {
      filter: true,
      sort: true,
    },
  },
  {
    name: "Takım",
    options: {
      filter: true,
      sort: true,
    },
  },

];



