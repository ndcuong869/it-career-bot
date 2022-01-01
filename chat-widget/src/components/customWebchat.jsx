import Widget from "rasa-webchat";
import { useEffect, useRef } from "react";
import { useCookies } from "react-cookie";
import "../assets/css/widget.css";
import { login_window } from "../config";

export default function CustomWidget() {
  const webchatRef = useRef(null);
  const payload = "/greet";

  const openInNewTab = (url) => {
    const new_window = window.open(url, '_blank', 'noopener,noreferrer')
    if (new_window) new_window.opener = null
  }

  const channel = new BroadcastChannel("app-data");
  channel.addEventListener("message", (event) => {
    if (event.data.is_login === true) {
      const user_id = event.data.user_id;
      const user_name = event.data.user_name;

      if (webchatRef.current && webchatRef.current.sendMessage) {
        webchatRef.current.sendMessage(
          '/greetWithName{"user_id": "' +
            user_id +
            '",' +
            '"user_name": "' +
            user_name +
            '"' +
            "}"
        );

      }
    }
  });

  channel.addEventListener("message", (event) => {
    if (event.data.is_update_skills === true) {
      if (webchatRef.current && webchatRef.current.sendMessage) {
        webchatRef.current.sendMessage('/update_user_skills')
      }
    }
  });
  console.log("Rasa webchat init")
  return (
    <Widget
      ref={webchatRef}
      initPayload={payload}
      user
      // socketUrl={"http://localhost:5005"}
      socketUrl={"https://ff3f-115-73-217-121.ngrok.io"}
      customData={{ language: "en" }}
      title="IT Career bot"
      subtitle="Powered by FIT-HCMUS"
      showFullScreenButton={true}
      showMessageDate={false}
      profileAvatar="https://i.ibb.co/wQqdKPf/chatbot-icon.png"
      onSocketEvent={{
        'connect': () => console.log('connection established'),
        'bot_uttered': (message) => {
          if (message.text === "You are directed to the login page.")
          {
            openInNewTab("/login")
          }

          if (message.text === "You are directed to the register page.")
          {
            openInNewTab("/register")
          }

          if (message.text === "You are directed to the skill page.")
          {
            openInNewTab("/user/skills")
          }

          if (message.text === "You are directed to the survey page.")
          {
            openInNewTab("https://bit.ly/it_career_bot_survey_vi")
          }
      }
        ,
      }}
    />
  );
}
