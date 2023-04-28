import { Table, TableContainer, TableHead, TableRow, TableCell, TableBody } from '@mui/material';
import Paper from '@mui/material/Paper';
import { makeStyles } from '@mui/styles';
import Box from '@mui/material/Box';

const useStyles = makeStyles({
    root: {
        background: '#45484d',
    },
    tableWrapper: {
        height: '400px',
        overflow: 'auto',
    },
    text: {
        color: 'white' // Set the color to white
    }
});

function PayoutsPreviewTable(props) {
    const { payoutsPreview } = props;
    let names = payoutsPreview['payment_table']['Name']
    let amounts = payoutsPreview['payment_table']['Amount']

    let total_amount = payoutsPreview['total_amount'].toLocaleString('en-US', { style: 'currency', currency: 'USD' });


    const classes = useStyles();

    return (
        <>
            <Box sx={{pb:5}}>
                Total Payout: {total_amount}
            </Box>
            <Paper className={classes.root}>
                <div className={classes.tableWrapper}>
                    <Table style={{ width: '100%' }}>
                        <TableHead>
                            <TableRow>
                                <TableCell className={classes.text}>Name</TableCell>
                                <TableCell className={classes.text}>Amount</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {names.map((name, index) => (
                                <TableRow key={name}>
                                    <TableCell className={classes.text}>{name}</TableCell>
                                    <TableCell className={classes.text}>{amounts[index]}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div>
            </Paper>
        </>
    );
}

export default PayoutsPreviewTable;