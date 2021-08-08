import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  FormControl,
  InputAdornment,
  InputLabel,
  OutlinedInput,
  Typography,
} from "@material-ui/core";
import React, { Component, useState } from "react";
import "../assets/css/login.css";
import EmailIcon from "@material-ui/icons/Email";
import LockIcon from "@material-ui/icons/Lock";
import { useHistory } from "react-router";
import { Link } from "react-router-dom";
import root_url from "../config";
import axios from "axios";
import { useCookies } from "react-cookie";
import loginImage from '../assets/images/login.png'

export default function LoginPage() {
  const history = useHistory();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [cookies, setCookie] = useCookies(["user"]);

  const preventDefault = (event) => {
    event.preventDefault();
    history.push("/register");
  };

  const updateUsername = (evt) => setUsername(evt.target.value);
  const updatePassword = (evt) => setPassword(evt.target.value);

  const loginHandler = () => {
    const data = {
      username: username,
      password: password,
    };

    axios.post(root_url + "/api/login", data).then((response) => {
      setCookie("user", response["data"]["id"], {
        path: "/",
      });
      const channel = new BroadcastChannel("app-data");
      channel.postMessage({ is_login: true, user_id: response["data"]["id"], user_name: response["data"]["name"] });
      history.push("/login_success");
    });
  };

  return (
    <div className="container-form">
      <Card
        style={{ width: "800px", height: "370px", padding: '20px'}}
        className="form-login"
        variant="outlined"
      >
        <div className="container-elements" style={{ display: "flex" }}>
          <div className="container-images">
          <img
              width={400}
              height={400}
              style={{
                objectFit: "cover",
                marginRight: "20px",
              }}
              src={loginImage}
            />
          </div>
          <div>
            <CardHeader
              title="IT Career Bot"
              subheader="Powered by FIT-HCMUS"
            ></CardHeader>
            <CardContent>
              <form>
                <FormControl fullWidth variant="outlined">
                  <InputLabel htmlFor="outlined-adornment-password">
                    Email
                  </InputLabel>
                  <OutlinedInput
                    id="outlined-adornment-amount"
                    labelWidth={60}
                    onChange={updateUsername}
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
                    onChange={updatePassword}
                    startAdornment={
                      <InputAdornment position="start">
                        <LockIcon />
                      </InputAdornment>
                    }
                  />
                </FormControl>
              </form>
            </CardContent>
            <CardActions>
              <Button
                variant="contained"
                style={{
                  backgroundColor: "#0062e6",
                  color: "#ffffff",
                  width: "365px",
                  height: "50px",
                  marginLeft: "8px",
                }}
                onClick={loginHandler}
              >
                Login
              </Button>
              <div></div>
            </CardActions>
            <div style={{ margin: "10px" }}>
              <Typography variant="inherit">Don't have account?</Typography>
              <Link
                style={{
                  marginLeft: "8px",
                  marginRight: "15px",
                }}
                variant="inherit"
                href="#"
                onClick={preventDefault}
              >
                Sign up
              </Link>
            </div>
            <Typography
              variant="caption"
              style={{
                marginTop: "20px",
                marginBottom: "20px",
              }}
            >
              Copyright &copy; 2021 IT Career Bot
            </Typography>
          </div>
        </div>
      </Card>
    </div>
  );
}

var firebaseConfig = {
  apiKey: "AIzaSyAvoQzCLkd3JY-WN587igZVR9JaJHWaVTA",
  authDomain: "it-career-bot.firebaseapp.com",
  databaseURL: "https://it-career-bot-default-rtdb.firebaseio.com",
  projectId: "it-career-bot",
  storageBucket: "it-career-bot.appspot.com",
  messagingSenderId: "586704512898",
  appId: "1:586704512898:web:7a8f27b35c2d02605c119b",
  measurementId: "G-P86VYPZBCD",
};
// Initialize Firebase
//firebase.initializeApp(firebaseConfig);
