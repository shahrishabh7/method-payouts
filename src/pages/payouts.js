import { Container } from '@mui/system'
import { TextField, Button, Stack } from '@mui/material'
import { useState, useCallback } from 'react'
import Dropzone from '../components/dropzone.js'
import { createTheme, ThemeProvider } from '@mui/material/styles'
import Typography from '@mui/material/Typography'
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box'
import { v4 as uuidv4 } from 'uuid'
import PayoutsPreviewTable from '../components/payouts_preview_table.js'

const button_theme = createTheme({
    status: {
        danger: '#e53e3e'
    },
    palette: {
        primary: {
            main: '#371d10'
        },
        secondary: {
            main: '#b87333'
        },
        background: {
            main: '#e4cead'
        }
    },
    typography: {
        fontSize: 28
    }
})

function Payouts() {
    const [XMLFile, setXMLFile] = useState(null);
    const [payoutsPreview, setPayoutsPreview] = useState(null);
    const [paymentsData, setPaymentsData] = useState(null);

    const onDrop = useCallback(acceptedFiles => {
        const file = acceptedFiles[0];
        const reader = new FileReader();
        console.log(file)
        reader.onload = function (e) {
            setXMLFile({ xml: e.target.result });
        };
        reader.readAsDataURL(file);
    }, []);

    const handleSubmit = e => {
        e.preventDefault()
        fetch('/process_xml', {
            method: 'post',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                xml: XMLFile
            })
        })
            .then(response => {
                console.log('object posted')
                if (!response.ok) {
                    throw new Error('Network response was not ok')
                }
                return response.json()
            })
            .then(data => {
                console.log('data received', data)
                if (!data && !data.result) {
                    throw new Error('Response data is not valid')
                }
                setPayoutsPreview(data['payments_preview']);
                setPaymentsData(data['payment_data']);
            })
            .catch(error => {
                // Handle any errors that occur during the request
                console.error(error)
            })
    }

    const handleAuthorize = e => {
        e.preventDefault()
        fetch('/process_payments', {
            method: 'post',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                paymentsData: paymentsData
            })
        })
            .then(response => {
                console.log('object posted')
                if (!response.ok) {
                    throw new Error('Network response was not ok')
                }
                return response.json()
            })
            .then(data => {
                console.log('data received', data)
                if (!data && !data.result) {
                    throw new Error('Response data is not valid')
                }
            })
            .catch(error => {
                // Handle any errors that occur during the request
                console.error(error)
            })
    }

    return (
        <div className='App'>
            <header className='App-header'>
                <Box sx={{pt:6}}></Box>
                <h1>Payouts</h1>
                <div className='App'>
                    <p></p>
                    <div className='App container mt-5' style={{ width: 600 }}>
                        <Dropzone onDrop={onDrop}></Dropzone>
                    </div>
                    <aside>
                        {/* <p style={{ fontSize: 23 }}> {XMLInfo.length} Files Uploaded </p> */}
                    </aside>
                    <p></p>
                </div>
                <div>
                    <Button
                        variant='outlined'
                        onClick={handleSubmit}
                        size='large'
                        sx={{ border: 1.5 }}
                        style={{ textTransform: 'none' }}
                    >
                        Submit
                    </Button>
                </div>
                <div>
                    {payoutsPreview && (
                        <>
                            <Typography variant="h5" sx={{ pt: 5 }}>Payouts are staged.</Typography>
                            <Typography variant="h5" sx={{ pb: 5 }}>Confirm details below to complete payouts.</Typography>
                            <Stack direction="row" spacing={2} sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: 2, pb: 5 }}>
                                <Button variant="contained" onClick={handleAuthorize}>Authorize</Button>
                                <Button variant="outlined">Discard</Button>
                            </Stack>
                            <PayoutsPreviewTable sx={{ marginTop: 20 }} payoutsPreview={payoutsPreview}></PayoutsPreviewTable>
                        </>
                    )}
                </div>
            </header>
        </div>
    )
}

export default Payouts