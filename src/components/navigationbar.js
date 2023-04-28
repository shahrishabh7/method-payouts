import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import MenuItem from '@mui/material/MenuItem';
import { Stack } from '@mui/material';
import { Link } from 'react-router-dom';
import Button from '@mui/material/Button';
import Reporting from '../pages/reports'

const pages = ['Payouts', 'Reporting'];
const links = ['', '/reporting'];

const bar_theme = createTheme({
    status: {
        danger: '#e53e3e',
    },
    palette: {
        primary: {
            main: '#3d5a80',
        },
        secondary: {
            main: '#b87333',
        },
    },
});

export default function ButtonAppBar() {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <ThemeProvider theme={bar_theme}>
                <AppBar
                    position="fixed"
                    color="primary"
                >
                    <Toolbar>
                        <Typography
                            sx={{
                                flexGrow: 1,
                                textAlign: "left"
                            }}
                        >
                            <IconButton
                                size="large"
                                edge="start"
                                color="inherit"
                                aria-label="menu"
                            >
                            </IconButton>
                        </Typography>
                        <Stack direction='row' spacing={1}>
                            {pages.map((page, index) => (
                                <Link to={links[index]} style={{ textDecoration: 'none' }}>
                                    <MenuItem
                                        key={page}
                                        textAlign="right"
                                    >
                                        <Button key={page} sx={{ color: '#fff' }} style={{ fontSize: '16px', textTransform: 'none' }}>
                                            {page}
                                        </Button>
                                    </MenuItem>
                                </Link>

                            ))}
                        </Stack>
                    </Toolbar>
                </AppBar>
            </ThemeProvider>
        </Box >
    );
}