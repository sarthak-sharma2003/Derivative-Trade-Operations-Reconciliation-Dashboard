import React, { useState, useEffect } from 'react';
import { Button, Card, CardContent, Typography } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const REAL_TIME_API_URL = 'http://localhost:5001/api/trade-data';
const HISTORICAL_API_URL = 'http://localhost:5001/api/historical-trade-data';
const RECONCILIATION_API_URL = 'http://localhost:5001/api/reconciliation';

const DerivativesDashboard = () => {
    const [tradeData, setTradeData] = useState([]);
    const [dataMode, setDataMode] = useState('real-time');
    const [discrepancies, setDiscrepancies] = useState([]);

    useEffect(() => {
        fetchTradeData();
        fetchReconciliationData();
    }, [dataMode]);

    const fetchTradeData = async () => {
        try {
            const response = await fetch(dataMode === 'real-time' ? REAL_TIME_API_URL : HISTORICAL_API_URL);
            const data = await response.json();
            setTradeData(data);
        } catch (error) {
            console.error('Failed to fetch trade data:', error);
        }
    };

    const fetchReconciliationData = async () => {
        try {
            const response = await fetch(RECONCILIATION_API_URL);
            const data = await response.json();
            setDiscrepancies(data);
        } catch (error) {
            console.error('Failed to fetch reconciliation data:', error);
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
                <Button
                    variant={dataMode === 'real-time' ? 'contained' : 'outlined'}
                    color="primary"
                    onClick={() => setDataMode('real-time')}
                >
                    Real-Time Data
                </Button>
                <Button
                    variant={dataMode === 'historical' ? 'contained' : 'outlined'}
                    color="primary"
                    onClick={() => setDataMode('historical')}
                >
                    Historical Data
                </Button>
            </div>
            <Card>
                <CardContent>
                    <Typography variant="h5" gutterBottom>
                        {dataMode === 'real-time' ? 'Real-Time Trade Data' : 'Historical Trade Data'}
                    </Typography>
                    {tradeData.length > 0 ? (
                        <ResponsiveContainer width="100%" height={400}>
                            <LineChart data={tradeData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="date" />
                                <YAxis />
                                <Tooltip />
                                <Line type="monotone" dataKey="tradeVolume" stroke="#8884d8" activeDot={{ r: 8 }} />
                            </LineChart>
                        </ResponsiveContainer>
                    ) : (
                        <Typography color="textSecondary">
                            No trade data available at the moment.
                        </Typography>
                    )}
                </CardContent>
            </Card>
        </div>
    );
};

export default DerivativesDashboard;
