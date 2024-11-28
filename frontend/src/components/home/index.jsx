import * as React from 'react';
import Box from '@mui/material/Box';
import AppBarComponent from './appBarComponent';
import UawPage from './homePages/uawPage';
import TeamsPage from './homePages/teamsPage';
import PartsPage from './homePages/partsPage';


import { useState } from 'react';
import { Paper } from '@mui/material';

const Home = ({userInfo}) => {

  const [currentPage, setCurrentPage] = useState("uaw")

  const pages = [
    { id: "uaw", name: "Uçak Envanteri", desc: "İnsansız Hava Araçlarının listesi ve bilgileri" },
    { id: "teams", name: "Takımlar", desc: "Farklı takımlar ve görev dağılımlarının detayları" },
    { id: "parts", name: "Parça Üret ve Montajla", desc: "Montajda kullanılan bileşenler ve ekipmanlar" },
  ];

  return (
    <Box>
      <AppBarComponent pages={pages} currentPage={currentPage} setCurrentPage={setCurrentPage} userInfo={userInfo}/>

      <Box sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginTop: "15%",
      }}>
        <Paper elevation={3} sx={{width:"100%"}}>
          {currentPage === "uaw" && <UawPage />}
          {currentPage === "teams" && <TeamsPage userInfo={userInfo}/>}
          {currentPage === "parts" && <PartsPage userInfo={userInfo}/>}
        </Paper>
      </Box>
    </Box>
  );
}
export default Home;