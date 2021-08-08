import React, { Component, useState } from "react";
import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Checkbox,
  FormControl,
  InputAdornment,
  InputLabel,
  OutlinedInput,
  Typography,
} from "@material-ui/core";

import EmailIcon from "@material-ui/icons/Email";
import LockIcon from "@material-ui/icons/Lock";
import PersonIcon from "@material-ui/icons/Person";
import WorkIcon from "@material-ui/icons/Work";
import { Link, useHistory } from "react-router-dom";
import DialogSkill from "../components/dialogSkill";
import RegisterImage from "../assets/images/register.png";
import axios from "axios";
import root_url from "../config";

function renderLink() {
  return <Link>Terms of use</Link>;
}

function renderVerifyCheckbox() {
  return (
    <div style={{ display: "flex", alignItems: "center", marginTop: "15px" }}>
      <Checkbox color="primary" />
      <Typography variant="caption">
        I accept the {renderLink()} and Privacy policy
      </Typography>
    </div>
  );
}

export default function RegisterPage() {
  const history = useHistory();
  const [isOpenDialog, openDialog] = useState(false);

  const preventDefault = (event) => {
    event.preventDefault();
    history.push("/login");
  };

  const openDialogSkill = () => {
    openDialog(true);
  };

  const closeDialogSkill = () => {
    openDialog(false);
  };
  return (
    <div className="container-form">
      <DialogSkill isOpen={isOpenDialog} closeDialog={closeDialogSkill}/>
      <Card style={{}}>
        <CardHeader
          title="Register your account"
          subheader="Explore more your career path"
        ></CardHeader>
        <CardContent style={{ display: "flex" }}>
          <div className="container-image">
            <img
              width={400}
              height={400}
              style={{
                objectFit: "cover",
                marginRight: "20px",
              }}
              src={RegisterImage}
            />
          </div>
          <div
            className="container-two-forms"
            style={{
              display: "flex",
              flexDirection: "column",
            }}
          >
            <div style={{ display: "flex" }}>
              <form>
                <FormControl fullWidth variant="outlined">
                  <InputLabel htmlFor="outlined-adornment-password">
                    Email
                  </InputLabel>
                  <OutlinedInput
                    id="outlined-adornment-amount"
                    labelWidth={60}
                    startAdornment={
                      <InputAdornment position="start">
                        <EmailIcon />
                      </InputAdornment>
                    }
                  />
                </FormControl>

                <div style={{ marginTop: "20px" }}></div>
                <FormControl fullWidth variant="outlined">
                  <InputLabel htmlFor="outlined-adornment-password">
                    Password
                  </InputLabel>
                  <OutlinedInput
                    id="outlined-adornment-amount"
                    labelWidth={100}
                    type="password"
                    startAdornment={
                      <InputAdornment position="start">
                        <LockIcon />
                      </InputAdornment>
                    }
                  />
                </FormControl>
                <div style={{ marginTop: "20px" }}></div>
                <FormControl fullWidth variant="outlined">
                  <InputLabel htmlFor="outlined-adornment-password">
                    Re-type password
                  </InputLabel>
                  <OutlinedInput
                    id="outlined-adornment-amount"
                    labelWidth={150}
                    type="password"
                    startAdornment={
                      <InputAdornment position="start">
                        <LockIcon />
                      </InputAdornment>
                    }
                  />
                </FormControl>
              </form>

              <form
                style={{
                  marginLeft: "20px",
                  display: "flex",
                  flexDirection: "column",
                }}
              >
                <FormControl fullWidth variant="outlined">
                  <InputLabel htmlFor="outlined-adornment-password">
                    Your name
                  </InputLabel>
                  <OutlinedInput
                    id="outlined-adornment-amount"
                    labelWidth={100}
                    startAdornment={
                      <InputAdornment position="start">
                        <PersonIcon />
                      </InputAdornment>
                    }
                  />
                </FormControl>

                <FormControl
                  fullWidth
                  variant="outlined"
                  style={{ marginTop: "20px" }}
                >
                  <InputLabel htmlFor="outlined-adornment-password">
                    Job title
                  </InputLabel>
                  <OutlinedInput
                    id="outlined-adornment-amount"
                    labelWidth={100}
                    startAdornment={
                      <InputAdornment position="start">
                        <WorkIcon />
                      </InputAdornment>
                    }
                  />
                </FormControl>

                <Button
                  variant="contained"
                  style={{
                    backgroundColor: "#1abc9c",
                    color: "#ffffff",
                    width: "250px",
                    height: "55px",
                    marginTop: "20px",
                  }}
                  onClick={openDialogSkill}
                >
                  Add your skills
                </Button>
              </form>
            </div>
            <div className="verify-checkbox">{renderVerifyCheckbox()}</div>
            <div className="container-buttons" style={{display: 'flex', marginTop: '20px'}}>
              <Button
                variant="contained"
                style={{
                  backgroundColor: "#0062e6",
                  color: "#ffffff",
                  width: "260px",
                  height: '50px'
                }}
              >
                Register
              </Button>
            </div>
            <div style={{ marginTop: "10px" }}>
              <CardActions>
                <Typography
                  variant="caption"
                >
                  <Typography variant="inherit">
                    Already have an account?
                  </Typography>
                  <Link
                    style={{
                      marginLeft: "8px",
                      marginRight: "45px",
                    }}
                    variant="inherit"
                    href="#"
                    onClick={preventDefault}
                  >
                    Login now
                  </Link>
                </Typography>
              </CardActions>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
