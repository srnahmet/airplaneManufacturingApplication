import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import AdbIcon from '@mui/icons-material/Adb';
import Logo from "./../../assets/images/srnahmet_logo.png"
import PersonIcon from '@mui/icons-material/Person';

const AppBarComponent = ({ pages, currentPage, setCurrentPage, userInfo }) => {
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);

  // const handleOpenNavMenu = (event) => {
  //   setAnchorElNav(event.currentTarget);
  // };

  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const openSelectedPage = (pageId) => {
    setCurrentPage(pageId)
  };

  const handleCloseUserMenu = (setting) => {
    if (setting === "Admin Paneli") window.open("http://127.0.0.1:8000/admin")
    if (setting === "Çıkış") window.location.reload()
    setAnchorElUser(null);
  };

  return (
    <AppBar>
      <Container>
        <Toolbar disableGutters>
          <Box
            component="img"
            src={Logo}
            alt="Giriş Resmi"
            sx={{ maxWidth: "5%", maxHeight: "auto", mr: 1 }}
          />

          <Box sx={{ flexGrow: 1, display: { xs: '1em', md: 'flex' } }}>
            {pages.map((page, index) => (
              <Button
                key={index}
                onClick={() => openSelectedPage(page?.id)}
                sx={{ my: 2, color: currentPage !== page.id ? 'white' : "none", display: 'block' }}
                color={currentPage === page.id ? 'warning' : ""}
              >
                {page.name}
              </Button>
            ))}
          </Box>
          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Kullanıcı">
              <IconButton color="inherit" onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <PersonIcon />
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: '45px' }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >


              {userInfo?.isAdmin && <MenuItem key={"Admin Paneli"} onClick={() => handleCloseUserMenu("Admin Paneli")}>
                <Typography sx={{ textAlign: 'center' }}>{"Admin Paneli"}</Typography>
              </MenuItem>}
              <MenuItem key={"Çıkış"} onClick={() => handleCloseUserMenu("Çıkış")}>
                <Typography sx={{ textAlign: 'center' }}>{"Çıkış"}</Typography>
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default AppBarComponent;