import { Card, CardHeader, Typography } from "@material-ui/core";
import { render } from "@testing-library/react";
import React, { Component, useEffect, useState } from "react";

function renderTitle() {
    return(
        <Typography variant='h5' style={{color: '#1abc9c'}}>
            You register successfully.
        </Typography>
    )
}

export default function RegisterSuccessPage() {
  const [timer, setTimer] = useState(5)

  const countDown = () => {
    setTimer(timer - 1)
  }

  if (timer === 0) {
    window.location ="/login"
  }

  useEffect(() => {
    const timer_control = setInterval(countDown, 1000)

    return () => clearInterval(timer_control)
  })

  return (
    <div className="container-form">
      <Card>
        <CardHeader
          title={renderTitle()}
          subheader="Close this window and enjoy the IT career bot now."
        />
        <div style={{'marginBottom': '10px'}}>{"Redirecting to login page in " + timer.toString() + " seconds."}</div>
      </Card>
    </div>
  );
}
