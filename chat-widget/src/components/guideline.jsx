import {
  Card,
  CardContent,
  CardHeader,
  Typography,
  Paper
} from "@material-ui/core";
import React, { Component } from "react";
import { Link } from "react-router-dom";
import guideline from "../assets/images/guideline.png";

function renderCardItem(step, content) {
  return (
    <>
      <Paper variant="outlined" style={{ maxWidth: "450px", marginBottom: "20px", padding: '10px'}}>
            <Typography gutterBottom variant="h5" color='textPrimary' component="h2" align='left'>
              {step}
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p" align='left'>
              {content}
            </Typography>
      </Paper>
    </>
  );
}

export default function Guideline() {
  const items = [
    { step: "Step 1", content: "Click the right bottom icon in the website." },
    {
      step: "Step 2",
      content: "Ask the chatbot about your learning path.",
    },
    {
      step: "Step 3",
      content:
        "Complete the survey at the end of the conversation to improve your experience next time.",
    },
  ];

  return (
    <div className="container-form">
      <Card style={{maxWidth: '1000px'}}>
        <CardHeader
          title="IT CAREER BOT"
          subheader="IT Career Bot is a career counseling chatbot that helps students (especially senior students who are about to graduate and work in the labor market) as well as employees (who intend to change their current job) to figure out who they are and what they want on their career path. "
        />
        <div className="main-container" style={{ display: "flex" }}>
          <img
            width={400}
            height={400}
            style={{
              objectFit: "cover",
              marginRight: "20px",
              marginLeft: "20px",
            }}
            src={guideline}
          />
          <div className="content">
            <CardContent>
              {items.map((item) => renderCardItem(item.step, item.content))}
            </CardContent>
          </div>
        </div>

        <div className="footer">
          <Typography variant="h5" style={{ marginBottom: "20px" }}>
            Thank you for taking the time to complete this survey.
          </Typography>

          <Typography style={{ marginBottom: "10px" }} variant='caption'>
              <Link>Report if you cannot use the bot.</Link>
          </Typography>
        </div>
      </Card>
    </div>
  );
}
