import { Container } from '@mui/system'
import { TextField, Button } from '@mui/material'
import { useState, useCallback } from 'react'
import { ThemeProvider } from '@mui/material/styles'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import { Link } from 'react-router-dom'
import { v4 as uuidv4 } from 'uuid'

function Reporting() {

    return (
        <div className='App'>
            <header className='App-header'>
                {/* <div class='spin'>
            <img src={logo} className="App-logo"/>
        </div> */}
                <h1>Reports</h1>
                <div className='App'>
                </div>
                <div>
                    <Link to={'/results'} style={{ textDecoration: 'none' }}>
                        <Button
                            variant='outlined'
                            size='large'
                            sx={{ border: 1.5 }}
                            style={{ textTransform: 'none' }}
                        >
                            Submit
                        </Button>
                    </Link>
                </div>
            </header>
        </div>
    )
}

export default Reporting