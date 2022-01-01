import { Card, CardContent } from "@material-ui/core";
import axios from "axios";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import root_url from "../config";

function useQuery() {
    return new URLSearchParams(useLocation().search);
  }

function renderDashboard(data) {
    return (
        <>
        <div className="container-form">
            <Card style={{ width: "800px", height: "370px", padding: '20px'}}
        className="form-login"
        variant="outlined">
            <CardContent>
                <h2>Dashboard</h2>
                <h3>{"User statistics (" + new Date().toLocaleString() + ")"}</h3>
                <p>{"Registered users: " + data['total_users']}</p>
                <p>{"The number of active users in last 1 hour: " + data['total_active_1']}</p>
                <p>{"The number of active users in last 24 hours: " + data['total_active_24']}</p>
                <p>{"Total feedback: " + data['total_feedback'] + "/" + data['total_users']}</p>
            </CardContent>
            </Card>
        </div>
        </>
    )
}

export const Dashboard = () => {
    const query = useQuery()
    const token = query.get('token')
    const [isValid, setIsValid] = useState(false)
    const [data, setData] = useState([{'total_users': 0}])

    useEffect(() => {
        axios.get(root_url + '/api/dashboard?token=' + token)
        .then(response => {
            if (response.status === 200) {
                setIsValid(true)
                setData([response.data])
            }
        })
    }, [])

    if (isValid === true) {
        return renderDashboard(data[0])
    }

    return <>
        <div>The access is invalid.</div>
    </>

    return <></>
}

